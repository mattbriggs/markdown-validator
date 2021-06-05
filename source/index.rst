.. markdown validator documentation master file, created by
   sphinx-quickstart on Fri Jun  4 12:25:24 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the Markdown Doc Validator documentation.
==============================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   test
   modules

Validation queries are declarative statements using a limited number of 
keywords, operands, and tokens that correspond to markdown elements. The 
intent of the query is to use a minimal syntax that is expressive enough to 
capture assertions about the structural properties of a markdown document. 

The validation query contains two modalities.
* Mode one is to assess the key/value pairs in the metadata section.
* Mode two uses XPATH to interrogate the document object model (DOM). The 
  Document Object Model (DOM) is a cross-platform and language-independent 
  interface that treats an XML or HTML document as a tree structure wherein each 
  node is an object representing a part of the document. XPATH is a declarative 
  language used to query XML trees. In this case, these statements are used to 
  query an XHTML rendered markdown structure. 

You can find the code at https://github.com/mattbriggs/markdown-validator.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
