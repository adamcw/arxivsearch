## Usage ##

    arXiv Search

    Usage:
    arxiv id <arxiv_id> [--abstract] [--bib | --url | --pdf]
    arxiv search <query> [--author=<author>] [--category=<category>] [--period=<period>] [--limit=<limit>] [--score=<score>] [--abstract] [--bib | --url | --pdf]
    arxiv new [--author=<author>] [--category=<category>] [--period=<period>] [--limit=<limit>] [--score=<score>] [--abstract] [--bib | --url | --pdf]
    arxiv bib <arxiv_id>
    arxiv url <arxiv_id>
    arxiv pdf <arxiv_id>

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

