#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
import urllib2
from urllib2 import urlopen, URLError, HTTPError
import re, sys, os

install_seq = []

def dlmodule(url):
    print "[ %s ]" % url
    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page)

    for link in soup.find("td", text=" Package&nbsp;source: ").parent.parent.findAll('a', attrs={'href': re.compile("\.\./")}):
       dlfile(url+link.get('href'))

    deps = []
    imports = []

    try:
       for link in soup.find("td", text="Depends:").parent.parent.findAll('a', attrs={'href': re.compile("\.\./")}):
          deps.append(link.get('href').replace("index.html",""))

       for link in soup.find("td", text="Imports:").parent.parent.findAll('a', attrs={'href': re.compile("\.\./")}):
          imports.append(link.get('href').replace("index.html",""))

    except Exception, e:
       pass

    for link in deps:
       print ">>>>>> %s" % link
       dlmodule(url+link)

    for link in imports:
       print ">>>>>> %s" % link
       dlmodule(url+link)

def dlfile(url):
    try:
        f = urlopen(url)
        print "downloading " + url

        with open(os.path.basename(url), "wb") as local_file:
            local_file.write(f.read())

    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url

module = sys.argv[1]
cran_url = "https://cran.r-project.org/web/packages/%s/" % module
dlmodule(cran_url)
