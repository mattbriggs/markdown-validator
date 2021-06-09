''' Modular Doc Utilites

    Module contains common functions used by the Python script modules
    working with text files.
'''

import os
import csv

def get_textfromfile(path):
    """Return text from a MD filename path.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
    textout = ""
    fh = open(path, "r")
    for line in fh:
        textout += line
    fh.close()
    return textout


def write_text(outbody, path):
    """Write text file to the path.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
    out_file = open(path, "w")
    for line in outbody:
        out_file.write(line)
    out_file.close()


def write_csv(outbody, path):
    """Write CSV file to the path.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
    csvout = open(path, 'w', newline="")
    csvwrite = csv.writer(csvout)
    for r in outbody:
        try:
            csvwrite.writerow(r)
        except Exception as e:
            print("An error: {}".format(e))
    csvout.close()


def get_files(inpath, extension):
    """With the directory path, returns a list of markdown file paths.

        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
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