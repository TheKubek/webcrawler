import sys
import requests
import re
from bs4 import BeautifulSoup


# len is O(1) so there is no need carrying a count parameter
# due to the extra links parameter, the program is able to
# always fetch exactly 100 links, even with the recursion
#
# comparator '>=' instead of '==' used in case something
# unexpected happens
def crawl(url, links, max_links=100):
    # ignore inaccessible links
    try:
        webpage = requests.request(method='GET', url=url).text
    except requests.exceptions.SSLError:
        # KeyError should never occur, but good practice to catch it anyways
        try:
            links.remove(url)
        except KeyError:
            pass
        return links

    soup = BeautifulSoup(webpage, 'lxml')
    new_links = set()
    
    # get the http and https links that are not already in the 'links' set
    for link in set(map(lambda x: x.get('href'), soup.findAll('a', 
        attrs={'href': re.compile('^https?://')}))).difference(links):

        links.add(link)
        new_links.add(link)
        if len(links) >= max_links:
            return links

    # get links from the links (recursive step)
    for link in new_links:
        # print(len(links))
        links = crawl(link, links)
        if len(links) >= max_links:
            return links

    return links


def main():
    url = sys.argv[1]
    result = crawl(url, set([url]))

    for link in result: 
        print(link) 

    print(len(result))


if __name__ == '__main__':
    main()
