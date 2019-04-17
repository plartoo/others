"""
Author: Phyo Thiha
Last Modified : December 13, 2017
Description: Python script to download specified attachment from specified email subject from an
unread mail.

Enter input parameters in the config.ini file, which will then be passed  as a command line argument.

As an output, the email attachment(s) will be saved to the specified local path.

Usage:
$python email_attachment_to_local.py <config file name along with path>
"""

import sys
import imaplib
import src.email
import logging
import ConfigParser
from logbeam import CloudWatchLogsHandler

configFilePath = sys.argv[1]
configReader = ConfigParser.ConfigParser()
configReader.readfp(open(configFilePath))

SMTPServer = configReader.get('EmailFetcher', 'SMTPServer')  # SMTP Server name read from config file
UserName = configReader.get('EmailFetcher', 'UserName')  # SMTP User name read from config file
Password = configReader.get('EmailFetcher', 'Password')  # SMTP password read from config file
Subject = configReader.get('EmailFetcher', 'Subject')  # Email Subject name read from config file
FileName = configReader.get('EmailFetcher', 'FileName')  # Email attachment filename to download read from config file
LocalPath = configReader.get('EmailFetcher',
                             'LocalPath')  # Local directory name to download attachment read from config file
LogGroupName = configReader.get('EmailFetcher',
                                'LogGroupName')  # AWS CloudWatch Log Group Name for logging read from config file
LogStreamName = configReader.get('EmailFetcher',
                                 'LogStreamName')  # AWS CloudWatch Log Stream Name for logging read from config file

# Flag to decide, whether to logging into CloudWatch or not read from config file
cloudWatchLogFlag = configReader.get('EmailFetcher',
                                     'cloudWatchLogFlag')
emailArchiveFlag = configReader.get('EmailFetcher', 'emailArchiveFlag')
emailDeleteFlag = configReader.get('EmailFetcher', 'emailDeleteFlag')

# CloudWatch logger configuration
cw_handler = CloudWatchLogsHandler(log_group_name=LogGroupName, log_stream_name=LogStreamName)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(cw_handler)

# Connect to an IMAP server
def connect(server, user, password):
    m = imaplib.IMAP4_SSL(server)
    m.login(user, password)
    m.select()
    return m

class NoUnreadEmailFound(Exception):
    pass

class NoAttachmentFound(Exception):
    pass

# Download all attachment files for a given email
def downloadAttachmentsInEmail(m, emailid, filename, outputdir):
    resp1, data = m.uid('FETCH', emailid, '(BODY.PEEK[])')
    m.uid('STORE', emailid, '-FLAGS', '(\Seen)')
    email_body = data[0][1]
    mail = src.email.message_from_string(email_body)
    attachmentFound = False
    try:
        for part in mail.walk():
            # Allowed file-types : Tab delimited files, Plain txt files, CSVs, JSONs
            if str(part.get('Content-Disposition')).startswith('attachment') and part.get_filename() == filename:
                open(outputdir + '/' + part.get_filename(), 'wb').write(part.get_payload(decode=True))
                attachmentFound = True
                log('Requested attachment : %s found and downloaded.' % part.get_filename())
                m.uid('STORE', emailid, '+FLAGS', '(\Seen)')
                log("Email marked as read")
                if emailArchiveFlag == 'true':  # check flag, whether to archive email or not
                    markAsArchive(m, emailid)  # Calling function to archive emails
                elif emailDeleteFlag == 'true':  # check flag, whether to delete email or not
                    m.uid('STORE', emailid, '+FLAGS', '(\Deleted)')
                    m.expunge()
                    log("Downloaded attachment deleted successfully")
                if attachmentFound == False:
                    log('Requested attachment %s not found.' % filename)
                    raise NoAttachmentFound
    except NoAttachmentFound:
        log(
            "Attachment with expected file-name not found or expected file format not found. **Allowed file formats: Tab delimited files, Plain txt files, CSVs, JSONs")


# Function to Search all unread mails for the given subject
def getUnreadMails(server, user, password, subject, filename, outputdir):
    m = connect(server, user, password)
    resp, item = m.uid('SEARCH',
                       '(UNSEEN SUBJECT "%s")' % subject)  # Search for unread emails in the inbox as per subject name.
    items = item[0].split()
    try:
        if len(items) == 0:
            log('Found {0} unread messages with Subject "{1}"'.format(len(items), subject))
            raise NoUnreadEmailFound
        else:
            log('Found {0} unread messages with Subject "{1}"'.format(len(items), subject))
            for emailid in items:
                resp, data = m.uid('FETCH', emailid, '(RFC822)')
                m.uid('STORE', emailid, '-FLAGS', '(\Seen)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = src.email.message_from_string(response_part[1])
                        for header in ['subject']:
                            if (msg[header]) == subject:
                                downloadAttachmentsInEmail(m, emailid, filename, outputdir)
    except NoUnreadEmailFound:
        log('Found {0} unread messages with Subject "{1}"'.format(len(items), subject))
        sys.exit()
    except Exception as e:
        log("Attachment could not be downloaded" + " " + str(e))


# Function to move processed email to archive folder
def markAsArchive(m, emailid):
    try:
        result = m.uid('COPY', emailid, 'Inbox/archive')
        if result[0] == 'OK':
            m.uid('STORE', emailid, '+FLAGS', '(\Deleted)')
            m.expunge()
            log("Downloaded attachment moved to Archive folder successfully")
    except Exception as e:
        log(str(e))

def log(logstr):
    if cloudWatchLogFlag == 'true':
        logger.info(logstr)
    return

if len (sys.argv) != 2 :
    print("Usage: email_attachment_to_local.py <config.ini>")
    sys.exit (1)
else:
    getUnreadMails(SMTPServer, UserName, Password, Subject, FileName, LocalPath)
