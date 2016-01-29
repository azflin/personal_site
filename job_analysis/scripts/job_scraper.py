import re
import json
import sys
import string
import os

import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

from django.conf import settings


removable_words = [x.strip() for x in open(os.path.join(settings.BASE_DIR, 'job_analysis/scripts/removable_words.txt'), 'r').readlines()]


def get_jobs_analysis(search_query, location='', domain_extension='ca', max=sys.maxint):

    # Scrape job urls from indeed API
    job_urls = []
    params = dict(publisher=7148936385213166,
                  v=2,
                  format='json',
                  q=search_query,
                  l=location,
                  start=0,
                  limit=25,
                  co=domain_extension,
                  userip='1.2.3.4',
                  useragent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)")
    r = requests.get('http://api.indeed.com/ads/apisearch', params=params)
    page_of_jobs_dict = json.loads(r.text)
    for job in page_of_jobs_dict['results']:
        job_urls.append(job['url'])
    while params['start'] < page_of_jobs_dict['totalResults'] and params['start'] < max-25:
        params['start'] += 25
        r = requests.get('http://api.indeed.com/ads/apisearch', params=params)
        page_of_jobs_dict = json.loads(r.text)
        for job in page_of_jobs_dict['results']:
            job_urls.append(job['url'])
    print "Gathered {} urls".format(len(job_urls))

    # Scrape text from urls
    job_texts = []
    for url in job_urls:
        job_texts.append(scrape_text(url))
    print "Successfully scraped text from all urls"

    # Check frequency of keywords in URLs
    word_frequency = {}
    for text in job_texts:
        for word in text:
            word_frequency[word] = word_frequency.get(word, 0) + 1
    print "done word frequency"

    # Check frequency of bigrams
    bigram_frequency = {}
    for text in job_texts:
        for i in range(len(text)-1):
            bigram = text[i] + ' ' + text[i+1]
            bigram_frequency[bigram] = bigram_frequency.get(bigram, 0)+1
    print 'done!'
    return sorted(word_frequency.items(), key=lambda x: x[1], reverse=True), \
        sorted(bigram_frequency.items(), key=lambda x: x[1], reverse=True)


def scrape_text(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html)
    # Remove head, script, style, input and form tags
    for garbage_tag in soup(["head", "script", "style", "input", "form"]):
        garbage_tag.extract()
    text = soup.get_text(' ')
    # Remove spaces
    text = re.sub(r'(\s+)|(\s+\d+\s+)', ' ', text)
    # Remove unprintable unicode characters
    text = "".join([char for char in text if char in string.printable])
    # Remove punctuation
    text = "".join([char for char in text if char not in string.punctuation])
    # Remove stop words
    text = text.lower().split()
    text = [word for word in text if word not in stopwords.words("english")]
    text = [word for word in text if word not in removable_words]
    return text
