import re
from urllib import parse
#from urllib.parse import urlparse
#from urllib.parse import urldefrag
#from urllib.parse import urlsplit
#from urllib.parse import urljoin
#from urllib import parse
from urllib import robotparser

from bs4 import BeautifulSoup, SoupStrainer
from lxml import html
from lxml import etree, objectify
import requests
import os
import sys

DOMAINS = ['https://www.ics.uci.edu', 'https://www.cs.uci.edu', 'https://www.informatics.uci.edu', 'https://www.stat.uci.edu', 'https://today.uci.edu/department/information_computer_sciences/']

def scraper(url, resp):
    links = extract_next_links(url, resp)
    validLinks = set([link for link in links if is_valid(link)])
    print(validLinks)
    #finalLinks = Visited(validLinks)
    #print(finalLinks)
    while True:
        next = input("Press a next, e quit ")
        if next == 'a':
            break
        elif next == 'e':
            sys.exit()
    return list(validLinks)

def extract_next_links(url, resp):
    # Implementation requred.
    # add robots.txt
    # check if valid page
    # defrag links
    #r = requests.get(url, timeout=10)
    #if not r:
    #    return list()
    # check if url responds
    if resp.status == 200:
        print("SUCCESS")
    elif 200 < resp.status < 300: # and resp.status < 300:
        print("Success, but not 200")
        print(resp.status)
    elif resp.status == 404:
        print("FAIL")
        return list()
    elif resp.status in [600, 601, 602, 603, 604, 605, 606]:
        print(resp.status)
        print(resp.error)
        return list()
    else:
        print(resp.status)
        print(resp.error)
        return list()

    if resp.raw_response == None:
        return list()
    if not resp.raw_response.ok:
        return list()
    defrag = parse.urldefrag(url)[0]
    parsedUrl = parse.urlsplit(url, allow_fragments=False)
    base_url = "{0.scheme}://{0.netloc}/".format(parsedUrl)
    print(url)
    print(parsedUrl.netloc)
    print(base_url)

    did_visit = UniqueURLs(defrag)
    # might not need this
    if did_visit:
        print("did visit")
        return list()

    extracted_links = set()

    '''
    rp = robotparser.RobotFileParser()
    print(parsedUrl.scheme, parsedUrl.netloc)
    fullDomain = parsedUrl.scheme + '//' + parsedUrl.netloc
    print(fullDomain)

    #robDom = parse.urljoin(fullDomain, '/robots.txt')
    robDom = fullDomain + '/robots.txt'
    rp.set_url(robDom)
    rp.read()
    if rp.can_fetch("*", url):
        for line in rp.parse()
    else:
        print("Cannot fetch " + url)
    '''

    write_to_file('visitedURLs.txt', defrag.split())
    #visited = open('visitedURLs.txt', 'a+')
    #visited.write(defrag + "\n")
    #visited.close()

    '''
    #testing
    rp = robotparser.RobotFileParser()
    content = resp.raw_response.content
    dom = html.fromstring(content, parser=etree.HTMLParser(remove_comments=True))

    absDom = html.make_links_absolute(defrag, True)
    adom = html.fromstring(absDom, parser=html.HTMLParser(remove_comments=True))
    for element, attribute, link, pos in html.iterlinks(adom):
        print(link)
        if attribute == 'href':
            print("sss")
            print(link)
            print("ddd")
    '''
    #robots = ''
    #rp = robotparser.RobotFileParser()
    content = resp.raw_response.content
    soup = BeautifulSoup(content, 'lxml')
    for link in soup.find_all('a'):
        link_url = link['href']
        if len(link_url) > 200:
            continue
        url = parse.urljoin(base_url, link_url)
        extracted_links.add(url)
    '''
        if robots == '' or base_url not in robots:
            robots = base_url+'robots.txt'
            print(robots)
            rp.set_url(robots)
            rp.read()
        # bare minimum if we even CAN fetch urls.
        if rp.can_fetch("*", link_url):
            print("link added ", link_url)
            extracted_links.add(url)
        #extracted_links.add(url)
    '''
    '''
    robots = ''
    rp = robotparser.RobotFileParser()
    for link in extracted_links:
        newLink = parse.urlsplit(link)
        fullDomain = "{0.scheme}://{0.netloc}/".format(newLink)

        # robDom = parse.urljoin(fullDomain, '/robots.txt')
        # IF a link to another domain exists, check its robots.txt to see if it is a valid link to crawl
        # fetch doesnt seem to work
        if robots == '' or fullDomain not in robots:
            robots = fullDomain+'robots.txt'
            print(robots)
            rp.set_url(robots)
            rp.read()
        if rp.can_fetch("*", link):
            extracted_links.add(link)
        else:
            print("Cannot fetch acc robots.txt")
    #except:
    #    print("Page content unavailable")
    #    print(url)
    '''
    #add html parsing

    #print(is_valid(defrag))
    #return list()
    extracted_links = sorted(list(extracted_links))
    l = parse_robots_txt(base_url, extracted_links)
    return l

