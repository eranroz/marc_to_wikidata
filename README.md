This project aims to enrich Wikidata entities with data from libraries based on MARC standard.

# What is it?
The National Library of Israel (NLI) publicly shares a huge thesaurus about people, places and institutes.
The thesaurus is given in [MARC standard](https://en.wikipedia.org/wiki/MARC_standards) which
 is common in many libraries.

In this POC project we map MARC attributes to Wikidata properties to enrich Wikidata from data of libraries.

# Data
marcxml_example.xml is small subset of MARC records from National Library of Israel that you are free to use,
and should be useful for development.

For production use you would like to get MARC data with many more records.
Ask your library (GLAM GLAM GLAM) or find a public web MARC resource (with permission to use!).


# TODOs
* [MARC specification in the Library of Congress](https://www.loc.gov/marc/marcdocz.html)
* Should we use some MARC package such as the nice [pymarc](https://github.com/edsu/pymarc) ?
* [Wikidata properties to MARC mapping](https://docs.google.com/spreadsheets/d/1lXxIe1vYFbUaTGUWTFi7Gh9zZzUcKZNSjPCk65qgm2A/edit#gid=0)
