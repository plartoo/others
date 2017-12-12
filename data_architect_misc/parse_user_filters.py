import xml.etree.ElementTree as ET
import os, time, re, sys, csv, getopt

def main(argv):
    """
    Author: Phyo Thiha
    
    Description: Script to scrape the data permission and client 
    access permission data from the Tableau workbook (TWB) files. 
    This outputs a file with individual username paired with the 
    client names they are allowed to see. Tested with Tableau 10.0+.

    Run:
    > python parse_user_filters.py -h
    to find out how to use.
    """
    input_file = ''
    output_file = ''

    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('Usage: parse_user_filters.py -i <input file> -o <output file>')
        sys.exit(2)

    if len(argv) == 0:
        print('Usage: parse_user_filters.py -i <input file> -o <output file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('Usage: parse_user_filters.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
            file_out = open(output_file, 'w')

    # Extract meta data about the input file such as file path,
    # last modified date, current extraction date and column headers
    full_path = os.path.abspath(input_file)
    file_out.write("File Full Path: " + full_path + "\n")

    last_modified = time.ctime(os.path.getmtime(input_file))
    file_out.write("File Last Modified On: " + last_modified + "\n\n")

    cur_date = time.strftime("%c")
    file_out.write("Permission Info Below Extracted On: " + cur_date + "\n\n\n")

    file_out.write("UserID, Advertiser\n")
    # Parsing the XML begins here
    tree = ET.parse(input_file)
    root = tree.getroot()
    parent=root.findall(".//group[@name='[AdvertiserAccess]']/groupfilter/groupfilter/groupfilter[@function='filter']")

    for child in parent[1:]:
        if child.attrib['expression']:
            expr = child.attrib['expression']
            regex_match = re.search('.*\\\\(.+)\'\)', expr)
            if regex_match:
                user_name = regex_match.group(1)

            if user_name:
                member = 'UNKNOWN'
                for eee in child.findall("./groupfilter"):
                    if ('from' in eee.attrib) and ('to' in eee.attrib): # for admins
                        member = 'ALL'
                        file_out.write(user_name + ", " + member + "\n")
                for eee in child.findall("./groupfilter/groupfilter"):
                    if ('member' in eee.attrib): # for members
                        member = eee.attrib['member']
                        file_out.write(user_name + ", " + member + "\n")
                for eee in child.findall("./groupfilter[@function='member']"):
                    if ('member' in eee.attrib):
                        member = eee.attrib['member']
                        file_out.write(user_name + ", " + member + "\n")

    print("Output file written to: ", output_file)
    file_out.close()

if __name__ == "__main__":
    main(sys.argv[1:])
