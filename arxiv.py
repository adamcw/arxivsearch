#!/usr/bin/env python
# coding: utf-8

"""arXiv Search

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
"""

import os
import re
import sys
import time
import requests
import feedparser
from docopt import docopt
from datetime import datetime as dt, timedelta as td
    
import pybibtex.bibtex as bibtex
from pybibdesk.bibdesk import BibDesk
from score import score

# Whether or not you use BibDesk to handle your references (will automatically
# export BibTex references into the currently open BibDesk bilbiography)
USE_BIBDESK = True

# Whether or not to include the abstract in exported BibTex references
INC_ABSTRACT = True

# The default categories to search if no other categories are specified
DEFAULT_CATEGORIES = ['quant-ph']

# The number of results to return if no number is specified
DEFAULT_LIMIT = 100

# Named aliases to search for specific time ranges when using --period
YESTERDAY = ["yesterday", "yday", "y"]
LAST_WEEK = ["last week", "lastweek", "lweek", "lw", "w"]
LAST_MONTH = ["last month", "lastmonth", "lmonth", "lm", "m"]

# A Python .format() string representing how results will be formatted
OUTPUT_FORMAT = "{i:<6} {date} ({arxiv_id}) | {score} | {cate} | {mark}{title}{mark}"

args = docopt(__doc__, version='arXiv Search v1.0')
class arXiv:
    '''Utilities for searching and parsing arXiv'''

    def clean(self, string):
        '''Replace all whitespace with a single space'''
        return re.sub(r'\s+', r' ', string).strip()

    def format_date(self, t):
        '''Formats a date for querying arXiv'''
        return t.strftime("%Y%m%d210000")

    def parse_date(self, t):
        '''Parses a date from arXiv'''
        return time.strptime(t, "%Y-%m-%dT%H:%M:%SZ")

    def format_bibtex(self, article):
        '''Format a parsed article into BibTeX'''
        data = {
            'title': bibtex.wrap(self.clean(article['title'])),
            'author': article['authors'],
            'note': "arXiv:{0}".format(article['id']),
        }

        if INC_ABSTRACT:
            data['abstract'] = self.clean(article['abstract'])

        if USE_BIBDESK:
            data['Bdsk-Url-1'] = article['url']

        # Set DOI, if available
        if data.get('doi', False):
            data['doi'] = article['doi']

        # Extend with any reference information that could be parsed
        ref = self.parse_ref(article['journal_ref'])
        if ref:
            data.update(ref)

        # If there is no reference, then use the arXiv data instead
        else:
            data.update({
                'year': article['published'].tm_year,
                'month': article['published'].tm_mon,
                'journal': article['journal_ref'],
            })

        return bibtex.format(data)

    def parse_ref(self, ref):
        '''Terrible, Terrible hacked together way to try and parse common
        journal_ref strings from arXiv entries.'''
        if not ref:
            return False

        ref = ref.strip()
        
        try:
            if ";" in ref:
                parts = ref.split(";")
                refs = [parse_ref(part) for part in parts]
                return refs[0]
        
            if "(" in ref:
                parts1 = ref.split("(")
                parts2 = parts1[1].split(")")
            
                # Get Year
                year = parts2[0].strip()

                if parts2[1]:
                    parts3 = parts1[0].split()
                    
                    # Get the rest
                    journal = " ".join(parts3[:-1]).strip()
                    page = parts2[1].strip()
                    vol = parts3[-1].strip()
                else:
                    if "," in ref:
                        parts3 = parts1[0].split(",")

                        # International Journal of Quantum Information, 8:1-27 (2010)
                        if ":" in ref:
                            parts4 = parts3[1].split(":")
                            
                            # Get the rest 
                            journal = parts3[0]
                            page = parts4[1]
                            vol = parts4[0]
                        else:
                            parts4 = parts3[0].split()
                            
                            # Get the rest
                            journal = " ".join(parts4[:-1]).strip()
                            page = parts3[1].strip()
                            vol = parts4[-1].strip()
                    
                if journal and page and year and vol:
                    return {
                        'journal': journal,
                        'pages': page,
                        'year': year,
                        'volume': vol,
                    }

            if ":" in ref:
                parts = ref.split(":")

                info = parts[1].split(",")
                
                # Get info
                journal = parts[0].strip()
                page = info[0].strip()
                year = info[1].strip()

                if journal and page and year:
                    return {
                        'journal': journal,
                        'pages': page,
                        'year': year,
                        'volume': '',
                    }
        except:
            return False

        return False

    def query(self, params):
        '''Executes a query against the arXiv API'''

        r = requests.get("http://export.arxiv.org/api/query", params=params)
        return self.parse(r.text.encode('utf8'))      

    def get_id(self, aid):
        '''Queries arXiv for a specific ID'''

        return self.query({
            'id_list': aid,
        })

    def search(self, period=None, query='', author=None, category=None, start=0, limit=None):
        '''Searches arXiv based on a number of provided criteria'''
        params = {}
        q = []

        # Set the default categories
        for cat in DEFAULT_CATEGORIES:
            q.append("cat:{0}".format(cat))

        # Starting point of search results
        params['start'] = start

        # Maximum number of search results to return
        params['max_results'] = limit if limit else DEFAULT_LIMIT

        if query:
            q.append(query)
        
        if author:
            q.append("au:{0}".format(author))

        if category:
            q.append("cat:{0}".format(category))

        if query == None and not period:
            period = 0

        if period != None:
            period = str(period).lower()
            if period in YESTERDAY:
                period = 1
            elif period in LAST_WEEK:
                period = 7
            elif period in LAST_MONTH:
                period = 30
            
            start_offset = 2 + int(period)
            end_offset = 1

            start_t = self.format_date(dt.now() - td(days=start_offset))
            end_t = self.format_date(dt.now() - td(days=end_offset))

            q.append("submittedDate:[{0} TO {1}]".format(start_t, end_t))
        
        # Build the search query
        params['search_query'] = " AND ".join(q)

        print "Search:", params['search_query']

        return self.query(params)

    def parse(self, xml):
        '''Parses the return XML from the arXiv API'''
        feed = feedparser.parse(xml)

        # Parse Search Results
        arxiv = {
            'articles':         [],
            'title':            feed.feed.title,
            'updated':          feed.feed.updated,
            'start_index':      feed.feed.opensearch_startindex,
            'total_results':    feed.feed.opensearch_totalresults,
            'items_per_page':   feed.feed.opensearch_itemsperpage,
        }

        # Parse Articles
        for entry in feed.entries:
            a_id = entry.id.split('/abs/')[-1]
            default_ref = "arXiv:{0}".format(a_id)

            authors = [author.get('name', '') for author in entry.get('authors', [])]
            authors = ' and '.join(authors)

            categories = ', '.join([t['term'] for t in entry.tags])

            article = {
                'id': a_id,
                'categories':       categories,
                'authors':          authors.encode('utf8'),
                'title':            entry.title.encode('utf8'),
                'abstract':         entry.summary.encode('utf8'),
                'comment':          entry.get('arxiv_comment', ''),
                'updated':          self.parse_date(entry.updated),
                'published':        self.parse_date(entry.published),
                'primary':          entry.arxiv_primary_category['term'],
                'journal_ref':      entry.get('arxiv_journal_ref', default_ref),
            }

            # Parse any links available for the article (Page, PDF, DOI)
            for link in entry.links:
                if link.rel == 'alternate':
                    article['page_link'] = link.href
                elif link.title == 'pdf':
                    article['pdf_link'] = link.href
                elif link.title == 'doi':
                    article['doi'] = link.href

            # The URL should be DOI preferentially, else the arXiv link.
            article['url'] = article.get('doi', article.get('page_link', '')) 

            arxiv['articles'].append(article)

        return arxiv




