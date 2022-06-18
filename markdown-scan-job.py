
import sys
import yaml
import mod_utilities as MU
import markdown_scanner as MS

def main():
    ''' '''

    if sys.argv[1]:
        jobfile = sys.argv[[1]]
    else:
        print("Need a rules files.")
        exit

    with open (jobfile, "r") as stream:
        config = yaml.load(stream, Loader=yaml.CLoader)

    files = MU.get_files(config["repo"])

    report = [["ID", "Path", "Score"]]
    jsondump = {}
    count = 0

    for f in files:
        print(f)
        try:
            check = MS.MDScanner()
            assess = check.validate_with_rules(config["rules"], f)
            row = []
            count += 1
            row.append(count)
            row.append(f)
            row.append(assess["score"])
            report.append(row)
            jsondump[count] = assess
        except Exception as e:
            print("Error: {}".format(e))

    csvout = config["outputfolder"] + "\\report.csv"
    jsonout = config["outputfolder"] + "\\report.json"
    MU.write_csv(report, csvout)
    MU.write_text(str(jsondump), jsonout)
    input("Done. Hit a key.")


if __name__ == "__main__":
    main()

