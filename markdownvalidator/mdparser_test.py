'''
Unit tests using pytest for mdparser.py (MDParser class).
'''
import markdownvalidator.mdparser as PA

single_file = r"C:\git\mb\markdown-validator\markdownvalidator\testdata\azure-stack-overview.md"


def test_class_get_raw_body():
    testparser = PA.MDParser()
    get_body = testparser.get_raw_body(single_file)
    check_val = "---\ntitle: Azure Stack Hub overview \ndescription: An overview of what Azure Stack Hub is and how it lets you run Azure services in your datacenter."
    assert get_body[:147] == check_val


def test_class_butcher():
    testparser = PA.MDParser()
    testparser.get_raw_body(single_file)
    get_parts = testparser.butcher()
    size_it = len(get_parts)
    assert size_it == 2


def test_class_process_meta():
    testparser = PA.MDParser()
    testparser.get_raw_body(single_file)
    meta_dict = testparser.process_meta()
    assert meta_dict["Keyword"] == "use azure stack"


def test_class_process_body():
    testparser = PA.MDParser()
    testparser.get_raw_body(single_file)
    html_body = testparser.process_body()
    compare_it = "<h1>Azure Stack Hub overview</h1>"
    assert html_body[:33] == compare_it