arxiv = arXiv()

# Retreive and parse the query from arxiv

if args['<arxiv_id>']:
    r = arxiv.get_id(args['<arxiv_id>'])
else:
    r = arxiv.search(**{
        'query':    args['<query>'],
        'period':   args['--period'],
        'author':   args['--author'], 
        'category': args['--category'],
        'limit':  args['--limit']
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
    bibdesk = BibDesk()

for (i, (a, key_score)) in enumerate(articles):
    # Output BibTeX references (and import into BibDesk if in use)
    if args['--bib'] or args['bib']:
        ref = arxiv.format_bibtex(a)
        print ref

        if USE_BIBDESK:
            bibdesk.import_reference(ref)
            
    # Open arXiv Link
    elif args['url'] or args['--url']:
        os.system("open {0}".format(a['page_link']))

    # Open PDF Link
    elif args['pdf'] or args['--pdf']:
        os.system("open {0}".format(a['pdf_link']))

    # Output formatted result
    else:
        mark = " ** " if a['primary'] not in DEFAULT_CATEGORIES else ""
        print OUTPUT_FORMAT.format(**{
            'i':          i,
            'mark':       mark,
            'cate':       a['primary'],
            'score':      key_score,
            'date':       time.strftime("%Y-%m-%d", a['published']),
            'arxiv_id':   a['id'],
            'title':      arxiv.clean(a['title']),
            'author':     a['authors'],
        })

        if args['--abstract']:
            print "\n", a['abstract'], "\n"
