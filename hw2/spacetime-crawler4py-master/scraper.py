import re
from urllib import parse
import string
from bs4 import BeautifulSoup, Comment
import os
import sys

DOMAINS = ['https://www.ics.uci.edu', 'https://www.cs.uci.edu', 'https://www.informatics.uci.edu', 'https://www.stat.uci.edu', 'https://today.uci.edu/department/information_computer_sciences/']

class WebScraper:

    def __init__(self):
        self.unique_urls = set()
        self.longest_page = dict()
        self.common_words = dict()
        self.subdomains = dict()
        #self.no_content_paths = set()

    def scraper(self, url, resp):
        links = self.extract_next_links(url, resp)
        validLinks = sorted([link for link in links if is_valid(link)], reverse=True)
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

    def extract_next_links(self, url, resp):
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
            return list()
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
            print("raw resp is none")
            return list()
        if not resp.raw_response.ok:
            print("resp is not ok ):")
            return list()
        content_size = 0
        # 512 * 16
        for chunk in resp.raw_response.iter_content(8192):
            content_size += len(chunk)
        # dont crawl if the content size is greater than 7 mb
        # average size of a website is 3 - 4 mb* according to google
        if content_size > 7000000:
            print("too big")
            return list()

        defrag = parse.urldefrag(url)[0]
        parsedUrl = parse.urlsplit(url, allow_fragments=False)
        base_url = "{0.scheme}://{0.netloc}/".format(parsedUrl)
        print(url)

        did_visit = self.UniqueURLs(defrag)
        # checks defragged urls
        if did_visit:
            print("did visit")
            return list()

        self.write_to_file('visitedURLs.txt', defrag.split())
        if 'https://today.uci.edu/department/information_computer_sciences/calendar' in defrag:
            return list()
        content = resp.raw_response.content
        soup = BeautifulSoup(content, 'lxml')
        #print(soup)
        for script in soup.find_all('script'):
            script.extract()
        #print(soup)
        # remove comments
        for comments in soup.findAll(text=lambda text: isinstance(text, Comment)):
            comments.extract()

        for hidden in soup.find_all("div",attrs={"style": "display: none;"}):
            hidden.extract()
        #extracted_links = find_all_links(base_url, soup)

        p_text = self.find_all_text(soup)
        #p_text = soup.find_all(text = True)
        #print(p_text)
        #for p in p_text:
        #    print(p.parent)
        p_tokens = self.tokenize(p_text)
        #print(len(p_tokens))
        print(p_tokens)

        # If low textual content / information, dont get links (considered avoiding low content families)
        if len(p_tokens) < 60:
            #extracted_links = self.find_all_links(base_url, soup)
            #return extracted_links
            if parsedUrl.path == '':
                if '.ics.uci.edu' in base_url:
                    self.add_subdomains(parsedUrl.netloc)

                extracted_links = self.find_all_links(base_url, soup)

                return extracted_links
            print("No textual content")
            return list()
        '''
            if defrag in self.no_content_paths:
                return list()
            else:
                for path in self.no_content_paths:
                    if path in parsedUrl.path:
                        return list()
                self.no_content_paths.add(defrag)
                links = self.find_all_links(base_url, soup)
                for link in links:
                    link_path = parse.urlsplit(url, allow_fragments=False).path
                    if link_path in link:
                        return list()
                return self.find_all_links(base_url, soup)
            '''
        # check if the page has low information
        # if low information, get each subsequent link within that path
        # ignore those paths ?? ???????

        freq_dict = self.computeWordFrequencies(p_tokens)
        no_stop = self.remove_stop_words(freq_dict)
        #self.printFreq(no_stop)

        # add values to words common words dict
        for key, value in no_stop.items():
            if key in self.common_words.keys():
                self.common_words[key] += value
            else:
                self.common_words[key] = value

        # Check longest page length
        list_len = len(no_stop)
        for key, value in self.longest_page.items():
            if list_len >= value:
                self.longest_page.clear()
                self.longest_page[defrag] = value

        if '.ics.uci.edu' in base_url:
            self.add_subdomains(parsedUrl.netloc)

        extracted_links = self.find_all_links(base_url, soup)

        return list(extracted_links)

    '''
    def is_valid(self, url):
        try:
            parsed = parse.urlsplit(url, allow_fragments=False)
            isInDomain = False

            if parsed.scheme not in set(["http", "https"]):
                return False

            for domain in self.DOMAINS:
                parseDom = parse.urlparse(domain)
                if 'today.uci.edu' in parsed.netloc and '/department/information_computer_sciences' not in parsed.path:
                    return isInDomain
                elif parseDom.netloc in parsed.netloc:# or ('today.uci.edu' in parsed.netloc and '/department/information_computer_sciences' in parsed.path):
                    isInDomain = True
                    break
            if not isInDomain:
                return isInDomain
            
            #if url in DOMAINS:
            #    print("URL ALREADY SEEDED")
            #    return False
            
            parsed_path = set(parsed.path.split('/'))
            if 'pdf' in parsed_path:
                return False
            if 'xml' in parsed_path:
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
    def UniqueURLs(self, defrag):
        # check if url is unique
        if defrag not in self.unique_urls:
            self.unique_urls.add(defrag)
            return False
        return True

    def write_to_file(self, file_name, url_list):
        with open(file_name, 'a+') as file:
            for url in url_list:
                file.write(url + "\n")


    def file_to_set(self, file_name):
        file_set = set()
        with open(file_name, 'a+') as file:
            for line in file:
                file_set.add(line)
        return file_set


    def find_all_links(self, base_url, soup):
        links = set()
        for link in soup.find_all('a', href=True):
            link_url = link['href']
            if len(link_url) > 300:
                continue
            url = parse.urljoin(base_url, link_url)
            defragged_url = parse.urldefrag(url)[0]
            links.add(defragged_url)
        return links

    '''
    def find_all_text(soup):
        for script in soup(['script', 'style']):
            script.decompose()
        tag_list = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a']
        text_list = [text for text in soup.find_all(text=True) if text.parent.name in tag_list]
        print(soup.get_text)
        return text_list
    '''

    # https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text?noredirect=1&lq=1
    def find_all_text(self, soup):
        texts = soup.findAll(text=True)
        visible_texts = filter(self.filter_tags, texts)
        return [t.strip() for t in visible_texts if t.strip() != '']

    def filter_tags(self, element):
        if element.parent.name in {'style', 'script', '[document]', 'head', 'title', 'meta', 'noscript', 'header', 'html'}:
            return False
        if element.name == 'a':
            return False
        return True


    def find_text(self, soup):
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        return soup.get_text()


    def find_paragraph_words(self, soup):
        tag_list = {'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'td'}
        return [t.strip() for t in soup.find_all(text=True) if t.parent.name in tag_list]


    '''
    Tokenize has a time complexity dependent on the size of the text file. O(N)
    '''
    def tokenize(self, text_list):
        tokenList = []
        for line in text_list:
            line = re.sub(r'[^\x00-\x7f]', r' ', line).lower()
            line = line.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
            tokenList.extend(line.split())
        if len(tokenList) == 0:
            print("No valid tokens in the list")
        return tokenList


    def remove_stop_words(self, text_dict):
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
    def computeWordFrequencies(self, ListOfToken):
        wordFreqDict = dict()
        for token in ListOfToken:
            if token not in wordFreqDict.keys():
                wordFreqDict[token] = 1
            else:
                wordFreqDict[token] += 1
        return wordFreqDict


    '''
    printFreq has a time complexity dependent on the size of the input.
    The function sorts the frequency dictionary, thus the complexity is O(n log n)
    '''
    def printFreq(self, Frequencies):
        sortedFreq = sorted(Frequencies.items(), key = lambda val: val[1], reverse=True)
        for item in sortedFreq:
            print(str(item[0]) + " -> " + str(item[1]))

    def add_subdomains(self, sdomain):
        if sdomain not in self.subdomains:
            self.subdomains[sdomain] = 1
        else:
            self.subdomains[sdomain] += 1

    def most_common_words(self):
        return sorted(self.common_words.items(), key=lambda val: val[1], reverse=True)

    def get_unique_pages_count(self):
        return len(self.unique_urls)

    def get_longest_page(self):
        return self.longest_page

    def get_subdomains(self):
        return self.subdomains


def is_valid(url):
    try:
        parsed = parse.urlsplit(url, allow_fragments=False)
        isInDomain = False

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
        parsed_path = set(parsed.path.split('/'))
        if '/pdf' in parsed_path:
            return False
        if '/xml' in parsed_path:
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