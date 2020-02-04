import re
from urllib.parse import urlparse
from urllib.parse import urldefrag
from lxml import html
import os

def scraper(url, resp):
    links = extract_next_links(url, resp)
    validLinks = set([link for link in links if is_valid(link)])
    print(validLinks)
    finalLinks = Visited(validLinks)
    print(finalLinks)
    return list(finalLinks)

def extract_next_links(url, resp):
    # Implementation requred.
    # add robots.txt
    # check if valid page
    # defrag links

    # check if url responds
    if resp.status == 200:
        print("SUCCESS")
    elif resp.status == 404:
        print("FAIL")
        return list()

    defrag = urldefrag(url)[0]

    print(url)
    print(defrag)
    visited = open('visitedURLs.txt', 'a+')
    visited.write(defrag + "\n")
    visited.close()

    #if Visited(url):
    #   return list()

    UniqueURLs(defrag)

    # extract links on the url page
    extracted_links = set()
    try:
        content = resp.raw_response.content
        dom = html.fromstring(content)
        for link in dom.xpath('//a/@href'):
            if link[0] == '#' or len(link) == 1:
                print("cont")
                continue
            elif link[0] == '/' and link[1] != '/':
                link = urlparse(url).netloc + link
            print(link)
            #defragged = urldefrag(link)[0]
            extracted_links.add(link)
    except:
        print("Page content unavailable")
        print(url)

    #print(is_valid(defrag))
    return extracted_links

def is_valid(url):
    try:
        parsed = urlparse(url)
        isInDomain = False
        domains = ['ics.uci.edu', 'cs.uci.edu', 'informatics.uci.edu', 'stat.uci.edu', 'today.uci.edu/department/information_computer_sciences']

        if parsed.scheme not in set(["http", "https"]):
            return False

        for domain in domains:
            if domain in parsed.netloc or ('today.uci.edu' in parsed.netloc and '/department/information_computer_sciences' in parsed.path):
                isInDomain = True
                break
        if not isInDomain:
            return isInDomain

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


def Visited(urlList):
    urlSet = []
    #finalList = []
    # visited = open("visitedURLs.txt", "a+")
    #lines = visited.readlines()
    with open('visitedURLs.txt', 'a+') as visited:
        for line in visited:
            urlSet.append(line)
        urlSet = set(urlSet)
        urlList = set(urlList)
        finalSet = urlList.difference(urlSet)
        for url in finalSet:
            visited.write(url + "\n")

    '''
    for url in urlList:
        if url in urlSet:
            continue
        else:
            finalList.append(url)
    '''
    #visited.close()
    return finalSet


def UniqueURLs(defrag):
    # check if url is unique
    urlExists = False
    urlSet = set()
    with open('uniqueURLs.txt', 'a+') as unique:
        for line in unique:
            urlSet.add(line)
        if defrag not in urlSet:
            print("writing url")
            unique.write(defrag + "\n")
        '''
            if line == defrag:
                urlExists = True
                break
        if not urlExists:
            print("writing url")
            unique.write(defrag + "\n")
        '''

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

