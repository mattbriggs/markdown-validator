# Validation queries specification

Matt Briggs, 10/6/2021

This document specifies the document interface for the query rules.

The ruleset document will be run when a document is validated for a specific content type. The content type is a specific document schema that has a specific purpose. The ruleset describes the required and recommended features of a document type. The ruleset will allow the system to programmatically check a markdown document and validate that conformance to the rules, and if not valid, produce a message for the user on how the markdown file can be fixed.

## About the code

This specification document is more of the design. You can review the stab at implementation here.

The code is a set of Python scripts for validating markdown files used in static site
builders such as [docFX](https://dotnet.github.io/docfx/) and 
[Hugo](https://gohugo.io/).

You can read the Docs at: 
[https://blue-forest-0a98c3610.azurestaticapps.net/](https://blue-forest-0a98c3610.azurestaticapps.net/)

## The ruleset JSON document

The ruleset is a JSON array. Each rule is defined with ten attributes. The rules are set of declarative assertions. They are broken into types. Metadata assertions and assertions about the body of the document. An executed rule requires as input the rule JSON declaration and a markdown file. The rule returns two values: True or False for the validity of the rule and an object found by the query.

For example, if a rule that checks for the existence of a H1 runs the query \"/html/body/h1\" for a markdown document. The rule will return both True and the string for the header.

You can find an example here: [validationrule-examplev2.json](./validationrule-example-V2.json)

## Rendering and disambiguating the markdown

Markdown is an ambiguous format. For validation parsing, the validator will render markdown in a semantically unambiguous format. Since the target is a web site, the markdown will be rendered as XHTML.

The rules will run on a markdown document that will be rendered into two parts:

**Part 1**: Is a JSON array of the metadata.

**Part2:** Is an XHTML document that has been modified from the classic HTML DOM to reflect the table of contents organization of the document. A typical DOM is wrapped in HTML and then contains a header and body section. The body section contains a list of nodes that are children of the body node. In the validation XHTML schema, the body nodes reflect the outline levels of the document. That is an H3 is a child of a H2 and the H2 is a child of an H1.

## Strategy for validation

A document is divided into two parts with two different modes of running a check. A validation will run a rule using an assert operation. This means it will find a value and then check if the operation is true. For example, it might check if the metadata value is ms.author == "mabrigg". This will be true or false.

**Part 1: metadata**. This will render the metadata as a set of key value pairs. Each key can be interrogated both for its existence and for the values.[^1] For example, you can check if key: ms.author exists. And you can check the value of ms.author.

**Part 2: XHTML (with outline)**. The body of the document will be rendered as an XML tree that reflects the outline of the document. The nodes of the tree can be navigated and extracted using an XPath query. For example, you can check if the title of the document (the H1) is "A specific string" with an XPath query: /html/body/H1 == "A specific string".

Each query returns two values. It returns a bool (true/false) and the element that is found. For example, ms.author would return true, and the value of the key.

Queries can be concatenated by a reference to the query id attribute. This allows queries to build off of each other in a chain. For instance, we can check that the title metadata attribute equals the H1. Or you can grab a section of the document with one query and then run checks on it in another query.

Each rule contains the following attributes:

-   **Name**: a string to identify the rule.

-   **Type**: if this is a header (metadata query) or a body (xpath query)

-   **ID**: A unique identifier for the rule.

-   **Query**: the metadata or the xpath query. A query can reference a previous query. The query returns a value as either a string, a list of strings, or an XML collection of child/parent nodes.

-   **Filter**: Query filters reduce the amount of data retrieved from the query.

-   **Flag**: Selects the expression type for the operation. For instance, regex runs a regex check on the value(s) returned by the query.

-   **Operation**: Numerical operations are basic mathematical operations like addition, subtraction, multiplication, and division as well as other operations that are denoted by symbols like 'less than', 'greater than', 'equal to', 'not equal to'.

-   **Value**: The expected value.

-   **Level**: The level of the validation. Required or recommended. A required value that fails would fail the overall validation.

-   **Mitigation**: A text (string) explanation of how to fix the issue. The mitigation may require a mechanism to pass the identified value with the expected value and a line number where the validation fail occurred.

## Rule set syntax

```json
{
    "name": "H1 must begin with tutorial",
"type:" : "body",
    "id": "29",
    "query": " /html/body/h1",
    "filter": "/text",
    "flag": "",
    "operation": "regex",
    "value": "^Tutorial",
    "level": "Required",
    "mitigation": "The H3 headings aren't numbered"
},
{
    "name": "H1 must begin with tutorial",
"body",
    "id": "29",
    "query": "{29}",
    "filter": "",
    "flag": "text",
    "operation": "regex",
    "value": "Azure Monitor",
    "level": "Required",
    "mitigation": "The H3 headings aren't numbered"
},

```


### Attribute definitions

| Field | Datatype | Required | Description |
|---|---|---|---|
| Name | string  | Yes | A unique string and name for the   rule. |
| ID | number | Yes and must be unique. | The alias for the rule that used when constructing the workflow. The ID   must be a number and must be unique in the context of a document. |
| Query | string | Yes | Header: The key for the metadata   value.<br>Body: This is the xpath query that returns a result from the   document.<br><br>Body rules also support references to other   rules. For example: {29} as the query would run the new rule on the result of   rule ID 29. |
| Filter | string | No | Contains a regex. |
| Flag | Enumeration:<br>check<br>value<br>date<br>regex<br>type<br>all | Yes | Selects the modes of the check.<br><br>For header:<br>- **Check** will check if the value is present. Used for checking for the presence of a key in the metadata value (header). For a body query, will check against the node type in the document object model.<br>- **Value** will evaluate the value of the metadata with a given value and operation.<br>- **Date** will check a metadata value with a given date. Note, you can use "now" to indicate the current time.<br>- **Regex** will allow a regex pattern and check the value.<br>- **Type** will check the datatype of the item. <br>- **Count** will return the number of items found in the query. <br>**Text** will return the text of the first item returned.<br>- **All** will return the entire text of the page. |
| Operation  | Enumeration (See list below) |  | Perform an operation of the query and the value. |
| Value | string | Yes | The value used for the comparison   in the assertion.<br><br>Supports a ref to another rule. This   will compare the return of the referenced rule to the value. For example, {1} |
| Level | Enumeration:<br>Required<br>Suggested<br> | Required | This is the level of the validation. All required validation rules must   pass for validation to pass. |
| Fix | string | Yes | This is the message returned to   the user when they run validation and a validation error is triggered. |
| Comment | String | Yes |  |

## Operations

The following operations are supported and will return a tuple of (Boolean, Value).

| Operand | Name | Return | Description | Example |
|---|---|---|---|---|
| == | equals | Boolean | Will   compare to values. |  |
| != | Not equal | Boolean | Will   compare to values. |  |
| <  | Less than | Boolean | Will   compare to values. |  |
| >  | Greater than | Boolean | Will   compare to values. |  |
| [: | Starts with | Boolean | Will check if the string occurs at the start of the item. | /html/body/h2[1] text [: Why use Azure Stack Hub? |
| [] | Contains | Boolean | Will   check if the string can be found within the item. | /html/body/h2[1]   text [] Why use Azure Stack Hub? |
| :] | End with | Boolean | Will check if the string occurs at the end of the item. | /html/body/h2[1] text :] Why use Azure Stack Hub? |
| p0 | Part of speech | Boolean | Will   check at the index the part of speech of the word. | /html/body/h2[1]   text [1 verb |
| l | Character length | Boolean | Will check if less than the length   given | /html/body/h2[1] text [- 120 |
| s | Sentence length | Boolean | Will check if less than the   length given | /html/body/h2[1]   text -] 6 |
| regex | regex | Boolean | Will check if the items matches   a  pattern. | %%/%%/%% |
## Parts of Speech

Alphabetical list of part-of-speech tags used in the [Penn Treebank Project](https://www.seas.upenn.edu/~pdtb/).

| Token | Part   of Speech |
|---|---|
| WRB | Wh-adverb |
| WP$ | Possessive wh-pronoun |
| WDT | Wh-determiner |
| VBZ | Verb, 3rd person singular present |
| VBP | Verb, non-3rd person singular present |
| VBN | Verb, past participle |
| VBG | Verb, gerund or present participle |
| VBD | Verb, past tense |
| SYM | Symbol |
| RBS | Adverb, superlative |
| RBR | Adverb, comparative |
| PRP | Personal pronoun |
| POS | Possessive ending |
| PDT | Predeterminer |
| NNS | Noun, plural |
| NNP | Proper noun, singular |
| JJS | Adjective, superlative |
| JJR | Adjective, comparative |
| WP | Wh-pronoun |
| VB | Verb, base form |
| UH | Interjection |
| TO | to |
| RP | Particle |
| RB | Adverb |
| NN | Noun, singular or mass |
| MD | Modal |
| LS | List item marker |
| JJ | Adjective |
| IN | Preposition or subordinating conjunction |
| FW | Foreign word |
| EX | Existential there |
| DT | Determiner |
| CD | Cardinal number |
| CC | Coordinating conjunction |
| PRP$ | Possessive pronoun |
| NNPS | Proper noun, plural |

## Node types in the document object model

Alphabetical list of nodes types in the document object model.

[^1]: Metadata can be programmatically checked in a few ways. 1. The metadata section can be rendered as JSON. This JSON can than have JSON Queries run against it and the return value assessed. 2. The metadata section can be converted into a dictionary and then the dictionary compared with a validation dictionary. An implementation of this is the Python library [Cerebus](https://docs.python-cerberus.org/en/stable/index.html). 3. In this case, we can simply convert the metadata section into a set of key value pairs. Depending on the datatype of each value we can run operations to determine if is the expected value.

Another method of schema-based validation has suggested itself and that is using [JSON schema validation](https://json-schema.org/).
