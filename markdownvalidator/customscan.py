
import sys
import mod_utilities as MU
import customscannumberedlines as CU

def main():
    ''' '''

    #
    #  repopath = sys.argv[1]
    # output = sys.argv[2]

    files = MU.get_files(r"C:\git\ms\azure-docs-pr\articles")

    report = [["ID", "Path", "Score"]]
    count = 0

    for f in files:
        print(f)
        try:
            check = CU.CountNoLines()
            assess = check.tally(f)
            row = []
            count += 1
            row.append(count)
            row.append(f)
            row.append(assess)
            report.append(row)
        except Exception as e:
            print("Error: {}".format(e))

    csvout = "C:\\data\\202206181120-scan" + "\\report.csv"
    MU.write_csv(report, csvout)
    input("Done. Hit a key.")


if __name__ == "__main__":
    main()

