#!/usr/bin/env python3
__author__ = 'otakucode'

import argparse
import sys
from urllib import parse

from bs4 import BeautifulSoup
import requests


def get_title(search_type, search_title):
    search_encoded = parse.quote(search_title)
    page = requests.get('http://www.canistream.it/search/{0}/{1}'.format(search_type, search_encoded),
                        headers={'referer' : 'http://www.canistream.it/',
                                 'Content-Type' : 'application/x-www-form-urlencoded',
                                 'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0'})

    soup = BeautifulSoup(page.content)
    searchresult = soup.find(class_="search-result row")

    if searchresult is None:
        return None

    movie_id = searchresult['rel']
    proper_title = searchresult['data1']

    return (movie_id, proper_title)


def query_availability(movie_id, availability_type):
    results = requests.get('http://www.canistream.it/services/query',
                           headers={'referer' : 'http://www.canistream.it/',
                                    'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0'},
                           params={'movieId' : movie_id,
                                   'attributes' : 1,
                                   'mediaType' : availability_type})

    return results.json()


def get_availability(movie_id, verbose, omits):
    all_queries = ['Streaming', 'Rental', 'Purchase', 'xfinity']
    queries = []
    for query in all_queries:
        if omits is None or query not in omits:
            queries.append(query)

    availability = ''

    firstone = True
    for q in queries:

        result = query_availability(movie_id, q.lower())

        if result:
            if verbose:
                availability += "\n" + q + ": "
            else:
                if firstone == True:
                    firstone = False
                else:
                    availability += ', '

            services = []
            for key in result.keys():
                services.append(result[key]['friendlyName'])

                if key == 'apple_itunes_purchase':
                    # Fix bug in canistream.it which lists wrong friendlyName for iTunes purchases
                    services[-1] = 'Apple iTunes Purchase'
                if result[key]['price'] != 0:
                    services[-1] += ' (${0})'.format(result[key]['price'])

            availability += ', '.join(services)

    return availability



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search www.canistream.it for movie availability.')
    parser.add_argument('movie', metavar='Title', type=str, help='title to search for')
    #parser.add_argument('--tv', help='search for TV show instead of movie')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--no-streaming', action='append_const', const='streaming', dest='omits', help='do not search for streaming availability')
    parser.add_argument('--no-rental', action='append_const', const='rental', dest='omits', help='do not search for rental availability')
    parser.add_argument('--no-purchase', action='append_const', const='purchase', dest='omits', help='do not search for purchase availability')
    parser.add_argument('--no-xfinity', action='append_const', const='xfinity', dest='omits', help='do not search for xfinity availability')

    args = parser.parse_args()

    print("Searching...", end='')
    sys.stdout.flush()
    movie = get_title('movie', args.movie)
    if movie is None:
        print("\rNo titles matching '{0}' found.".format(args.movie))
        sys.exit()

    (movie_id, proper_title) = movie
    results = get_availability(movie_id, args.verbose, args.omits)

    if len(results) == 0:
        print('\r"{0}" is not currently available.'.format(proper_title))
    else:
        print('\r"{0}" is available via: '.format(proper_title), end='')
        print(results)

