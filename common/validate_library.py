'''
This script will parse and validate the current known issues includes from Azure Stack Hub
(9/1/2020).

    The function validates the includes in the repository.

    1.  Configure the script by updating the global variables.
        MODULES points to the module folder.
        VALIDATIONREPORT points to the location of the validation report.
    2.  Run the script.
    3.  Open the validation report.

'''

import cmd
import pathlib
import json

import val_ki_functions as VAL
import mod_utilities as MU

MODULES = "not set"
SCHEMAS = "not set"
REPORTS = "not set"
CONFIG_FILE = "C:\\config\\config.json"
APPVERSION = "\nModule Library Validation CLI Version 1.0.0.20200901\n"


def get_config(CONFIG_FILE):
    '''With a config file, get the path, check it, and return the contents..'''
    path = pathlib.Path(CONFIG_FILE)
    if path.exists():
        with open(CONFIG_FILE) as fh:
            loaded_config = json.load(fh)
            print(loaded_config)
        try:
            global MODULES
            MODULES = loaded_config["library"]
            global SCHEMAS
            SCHEMAS = loaded_config["schemas"]
            global REPORTS
            REPORTS = loaded_config["reports"]
        except Exception as e:
            print("Error trying to access config file. {}".format(e))
        return "Config file loaded."
    else:
        return "Cannot find the configuration file. Place the file on your machine at `c:\config\config.json`."


def validate_repo():
    '''
        Validate includes in the repo. (Main Logic for repo parsing)
    '''
    global MODULES
    global SCHEMAS
    global REPORTS

    get_config(CONFIG_FILE)

    include_paths = MU.get_files(MODULES, "md")
    schema_paths = VAL.get_schemas(SCHEMAS)
    schema_set = set(schema_paths.keys())
    report = []
    report.append(["issueid", "validation status", "path", "error"])
    validatation_state = True
    for p in include_paths:
        split_path = p.split("\\")[-1].split("-")
        path_slug = "{}-{}".format(split_path[0],split_path[1])
        slug_index = len(path_slug)
        if path_slug in schema_set:
            in_body = MU.get_textfromMD(p)
            valid_id = p.split("\\")[-1][:-3]
            print("Validating module {} for {}".format(path_slug, valid_id[slug_index:]))
            try:
                if VAL.validate_base_file(in_body):
                    body_parse = VAL.parse_module(in_body)
                    v_line = VAL.validate_module_ki(schema_paths[path_slug], body_parse)
                    if v_line["summary"]:
                        report.append([valid_id, v_line["summary"], p, "No error."])
                    else:
                        validatation_state = False
                        fields = list(v_line["details"].keys())
                        for f in fields:
                            error_message = "{}: {}".format(v_line["details"][f][0], f)
                            report.append([valid_id, v_line["summary"], p, error_message ])
                else:
                    report.append([valid_id, False, p, "Not a valid include file."])
                    validatation_state = False
            except Exception as e:
                    report.append([valid_id, False, p, "Not a valid include file. {}".format(e)])
                    validatation_state = False
    MU.write_csv(report, REPORTS + "validation_report_validation.csv")
    print("The repository is valid: {}".format(validatation_state))
    print("The validation report saved to: " + REPORTS + "validation_report_validation.csv")

    return ""


class TagTerminal(cmd.Cmd):
    """Accepts commands via the normal interactive prompt or on the command line."""

    prompt = "> "
    #global MODULES

    def do_librarycheck(self, line):
        '''The main logic of the utility.'''
        
        try:
            path = pathlib.Path(CONFIG_FILE)
            if path.exists():
                validate_repo()
                return False
            else:
                print("Cannot find the config file.")
        except Exception as e:
            print ("There was some trouble.\nError code: {}".format(e))
            return False

    def do_help(self, line):
        '''Type help to get help for the application.'''
        print("Type `librarycheck`.")
        return False


    def do_quit(self, line):
        '''Type quit to exit the application.'''
        return True


    def do_exit(self, line):
        '''Type exit to exit the application.'''
        return True


    def do_EOF(self, line):
        return True


if __name__ == "__main__":
    TagTerminal().cmdloop(APPVERSION)