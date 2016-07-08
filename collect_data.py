import re
import math
import urllib.request

from collections import Counter
from bs4 import BeautifulSoup

from cassandra.solr_service import SolrService
from cassandra.solr_estimator import SolrEstimator

BASE_URL = "http://ufwebsite.tripod.com/scripts/"
SCRIPTS_URL = "http://ufwebsite.tripod.com/scripts/scripts.htm"

def get_all_urls():
    with urllib.request.urlopen(SCRIPTS_URL) as url:
        text = url.read()

    soup = BeautifulSoup(text, 'html.parser')
    pattern = re.compile("^([0-9]{3})")

    urls = []
    for url in soup.find_all('a'):
        href = url.get('href')
        if pattern.match(href):
            urls.append(href)

    return urls

def get_dialogues_from_episode(href):
    with urllib.request.urlopen(BASE_URL + href) as url:
        html = url.read()
        html = html.decode(encoding='UTF-8')

    conversations = get_all_conversations_from_episode(html)
    dialogues = select_dialogues_from_conversations(conversations)

    return dialogues

def get_all_conversations_from_episode(html):
    data = html.replace('\n', '')
    data = data.strip()
    data = re.sub(r'\([^)]*\)', '', data)
    data = re.sub(r'\[[^]]*\]', '', data)

    conversatios = data.split("<br>")
    conversatios = [s for s in conversatios if s]

    return conversatios

def select_dialogues_from_conversations(conversatios):
    dialogues = []
    for index in range(len(conversatios)):
        if(index+2 < len(conversatios)):
            name1 = re.findall(r'^[A-Z]*:', conversatios[index])
            name3 = re.findall(r'^[A-Z]*:', conversatios[index+2])
            if name1 and name3 and name1 == name3:
                text1 = re.sub(r"^[A-Z]*:", "", conversatios[index])
                text2 = re.sub(r"^[A-Z]*:", "", conversatios[index+1])
                text3 = re.sub(r"^[A-Z]*:", "", conversatios[index+2])
                text1 = text1.strip()
                text2 = text2.strip()
                text3 = text3.strip()

                if(text1 and text2 and text3):
                    dialogues.append([text1, text2])
                    dialogues.append([text2, text3])

    return dialogues

all_urls = get_all_urls()

solr = SolrService('cassandra')
for index, url in enumerate(all_urls):
    print("Importing episode " + str(index+1) + " of " + str(len(all_urls)))
    print(url)

    dialogues = get_dialogues_from_episode(url)
    # solr.load_dialogues(dialogues)
