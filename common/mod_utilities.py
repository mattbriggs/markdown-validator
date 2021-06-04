''' Modular Doc Utilites

    This script contains common functions used by the python script modules
    in this repository.

    Matt Briggs V1.0: 7.29.2020
'''

import os
import csv

def get_textfromMD(path):
    '''Return text from a MD filename path'''
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
    out_file.close()


def write_csv(outbody, path):
    '''Write CSV file to the path.'''
    csvout = open(path, 'w', newline="")
    csvwrite = csv.writer(csvout)
    for r in outbody:
        try:
            csvwrite.writerow(r)
        except Exception as e:
            print("An error: {}".format(e))
    csvout.close()


def get_files(inpath, extension):
    '''With the directory path, returns a list of markdown file paths.'''
    outlist = []
    for (path, dirs, files) in os.walk(inpath):
        for filename in files:
            ext_index = filename.find(".")
            if filename[ext_index+1:] == extension:
                entry = path + "\\" + filename
                outlist.append(entry)
    return outlist


def main():
    print("This is module contains commonly used functions.")


if __name__ == "__main__":
    main()