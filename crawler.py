
from crawler_core import Crawler
import re
import json
import csv
import random
import time
def open_csv(csvFile):
    file = open(csvFile)
    csvReader = csv.reader(file)
    header = next(csvReader)
    rows = []
    for row in csvReader:
        rows.append(row)
    file.close()
    return (header, rows)


def save_res(input, file):
    with open(file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(input)

def process(base_url, instruction, crawler, id=""):
    
    res = []
    with open("jsonCrawler/" + instruction) as f:
        road = json.load(f)
    url = base_url + id
    crawler.gotoObjective(road, url, do_init=True)
    for action in road["step"]:
        try:
            r = crawler.gotoObjective(action, url)
        except Exception as e:
            r = False
        if action[-1]["Regex"] != "":
            try:
                regex = re.compile(action[-1]["Regex"])
                r = [url for url in r if regex.search(url)] 
            except Exception as e:
                print(e)
                return
        res.append(r)
    return res #NEED TO FIX SO THAT WHE DON"T NEED TO DO res[0] on the output of the function

def save_res(input, file):
    with open(file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(input)


def get_article_urls(json):
        
    base_url = "https://www.reuters.com/site-search/?query=Technology&date=past_month&offset="
    iter = 220
    step = 20
    
    while iter < 290:
        crawler = Crawler(header=None, proxies=None, headless=False)
        current_url = base_url + str(iter)
        print(current_url)
        found_url = list(set(process(current_url, json, crawler)[0]))
        for article in found_url:
            with open("articles_urls_last_week.csv", 'a') as f:
                f.write("https://www.reuters.com" + article + '\n')
        iter += step
        time.sleep(random.uniform(0, 4))
        crawler.shutdown()
        del crawler






def get_article_content(json, source):
    _ , rows = open_csv(source)
    for row in rows:
        crawler = Crawler(header=None, proxies=None, headless=False) #if headless True reuters detect it and block us
        title, author, date, summary, content = process(row[0], json, crawler)
        save_res([row[0], title, author, date, summary[0], content.replace("\n", " ")], "result.csv")
        crawler.shutdown()
        del crawler

#STEP 1 GET ALL ARTICLES URLS FROM SEARCH TOOL OF REUTERS 
get_article_urls("reuters.json")

#STEP 2 GET ALL ARTICLES CONTENT
get_article_content("reuters_articles.json", "articles_urls.csv")


###BELOW IS FOR RUNNING THE CODE WITH THREAD BUT IT'S NOT WORKING WELL FOR NOW

# import threading
# from queue import Queue

# def worker(queue, json, source):
#     while not queue.empty():
#         item = queue.get()
#         try:
#             get_article_content(json, source, item)
#         finally:
#             queue.task_done()

# def get_article_content(json, source, row):
#     crawler = Crawler(header=None, proxies=None, headless=False)
#     title, author, date, summary, content = process(row[0], json, crawler)
#     save_res([row[0], title, author, date, summary[0], content.replace("\n", " ")], "result.csv")
#     crawler.shutdown()
#     del crawler

# def main():
#     source = "articles_urls.csv"
#     json = "reuters_articles.json"

#     _, rows = open_csv(source)
#     queue = Queue()

#     # Populate queue with tasks
#     for row in rows:
#         queue.put(row)

#     num_threads = 1 # Adjust based on your system's capability and the website's tolerance

#     threads = []
#     for _ in range(num_threads):
#         t = threading.Thread(target=worker, args=(queue, json, source))
#         t.start()
#         threads.append(t)

#     # Wait for all threads to finish
#     queue.join()

#     for t in threads:
#         t.join()

# if __name__ == "__main__":
#     main()
