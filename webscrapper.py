from urllib.request import urlopen as uReq
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
import os

with open("c:/source_lists.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

def extractLinks(link):
    tmp_links = []
    page = uReq(link)
    soup = BeautifulSoup(page.read(), "html.parser")
    subTopic = re.sub(' - EUR-Lex', '', soup.title.string)
    subTopic = re.sub('["!<>\\\/:\?\*\|]', ' ', subTopic)
    for a in soup.find_all('a', href = re.compile(r'.*?uri=legissum:.*')):
        tmp_links.append(urljoin("https://eur-lex.europa.eu/", a['href']))
    return subTopic, tmp_links
    
def getTargetUrl(link):
    tmp_url = ""
    page = uReq(link)
    soup = BeautifulSoup(page.read(), "html.parser")
    for a in soup.find_all('a', href = re.compile(r'.*/legal-content/EN/TXT/HTML/.*')):
        tmp_url = urljoin("https://eur-lex.europa.eu/", a['href'])
    return tmp_url

for link in content:
    topic = re.search(r"\/summary\/chapter\/(\w*_?\w*?_?\w*?)", link).group(1)
    subTopic, subTopicLinks =  extractLinks(link)
    for url in subTopicLinks:
        target = getTargetUrl(url)
        target_html = uReq(target)
        soup = BeautifulSoup(target_html.read(), "html.parser")
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        # get text
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        title = text.split('\n', 1)[0]
        title = re.sub('["!<>\\\/:\?\*\|]', '', title)
        title = title.strip()
        directory = "d:/output/"+topic+"/"+subTopic.lower()
        if not os.path.exists(directory):
            print("creating directory "+directory)
            os.makedirs(directory)
        print("writing file: "+directory+"/"+title+".txt")
        f = open(directory+"/"+title+".txt", "w+", encoding="utf-8")
        f.write(text)
        f.close()
