''' Modular Doc Utilites

    Module contains common functions used by the Python script modules
    working with text files.
'''

import os
import csv

def get_textfromfile(path):
    """Return text from a MD filename path.

        :param path: Path to a file. (c:\textfile.txt)
        :type string: File path
        ...
        :return: The text from the file.
        :rtype: string
        """
    textout = ""
    fh = open(path, "r")
    for line in fh:
        textout += line
    fh.close()
    return textout


def write_text(outbody, path):
    """Write text file to the path.

        :param outbody: The contents of the file to saved as a string.
        :type string: File contents.

        :param path: Path to a file. (c:\textfile.txt)
        :type string: File path.
        """
    out_file = open(path, "w")
    for line in outbody:
        out_file.write(line)
    out_file.close()


def write_csv(outbody, path):
    """Write CSV file to the path.

        :param outbody: A list of lists containing the header and rows.
        :type List: A list of lists.

        :param path: Full path name including the file. (c:\output.csv)
        :type string: File path
        ...
        :raises Error: Prints the error code.
        """
    csvout = open(path, 'w', newline="")
    csvwrite = csv.writer(csvout)
    for r in outbody:
        try:
            csvwrite.writerow(r)
        except Exception as e:
            print("An error: {}".format(e))
    csvout.close()


def get_files(inpath, extension=".md"):
    """With the directory path, returns a list of markdown file paths.

        :param inpath: Path to the folder containing the files.
        :type string: The path to a folder. (required)

        :param extension: File extension to filter retrieved files.
        :type string: The file extension. For example, ".md" (default) (optional)
        ...
        :return: Returns a list of filtered files.
        :rtype: List
        """
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