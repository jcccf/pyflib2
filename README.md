Usage
=====
* Download and extract cit-HepTh.txt.gz and cit-HepTh-abstracts.tar.gz obtained from http://snap.stanford.edu/data/cit-HepTh.html into the /data folder
* To generate all required files,
* Run authorship_parse.py
* Run citations_parse.py

In the lib folder...
====================
Authorship
----------
* authorship_parse.py generates the authorship graph from the abstract files
* authorship_properties.py calculates some properties of the actual authorship graph
* authorship_properties2.py calculates the macro properties of the actual authorship graph
* authorship_properties2_compare.py compares the macro properties of our growth model with the actual graph
* authorship_simulate.py runs our citation network growth model

Citations
---------
* citations_parse.py extracts useful data out of the citation graph
* citations_properties.py calculates properties of the actual citation graph

In the data folder...
=====================
random.txt
----------
* Average activity level over all authors. Average activity level is given by number of collaborations an author makes per year. Calculated by summing the total number of collaborations per author, then dividing by the number of "active" years an author has (first year of collaboration subtracted from 2003)

/graphs
-------
* activity_distribution is the distribution of # of collaborations per author over the whole dataset
* citation_distribution is the distribution of # of citations per paper over the whole dataset
* new_authors_per_year shows the # of new authors that appear each year
* papers_per_author shows distribution # of papers each author wrote over the whole dataset (includes papers written without collaborators)
* s_activity_level looks at the number of collaborations that authors with a certain range of total collaborations have each year
* s_citation_level looks at the distribution of # of citations a paper receives per year from the year it got published (for various ranges of # of citations received)

/parsed
-------
* papers_citations? is the dictionary of years in which a paper got cited
* papers_cpapers? is the list of papers that a specific paper cited
* citations? is the number of citations a specific paper got

Prefixes
--------
* g = Gamma Distribution with a = 3, b = 2
* dg = Gamma Distribution with a = degree of node, b = 2
* drg = Gamma Distribution with a = sqrt(degree of node), b = 2
