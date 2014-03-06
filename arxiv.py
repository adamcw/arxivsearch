#!/usr/bin/env python
# coding: utf-8

"""arXiv Search

Usage:
  arxiv.py id <arxiv_id> [--abstract] [--bib | --url | --pdf | --dl]
  arxiv.py search [-q=<query> | --query=<query>] [--author=<author>] [--category=<category>] [--period=<period>] [--limit=<limit>] [--score=<score>] [--abstract] [--bib | --url | --pdf]
  arxiv.py new [--author=<author>] [--category=<category>] [--period=<period>] [--limit=<limit>] [--score=<score>] [--abstract] [--bib | --url | --pdf]
  arxiv.py bib <arxiv_id>
  arxiv.py url <arxiv_id>
  arxiv.py pdf <arxiv_id>
  arxiv.py dl <arxiv_id>

Options:
  arxiv_id                      The ID of an arXiv paper 
  query                         A query string to search arXiv
  url, --url                    Opens the following arXiv id as a URL
  pdf, --pdf                    Opens the following arXiv id as a PDF
  dl, -dl                       Downloads the following arXiv id as PDF
  bib, --bib                    Will print out bibtex entry for each matching result
  --category=<category>         The category to restrict searches to
  --author=<author>             The author to restrict searches to
  --limit=<limit>               The maximum number of results to retrieve
  --score=<score>               The score cutoff for the display of papers [default: 0]
  --period=<period>             The days into the past to retrieve results for  
  --abstract                    Will print out the abstract for each matching result
"""

import os
import time
import urllib2
from docopt import docopt
args = docopt(__doc__, version='arXiv Search v1.0')

from config import *
from score import score
from pyarxiv.arxiv import arXiv

arxiv = arXiv(DEFAULT_CATEGORIES, DEFAULT_LIMIT, INC_ABSTRACT, USE_BIBDESK)

MIRROR = 'jp'

# Retrieve and parse the query from arXiv
if args['<arxiv_id>']:
    r = arxiv.get_id(args['<arxiv_id>'])
else:
    if args['new'] and not args['--period']:
        args['--period'] = 0

    r = arxiv.search(**{
        'query':    args['-q'] or args['--query'],
        'period':   args['--period'],
        'author':   args['--author'], 
        'category': args['--category'],
        'limit':    args['--limit']
    })

# Order articles by default category or not, then by date published
articles = sorted(r['articles'], 
    key=lambda x: (x['primary'] not in DEFAULT_CATEGORIES, x['published']))

# Filter articles that are below the score threshold
articles = [(a, score(a['title'], a['abstract'])) for a in articles]
articles = [(a, s) for (a, s) in articles if s >= int(args['--score'])]

print "Showing: {0} of {1} retrieved results. Total results: {2}".format(
    len(articles), len(r['articles']), r['total_results'])

if USE_BIBDESK:
    from pybibdesk.bibdesk import BibDesk
    bibdesk = BibDesk()
    current_authors = bibdesk.find_authors()

for (i, (a, key_score)) in enumerate(articles):
    # Output BibTeX references (and import into BibDesk if in use)
    if args['--bib'] or args['bib']:
        ref = arxiv.format_bibtex(a)
        print ref

        if USE_BIBDESK:
            bibdesk.import_reference(ref)
            
    # Open arXiv Link
    elif args['url'] or args['--url']:
        os.system("{0} {1}".format(OPEN_SOFTWARE, a['page_link']))

    # Open PDF Link
    elif args['pdf'] or args['--pdf']:
        os.system("{0} {1}".format(OPEN_SOFTWARE, a['pdf_link']))

    elif args['dl'] or args['--dl']:
        if a['pdf_link'][-4:] != ".pdf":
            a['pdf_link'] += ".pdf"

        filename = os.path.basename(a['pdf_link'])
        url = "http://{}.arxiv.org/pdf/{}.pdf".format(MIRROR, a['id'])
        print "Downloading: {} --> {}".format(
            url,
            filename
        )

        f = open(filename, 'w');
        page = urllib2.urlopen(url).read()
        f.write(page)
        f.close()

        if USE_BIBDESK:
            ref = bibdesk.find_arxiv_ref(a['id'])
            if not ref:
                print "Importing reference."
                ref = bibdesk.import_reference(arxiv.format_bibtex(a))
            bibdesk.link_pdf(ref, filename)
        print "Done."

    # Output formatted result
    else:
        mark = " ** " if a['primary'] not in DEFAULT_CATEGORIES else ""

        highlight_auths = False
        if USE_BIBDESK:
            auths = []
            for x in a['authors'].split(" and "):
                if x in current_authors:
                    highlight_auths = True
                    auths.append("\033[1;31m{}\033[0m".format(x))
                    key_score *= 1.1
                else:
                    auths.append(x)
            a['authors'] = " and ".join(auths)

        d = {
            'i':          (i+1),
            'mark':       mark,
            'cate':       a['primary'],
            'score':      round(key_score, 2),
            'date':       time.strftime("%Y-%m-%d", a['published']),
            'arxiv_id':   a['id'],
            'title':      arxiv.clean(a['title']),
            'author':     a['authors'],
        }

        if highlight_auths:
            print OUTPUT_FORMAT_AUTHS.format(**d)
        else:
            print OUTPUT_FORMAT.format(**d)

        if args['--abstract']:
            print "\n", a['abstract'], "\n"
