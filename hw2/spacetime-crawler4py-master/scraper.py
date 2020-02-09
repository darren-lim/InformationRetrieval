import re
from urllib import parse
import string
from bs4 import BeautifulSoup, SoupStrainer
from lxml import html
from lxml import etree, objectify
import requests
from reppy.robots import Robots
import os
import sys
import time

DOMAINS = ['https://www.ics.uci.edu', 'https://www.cs.uci.edu', 'https://www.informatics.uci.edu', 'https://www.stat.uci.edu', 'https://today.uci.edu/department/information_computer_sciences/']

def scraper(url, resp):
    links = extract_next_links(url, resp)
    validLinks = sorted([link for link in links if is_valid(link)])
    #print(validLinks)
    #print()
    #final = parse_robots_txt(validLinks)
    '''
    while True:
        next = input("Press a next, e quit ")
        if next == 'a':
            break
        elif next == 'e':
            sys.exit()
    print("next")
    '''
    return validLinks

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

    did_visit = UniqueURLs(defrag)
    # might not need this
    if did_visit:
        print("did visit")
        return list()

    extracted_links = set()

    write_to_file('visitedURLs.txt', defrag.split())
    #visited = open('visitedURLs.txt', 'a+')
    #visited.write(defrag + "\n")
    #visited.close()

    content = resp.raw_response.content
    soup = BeautifulSoup(content, 'lxml')
    extracted_links = find_all_links(base_url, soup)

    extracted_text = find_all_text(soup)
    token_list = tokenize(extracted_text)
    freq_dict = computeWordFrequencies(token_list)
    no_stop = remove_stop_words(freq_dict)
    printFreq(no_stop)

    #add html parsing

    #print(is_valid(defrag))
    #return list()
    #extracted_links = sorted(list(extracted_links))
    #l = parse_robots_txt(base_url, extracted_links)
    return list(extracted_links)

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


def find_all_links(base_url, soup):
    links = set()
    for link in soup.find_all('a', href=True):
        link_url = link['href']
        if len(link_url) > 200:
            continue
        url = parse.urljoin(base_url, link_url)
        links.add(url)
    return links


def find_all_text(soup):
    tag_list = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    text_list = [text for text in soup.find_all(text=True) if text.parent.name in tag_list]
    return text_list

def parse_robots_txt(link_list):
    robotsURL = ''
    robots = None
    links = []
    try:
        for link_url in link_list:
            parsed_link = parse.urlparse(link_url)
            link_base = '{0.scheme}://{0.netloc}/'.format(parsed_link)
            if robots == None or link_base not in robotsURL:
                robots_txt_name = parsed_link.netloc.split('.')
                robots_txt_name = ''.join(robots_txt_name)
                robotsURL = link_base + 'robots.txt'
                time.sleep(0.5)
                robots = Robots.fetch(robotsURL, timeout=20)
            if parsed_link.query == '':
                query_only = '{0.path}/{0.params}/'.format(parsed_link)
            else:
                query_only = '{0.path}/{0.params}/?/{0.query}'.format(parsed_link)
            if robots.allowed(query_only, '*'):
                links.append(link_url)
        return links
    except Exception as e:
        print("unable to robot: ", e)
        return link_list


'''
Tokenize has a time complexity dependent on the size of the text file. O(N)
'''
def tokenize(text_list):
    #if os.stat(TextFilePath).st_size == 0:
    #    print(TextFilePath + " is Empty")
    #    return []
    #file = open(TextFilePath, "r")
    tokenList = []
    for line in text_list:
        line = re.sub(r'[^\x00-\x7f]', r' ', line).lower()
        line = line.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
        tokenList.extend(line.split())
    if len(tokenList) == 0:
        print("No valid tokens in the list")
    return tokenList


def remove_stop_words(text_dict):
    final = text_dict
    with open('stopwords.txt') as file:
        for line in file:
            line = line.strip()
            if line in final:
                del final[line]
    return final

'''
computeWordFrequencies has a time complexity dependent on the size of the input. O(N)
'''
def computeWordFrequencies(ListOfToken):
    wordFreqDict = {}
    for token in ListOfToken:
        if token not in wordFreqDict:
            wordFreqDict[token] = 1
        else:
            wordFreqDict[token] += 1
    return wordFreqDict


'''
printFreq has a time complexity dependent on the size of the input.
The function sorts the frequency dictionary, thus the complexity is O(n log n)
'''
def printFreq(Frequencies):
    sortedFreq = sorted(Frequencies.items(), key = lambda val: val[1], reverse=True)
    for item in sortedFreq:
        print(str(item[0]) + " -> " + str(item[1]))

