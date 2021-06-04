'''
Unit tests using pytest for mdhandler.py (MDHandler class).
'''
import mdhandler as HA
import mdparser as PA

single_file = r"C:\git\ms\Azure-Stack-Hub-Doc-Tools\tools-development\testdata\azure-stack-overview.md"
handler = HA.MDHandler()
page = handler.get_page(single_file)


def test_process_xpath():
    '''Test to check.'''
    query = "/html/body/h2[1]"
    x = handler.process_xpath(page.html, query, "text")
    assert x == "Why use Azure Stack Hub?"


def testprocess_metadata():
    '''Test to check.'''
    value1 = "ms.author"
    x = handler.process_metadata(page.metadata, value1)

    assert x == 'patricka'


def test_operate_equal():
    '''Test to check.'''
    in_string = "dog"
    in_value = "dog"
    x = handler.operate_equal(in_string, in_value)
    assert x == True


def test_operate_greater():
    '''Test to check.'''
    in_string = "3"
    in_value = "2"
    x = handler.operate_greater(in_string, in_value)
    assert x == True


def test_operate_less():
    '''Test to check.'''
    in_string = "2"
    in_value = "3"
    x = handler.operate_less(in_string, in_value)
    assert x == True


def test_operate_not():
    '''Test to check.'''
    in_string = "3"
    in_value = "2"
    x = handler.operate_not(in_string, in_value)
    assert x == True


def test_operate_contains():
    in_string = "This is the monkey."
    test_string = "is the"
    x = handler.operate_contains(in_string, test_string)
    assert x == True


def operate_starts():
    in_string = "This is the monkey."
    test_string = "This is"
    x= handler.operate_ends(in_string, test_string)
    assert x == True

def operate_ends():
    in_string = "This is the monkey."
    test_string = "monkey."
    x = handler.operate_starts(in_string, test_string)
    assert x == True


def test_eval_query():
    '''Test to check.'''
    query = "/html/body/h2[1]"
    in_value = "Why use Azure Stack Hub?"
    x = handler.eval_query(page.html, query, "text", "==", in_value)
    assert x == True


def test_eval_ask():
    '''Test to check.'''
    keyword = "ms.author"
    in_value = "patricka"
    x = handler.eval_ask(page.metadata, keyword, "==", in_value)
    assert x == True


def test_get_page():
    '''Test to check.'''
    x = handler.get_page(single_file )
    assert x.raw[:10] == "---\ntitle:"


def test_make_html():
    '''Test to check.'''
    handler.make_html(page.html, "/testdata/body.html")
    assert 1 == 1


def test_make_json():
    '''Test to check.'''
    handler.make_json(page,  "/testdata/meta.json")
    assert 1 == 1


def test_eval_meta():
    '''Test to check.'''
    value1 = "ms.author"
    x = handler.eval_meta(page.metadata, value1)
    assert x == "patricka"


def test_get_rules():
    '''Test to check.'''
    RULE = ""
    handler.get_rules(RULE)
    assert 1 == 1