def is_valid(url):
    try:
        parsed = parse.urlsplit(url, allow_fragments=False)
        #base_url = "{0.scheme}://{0.netloc}/".format(parsed)
        isInDomain = False
        #domains = ['ics.uci.edu', 'cs.uci.edu', 'informatics.uci.edu', 'stat.uci.edu', 'today.uci.edu/department/information_computer_sciences']

        if parsed.scheme not in set(["http", "https"]):
            return False

        for domain in DOMAINS:
            parseDom = parse.urlparse(domain)
            if 'today.uci.edu' in parsed.netloc and '/department/information_computer_sciences' not in parsed.path:
                return isInDomain
            elif parseDom.netloc in parsed.netloc:# or ('today.uci.edu' in parsed.netloc and '/department/information_computer_sciences' in parsed.path):
                isInDomain = True
                break
        if not isInDomain:
            return isInDomain
        '''
        if url in DOMAINS:
            print("URL ALREADY SEEDED")
            return False
        '''
        if 'pdf' in parsed.path.split('/'):
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise

'''
def Visited(urlList):
    urlSet = []
    #finalList = []
    # visited = open("visitedURLs.txt", "a+")
    #lines = visited.readlines()
    if not os.path.isfile('frontierURLs.txt'):
        with open('frontierURLs.txt', 'a+') as start:
            for index in range(len(DOMAINS)-1):
                start.write(DOMAINS[index])
            start.write(DOMAINS[-1])
    with open('frontierURLs.txt', 'a+') as tovisit:
        for line in tovisit:
            urlSet.append(line)
        urlSet = set(urlSet)
        urlList = set(urlList)
        finalSet = urlList.difference(urlSet)
        for url in finalSet:
            tovisit.write(url + "\n")

    
    #for url in urlList:
    #    if url in urlSet:
    #        continue
    #    else:
    #        finalList.append(url)
    
    #visited.close()
    return finalSet
'''

def UniqueURLs(defrag):
    # check if url is unique
    url_exists = True
    #urlSet = set()
    '''
    if not os.path.isfile('uniqueURLs.txt'):
        with open('uniqueURLs.txt', 'a+') as unique:
            for dom in DOMAINS:
                unique.write(dom + "\n")
    '''
    unique_set = file_to_set('uniqueURLs.txt')
    if defrag not in unique_set:
        write_to_file('uniqueURLs.txt', defrag.split())
        url_exists = False

    #with open('/uniqueURLs.txt', 'a+') as unique:
    #    for line in unique:
    #        urlSet.add(line)
    #    if defrag not in urlSet:
    #        print("writing url")
    #        unique.write(defrag + "\n")
    #        urlExists = False

    return url_exists



def write_to_file(file_name, url_list):
    with open(file_name, 'a+') as file:
        for url in url_list:
            file.write(url + "\n")


def file_to_set(file_name):
    file_set = set()
    with open(file_name, 'a+') as file:
        for line in file:
            file_set.add(line)
    return file_set


def parse_robots_txt(base_url, link_list):
    robots = ''
    rp = robotparser.RobotFileParser()
    links = []
    for link_url in link_list:
        if robots == '' or base_url not in robots:
            robots = base_url + 'robots.txt'
            print(robots)
            rp.set_url(robots)
            rp.read()
        if rp.can_fetch("*", link_url):
            print("link added ", link_url)
            links.append(link_url)
    return links

    '''
    unique = open("uniqueURLs.txt", "a+")
    lines = unique.readlines()
    urlExists = False
    for line in lines:
        if line == defrag:
            urlExists = True
            break
    if not urlExists:
        print("writing url")
        unique.write(defrag + "\n")
        print(defrag)
    unique.close()
    '''

