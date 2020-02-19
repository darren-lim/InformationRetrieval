import os
import json
from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import re
import string

class Indexer:

    def __init__(self):
        # Posting structure: {token: {doc index #: [tf, importance of token]
        self.posting_dict = dict()
        self.doc_num = 0  # document numbering

        # https://stackoverflow.com/questions/15547409/how-to-get-rid-of-punctuation-using-nltk-tokenizer
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.stemmer = PorterStemmer()

        # for M1 report
        self.doc_count = 0
        self.unique_count = 0

    def indexer_main(self):
        if os.path.exists('ANALYST'):
            a = []
            count_num = 0
            for path in os.listdir('ANALYST'):
                for json_file in os.listdir('ANALYST/'+path):
                    # load json
                    json_path = 'ANALYST/'+path+'/'+json_file
                    print(json_path)
                    with open(json_path, 'r') as jfile:
                        data = json.load(jfile)
                        self.parse_html(count_num, data['content'])
                    count_num+=1
                    if count_num == 3:
                        break
                if count_num == 3:
                    break


    def parse_html(self, doc_index, content):
        soup = BeautifulSoup(content, "lxml")
        print(doc_index)
        for line in soup.find_all(["h1", "h2", "h3", "strong", "b"]):
            text = line.get_text()
            token_list = self.tokenizer.tokenize(text)
            for token in token_list:
                self.index_token(token, doc_index, 2)

        all_text = self.find_all_text(soup)
        for words in all_text:
            tokens = self.tokenizer.tokenize(words)
            for token in tokens:
                self.index_token(token, doc_index, 0)

        print(self.posting_dict)

        self.doc_count += 1


    # CHANGE THIS FORMAT, TOO CLOSE TO ANDREWS
    def index_token(self, token, doc_index, importance):
        stemmed = self.stemmer.stem(token.lower())
        if not self.check_word(stemmed):
            return
        if stemmed in self.posting_dict:
            if doc_index in self.posting_dict[stemmed]:
                self.posting_dict[stemmed][doc_index][0] += 1
                self.posting_dict[stemmed][doc_index][1] += importance
            else:
                self.posting_dict[stemmed][doc_index] = [1, importance]
        else:
            self.posting_dict[stemmed] = {doc_index: [1, importance]}

    '''
    find_all_text has a time complexity of O(N) because we are going through all the text.
    '''
    # https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text?noredirect=1&lq=1
    def find_all_text(self, soup):
        texts = soup.findAll(text=True)
        visible_texts = filter(self.filter_tags, texts)
        return [t.strip() for t in visible_texts if t.strip() != '']

    '''
    Time complexity of filter_tags is O(1) because in evaluation in set only takes O(1) time.
    '''
    # https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text?noredirect=1&lq=1
    def filter_tags(self, element):
        if element.parent.name in {'style', 'script', '[document]', 'head', 'title', 'meta', 'noscript', 'h1', 'h2', 'h3', 'strong', 'b'}:
            return False
        if isinstance(element, Comment):
            return False
        return True


    def check_word(self, word):
        if not word.isdigit():
            if len(word) == 1:
                return False
        return True



if __name__ == "__main__":
    indexer = Indexer()
    indexer.indexer_main()