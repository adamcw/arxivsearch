## Tested ##

Only tested on OSX 10.8 with the following dependent packages:

* requests v0.14.1
* feedparser v5.1.3
* docopt v0.6.1

## Dependencies ##

    pip install requests
    pip install feedparser
    pip install docopt

## Installation ##

* Update the options at the top of arxiv.py to suit your preferences (See: Options)
* Update score.py to include keyword, weight values for your own preferences

## Usage ##

    arXiv Search

    Usage:
    arxiv.py id <arxiv_id> [--abstract] [--bib | --url | --pdf]
    arxiv.py search <query> [--author=<author>] [--category=<category>] [--period=<period>] [--limit=<limit>] [--score=<score>] [--abstract] [--bib | --url | --pdf]
    arxiv.py new [--author=<author>] [--category=<category>] [--period=<period>] [--limit=<limit>] [--score=<score>] [--abstract] [--bib | --url | --pdf]
    arxiv.py bib <arxiv_id>
    arxiv.py url <arxiv_id>
    arxiv.py pdf <arxiv_id>

    Options:
    arxiv_id                      The ID of an arXiv paper 
    query                         A query string to search arXiv
    url, --url                    Opens the following arXiv id as a URL
    pdf, --pdf                    Opens the following arXiv id as a PDF
    bib, --bib                    Will print out bibtex entry for each matching result
    --category=<category>         The category to restrict searches to
    --author=<author>             The author to restrict searches to
    --limit=<limit>               The maximum number of results to retrieve
    --score=<score>               The score cutoff for the display of papers [default: 0]
    --period=<period>             The days into the past to retrieve results for 
    --abstract                    Will print out the abstract for each matching result

## Options (arxiv.py) ##

    # Whether or not you use BibDesk to handle your references (will automatically
    # export BibTex references into the currently open BibDesk bilbiography)
    USE_BIBDESK = True

    # The default categories to search if no other categories are specified
    DEFAULT_CATEGORIES = ['quant-ph']

    # A Python .format() string representing how results will be formatted
    OUTPUT_FORMAT = "{i:<6} {date} ({arxiv_id}) | {score} | {cate} | {mark}{title}{mark}"

## Search Options (arxivsearch.py) ##

    # Whether or not to include the abstract in exported BibTex references
    INC_ABSTRACT = True

    # The number of results to return if no number is specified
    DEFAULT_LIMIT = 100

    # Named aliases to search for specific time ranges when using --period
    YESTERDAY = ["yesterday", "yday", "y"]
    LAST_WEEK = ["last week", "lastweek", "lweek", "lw", "w"]
    LAST_MONTH = ["last month", "lastmonth", "lmonth", "lm", "m"]

## Future Prospects ##

* Automatically generate scoring keywords and weights based on a provided .bib file of references. 
* Improve and de-hackify the arXiv journal_ref parsing
