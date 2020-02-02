import re
from urllib.parse import urlparse
from urllib.parse import urldefrag
from lxml import html

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation requred.
    # check if valid page
    # defrag links

    if resp.status == 200:
        print("SUCCESS")
    elif resp.status == 404:
        print("FAIL")
        return list()

    print(url)
    defrag = urldefrag(url)[0]
    print(defrag)

    extracted_links = list()

    visited = open("visitedURLs.txt", "w")
    visited.write(defrag)
    visited.close()

    print(is_valid(defrag))

    return list()

def is_valid(url):
    try:
        parsed = urlparse(url)
        isInDomain = False
        domains = ["ics.uci.edu", "cs.uci.edu", "informatics.uci.edu", "stat.uci.edu", "today.uci.edu/department/information_computer_sciences"]
        if parsed.scheme not in set(["http", "https"]):
            return False
        for domain in domains:
            if domain in parsed.netloc:
                isInDomain = True
                print(domain)
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
        print ("TypeError for ", parsed)
        raise