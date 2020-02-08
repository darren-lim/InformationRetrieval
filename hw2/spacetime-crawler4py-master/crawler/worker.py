from threading import Thread

from utils.download import download
from utils import get_logger
from scraper import scraper
import time

import sys

from reppy.robots import Robots
from urllib import parse

class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        super().__init__(daemon=True)
        
    def run(self):
        run_time = 300
        run_start = 300
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break
            if self.frontier.check_url_completed(tbd_url):
                print("URL Already marked complete")
                print(tbd_url)
                print("Loading next url")
                continue
            resp = download(tbd_url, self.config, self.logger)
            if resp == None:
                self.logger.info(
                    f"{tbd_url} Timeout")
                continue
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            scraped_urls = scraper(tbd_url, resp)
            check_robots = self.parse_robots_txt(scraped_urls)
            for scraped_url in check_robots:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            print(len(check_robots) == len(scraped_urls))
            time.sleep(self.config.time_delay)
            if run_start == run_time:
                while True:
                    if run_start == run_time:
                        next = input("Press a next, e quit, q run 300 times ")
                        if next == 'a':
                            break
                        elif next == 'e':
                            sys.exit()
                        elif next == 'q':
                            run_start = 0
                            break
            else:
                run_start += 1

    def parse_robots_txt(self, link_list):
        host, port = self.config.cache_server
        robotsURL = ''
        robots = None
        links = []
        try:
            for link_url in link_list:
                parsed_link = parse.urlparse(link_url)
                link_base = '{0.scheme}://{0.netloc}/'.format(parsed_link)
                if robots == None or link_base not in robotsURL:
                    robotsURL = link_base + 'robots.txt'
                    time.sleep(0.5)
                    # get the robots.txt file
                    robots = Robots.fetch(f"http://{host}:{port}/", params=[("q", f"{robotsURL}"), ("u", f"{self.config.user_agent}")], timeout=20)

                    # WARNING: UNCOMMENTING BYPASSES CACHE

                    # if the robots is empty, get the robots.txt from actual server
                    #robots_str = str(robots)
                    #robots_str = robots_str.split(': ')[1].split('}')[0]
                    #if robots_str == '[]':
                    #    robots = Robots.fetch(robotsURL, timeout=20)
                    #    print(robots)

                if parsed_link.params == '':
                    if parsed_link.query == '':
                        query_only = '{0.path}/'.format(parsed_link)
                    else:
                        query_only = '{0.path}/?{0.query}'.format(parsed_link)
                else:
                    if parsed_link.query == '':
                        query_only = '{0.path}/{0.params}/'.format(parsed_link)
                    else:
                        query_only = '{0.path}/{0.params}/?{0.query}'.format(parsed_link)
                if robots.allowed(query_only, self.config.user_agent):
                    links.append(link_url)
            return links
        except Exception as e:
            print("unable to robot: ", e)
            return link_list