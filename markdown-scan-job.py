
import csv
import mod_utilities as MU
import markdown_scanner as MS

def main():
    ''' '''
    rules = input("Add rules (path) > ")
    repo = input("Repo location (dir) > ")
    output = input("reports location (dir) > ")
    files = MU.get_files(repo)
    print(files)

    report = [["ID", "Path", "Score"]]
    jsondump = {}
    count = 0

    for f in files:
        print(f)
        try:
            check = MS.MDScanner()
            assess = check.validate_with_rules(rules, f)
            row = []
            count += 1
            row.append(count)
            row.append(f)
            row.append(assess["score"])
            report.append(row)
            jsondump[count] = assess
        except:
            print("Error!")

    csvout = output + "\\report.csv"
    jsonout = output + "\\report.json"
    MU.write_csv(report, csvout)
    MU.write_text(str(jsondump), jsonout)
    input("Done. Hit a key.")


if __name__ == "__main__":
    main()

