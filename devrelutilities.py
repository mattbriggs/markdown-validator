''' Name

    This script will 
    Input
    Output

    Matt Briggs V0.0: X.X.2019
'''

import os
import csv
from datetime import datetime, timedelta
from prettytable import PrettyTable

THISDATE = str(datetime.now().strftime("%Y-%m-%d"))

def get_text_from_file(path):
    '''Return text from a text filename path'''
    textout = ""
    fh = open(path, "r")
    for line in fh:
        textout += line
    fh.close()
    return textout


def write_text(outbody, path):
    '''Write text file to the path.'''
    out_file = open(path, "w")
    for line in outbody:
        out_file.write(line)
        #out_file.write("\n")
    out_file.close()


def write_csv(outbody, path):
    '''Write CSV file to the path.'''
    csvout = open(path, 'w', newline="")
    csvwrite = csv.writer(csvout)
    for r in outbody:
        csvwrite.writerow(r)
    csvout.close()


def make_path_url(instring):
    '''Take a filepath and turns into a url for the docs repo.
    C:\Git\MS\azure-stack-docs-pr\azure-stack\operator\azure-stack-add-vm-image.md
    https://docs.microsoft.com/en-us/azure-stack/operator/azure-stack-add-vm-image
    
    orginal stem: "https://docs.microsoft.com/en-us/azure/{}'''

    stem = instring.split("\\")[-1].split(".")[0].replace("\\", "/")
    folder = instring.split("\\")[-2]
    return "https://docs.microsoft.com/en-us/azure-stack/{}/{}".format(folder, stem)

def make_path_url_azure_repo(instring):
    '''Take a filepath and turns into a url for the docs repo.'''
    start_index = instring.find("articles") + 9
    extension = instring.split(".")
    stem = extension[0][start_index:].replace("\\", "/")
    return "https://docs.microsoft.com/en-us/azure/{}".format(stem)


def get_files(inpath):
    '''With the directory path, returns a list of markdown file paths.'''
    outlist = []
    for (path, dirs, files) in os.walk(inpath):
        for filename in files:
            ext_index = filename.find(".")
            if filename[ext_index+1:] == "md":
                entry = path + "\\" + filename
                outlist.append(entry)
    return outlist


def main():
    print("This is the developer relations utility.")


if __name__ == "__main__":
    main()
