import devrelutilities as DV
import mdparser as PA

def filer_paths(list_of_files):
    keep_list = []
    for i in list_of_files:
        for j in target:
            if j in i:
                keep_list.append(i)
    return keep_list


# vals
list_of_files = DV.get_files(r"C:\git\ms\azure-stack-docs-pr\azure-stack")
single_file = r"C:\git\ms\azure-stack-docs-pr\azure-stack\operator\azure-stack-overview.md"
target = ["azure-stack\\user", "azure-stack\\operator", "azure-stack\\asdk"]

file_g = PA.MDParser(single_file)
print(file_g.parse_file())