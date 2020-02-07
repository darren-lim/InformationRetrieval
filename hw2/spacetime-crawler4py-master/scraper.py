import re
from urllib.parse import urlparse
from urllib.parse import urldefrag
from urllib.parse import urlsplit
from urllib.parse import urljoin
#from urllib import parse
from urllib import robotparser

from lxml import html
from lxml import etree, objectify
import requests
import os

DOMAINS = ['https://www.ics.uci.edu', 'https://www.cs.uci.edu', 'https://www.informatics.uci.edu', 'https://www.stat.uci.edu', 'https://today.uci.edu/department/information_computer_sciences/']

def scraper(url, resp):
    links = extract_next_links(url, resp)
    validLinks = set([link for link in links if is_valid(link)])
    print(validLinks)
    #finalLinks = Visited(validLinks)
    #print(finalLinks)
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

    defrag = urldefrag(url)[0]
    parsedUrl = urlsplit(url, allow_fragments=False)
    print(url)
    print(parsedUrl.netloc)

    with open('frontierURLs.txt', 'a+') as visit:
        visit.write(parsedUrl.netloc + "\n")

    didvisit = UniqueURLs(defrag)
    if didvisit:
        return list()

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

    visited = open('visitedURLs.txt', 'a+')
    visited.write(defrag + "\n")
    visited.close()


    # extract links on the url page
    extracted_links = set()
    if resp.raw_response == None:
        return list()
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

    robots = ''
    for link in dom.xpath('//a/@href'):
        if link[0] == '#' or len(link) == 1:
            continue
        parseLink = urlsplit(link, allow_fragments=False)
        if parseLink.scheme == '':
            if link[0] == '/' and link[1] != '/':
                print(parsedUrl.netloc)
                link = urljoin(defrag, link)
                print("yes")
            elif link[0] == '/' and link[1] == '/':
                link = urljoin('https:', link)
            else:
                print("WHAT" + link)
            #elif link[0] == '/' and link[1] == '/':
            #    link = 'https:' + link
        if len(link) >= 300:
            continue
        newLink = urlsplit(link)
        print(newLink)
        #print(newLink.scheme)
        fullDomain = urljoin(parsedUrl.scheme, parsedUrl.netloc)
        print(fullDomain)

        # robDom = parse.urljoin(fullDomain, '/robots.txt')
        # IF a link to another domain exists, check its robots.txt to see if it is a valid link to crawl
        # fetch doesnt seem to work
        if robots == '':
            robots = parsedUrl.scheme + '://' + parsedUrl.netloc + '/robots.txt'
           # robots = robDom
            print(robots)
            rp.set_url(robots)
            rp.read()
        if rp.can_fetch("*", robots):
            extracted_links.add(link)
        else:
            print("Cannot fetch acc robots.txt")
    #except:
    #    print("Page content unavailable")
    #    print(url)

    #add html parsing

    #print(is_valid(defrag))
    return extracted_links

def is_valid(url):
    try:
        parsed = urlparse(url)
        isInDomain = False
        #domains = ['ics.uci.edu', 'cs.uci.edu', 'informatics.uci.edu', 'stat.uci.edu', 'today.uci.edu/department/information_computer_sciences']

        if parsed.scheme not in set(["http", "https"]):
            return False

        for domain in DOMAINS:
            parseDom = urlparse(domain)
            if 'today.uci.edu' in parsed.netloc and '/department/information_computer_sciences' not in parsed.path:
                return isInDomain
            elif parseDom.netloc in parsed.netloc:# or ('today.uci.edu' in parsed.netloc and '/department/information_computer_sciences' in parsed.path):
                isInDomain = True
                break
        if not isInDomain:
            return isInDomain

        if url in DOMAINS:
            print("URL ALREADY SEEDED")
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
    urlExists = True
    urlSet = set()
    '''
    if not os.path.isfile('uniqueURLs.txt'):
        with open('uniqueURLs.txt', 'a+') as unique:
            for dom in DOMAINS:
                unique.write(dom + "\n")
    '''
    with open('uniqueURLs.txt', 'a+') as unique:
        for line in unique:
            urlSet.add(line)
        if defrag not in urlSet:
            print("writing url")
            unique.write(defrag + "\n")
            urlExists = False
    return urlExists



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

