import sys
import re
import string
import os

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import json
from time import sleep

from forms import JobAnalysisForm


# This data structure holds results for job analyses.
analysis_dict = {}


def do_job_analysis(request):
    if request.method == 'POST':

        # Grab parameters for function
        analysis_id = request.POST.get('analysis_id')
        search_query = request.POST.get('search_query')
        location = request.POST.get('location')
        country = request.POST.get('country')
        max_jobs = request.POST.get('max_jobs')
        if not max_jobs:
            max_jobs = sys.maxint
        else:
            max_jobs = int(max_jobs)

        # Declare unique dict for the job analysis
        analysis_dict[analysis_id] = {}
        d = analysis_dict[analysis_id]

        # Build list of urls from post parameters
        urls = []
        params = {
            'publisher': 7148936385213166,
            'v': 2,
            'format': 'json',
            'q': search_query,
            'l': location,
            'start': 0,
            'limit': 25,
            'co': country,
            'userip': '1.2.3.4',
            'useragent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)"
        }
        r = requests.get('http://api.indeed.com/ads/apisearch', params=params)
        page_of_jobs_dict = json.loads(r.text)
        for job in page_of_jobs_dict['results']:
            urls.append(job['url'])
        while params['start'] < page_of_jobs_dict['totalResults'] and params['start'] < max_jobs-25:
            params['start'] += 25
            r = requests.get('http://api.indeed.com/ads/apisearch', params=params)
            page_of_jobs_dict = json.loads(r.text)
            for job in page_of_jobs_dict['results']:
                urls.append(job['url'])
        # Finally load the urls into id dict
        d['urls'] = urls

        job_texts = []
        d['progress'] = 0
        for url in urls:
            job_texts.append(scrape_text(url))
            d['progress'] += 1

        word_frequency = {}
        for text in job_texts:
            for word in text:
                word_frequency[word] = word_frequency.get(word, 0) + 1
        bigram_frequency = {}
        for text in job_texts:
            for i in range(len(text)-1):
                bigram = text[i] + ' ' + text[i+1]
                bigram_frequency[bigram] = bigram_frequency.get(bigram, 0)+1
        d['frequencies'] = {
            'words': sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)[:25],
            'bigrams': sorted(bigram_frequency.items(), key=lambda x: x[1], reverse=True)[:25]
        }

    # Throws server error if nothing returned.
    return JsonResponse({})


def poll_jobs_analysis(request):
    analysis_id = request.GET.get('analysis_id')
    d = analysis_dict[analysis_id]
    # Wait for something to be in dictionary.
    while not d:
        sleep(0.1)
    return JsonResponse(d)


def index(request):
    if request.method == 'GET':
        form = JobAnalysisForm()
        return render(request, 'job_analysis/index.html', {'form': form})


def scrape_text(url):

    removable_words = [x.strip() for x in open(os.path.join(settings.BASE_DIR, 'job_analysis/scripts/removable_words.txt'), 'r').readlines()]

    html = requests.get(url).text
    soup = BeautifulSoup(html)
    # Remove head, script, style, input and form tags
    for garbage_tag in soup(["head", "script", "style", "input", "form"]):
        garbage_tag.extract()
    text = soup.get_text(' ')
    # Remove spaces
    text = re.sub(r'(\s+)|(\s+\d+\s+)', ' ', text)
    # Remove numbers
    text = re.sub(r'(\s+\d+\s+)', ' ', text)
    # Remove unprintable unicode characters
    text = "".join([char for char in text if char in string.printable])
    # Remove punctuation
    text = "".join([char for char in text if char not in string.punctuation])
    # Remove stop words
    text = text.lower().split()
    text = [word for word in text if word not in stopwords.words("english")]
    text = [word for word in text if word not in removable_words]
    return text

