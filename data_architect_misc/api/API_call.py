"""
Author: Phyo Thiha
Last modified date: Dec 11, 2017
Description: Python script to call API and save the data/file into local directory.

Input: Input to the python script will be config.ini file as a command line argument,
which contains all the required parameters to execute the script.

Output: As a output, the data/file will be saved to local directory in a file.

Usage: 
$python API_call.py <config file name along with path>
"""

import sys
import time
import os
import requests
import ConfigParser
#import configparser # for Python 3.0+
import logging
from logbeam import CloudWatchLogsHandler

# Class to read config.ini file as a command line parameter and save required variable values
class readConfigFile():
    configFileName = sys.argv[1]
    config = ConfigParser.ConfigParser()
    config.readfp(open(configFileName))  # Reading parameters from config file.

    #Variables to hold values for required parameters
    API_NAME = config.get('api_call', 'API_NAME')                       # Read API_NAME from config file
    API_LOCAL_DIR = config.get('api_call', 'API_LOCAL_DIR')             # Read local directory path name to store data file on local
    CW_LOG_GROUP_NAME = config.get('api_call', 'CW_LOG_GROUP_NAME')     # Read AWS CloudWatch Log Group Name for logging
    CW_LOG_STREAM_NAME = config.get('api_call', 'CW_LOG_STREAM_NAME')   # Read AWS CloudWatch Log Stream Name for logging
    CW_LOG_FLAG = config.get('api_call', 'CW_LOG_FLAG')                 # Read temporary flag to decide whether to implement logging or not

    # CloudWatch logger configuration
    cw_handler = CloudWatchLogsHandler(
    log_group_name=CW_LOG_GROUP_NAME,
    log_stream_name=CW_LOG_STREAM_NAME
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(cw_handler)

def apiCall():
    API_NAME = readConfigFile.API_NAME
    API_LOCAL_DIR = readConfigFile.API_LOCAL_DIR
    try:
        response = requests.get(API_NAME, verify=False)
        with open(os.path.join(API_LOCAL_DIR, 'data.json'),'w') as f:  # Open data.json file in write mode to save API data
            f.write(response._content)
            log(time.ctime() + " API data saved successfully to file!!")
            print("success")
    except Exception, e:
        log(time.ctime() + " can not open file due to: " + str(e))
        log(time.ctime() + " " + "API call failed due to: " + str(e))
        sys.exit(log("Report: " + time.ctime() + " " + "Ending Application!!"))
    return
#End of function

def log(logstr):
    CW_LOG_FLAG = readConfigFile.CW_LOG_FLAG
    logger = readConfigFile.logger
    if CW_LOG_FLAG == 'true':
        logger.info(logstr)
    return


if len(sys.argv) != 2:
    print "Usage: apiCall.py <config.ini>"
    sys.exit(1)
else:
    apiCall()  # Calling function apiCall()
