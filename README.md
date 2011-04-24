In the data folder...

random.txt
==========
* Average activity level over all authors. Average activity level is given by number of collaborations an author makes per year. Calculated by summing the total number of collaborations per author, then dividing by the number of "active" years an author has (first year of collaboration subtracted from 2003)

/graphs
=======
* activity_distribution is the distribution of # of collaborations per author over the whole dataset
* citation_distribution is the distribution of # of citations per paper over the whole dataset
* new_authors_per_year shows the # of new authors that appear each year
* papers_per_author shows distribution # of papers each author wrote over the whole dataset (includes papers written without collaborators)
* s_activity_level looks at the number of collaborations that authors with a certain range of total collaborations have each year
* s_citation_level looks at the distribution of # of citations a paper receives per year from the year it got published (for various ranges of # of citations received)

/parsed
=======
* papers_citations_? is the dictionary of years in which a paper got cited
* papers_cpapers_? is the list of papers that a specific paper cited
* citations_? is the number of citations a specific paper got