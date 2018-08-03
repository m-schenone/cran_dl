#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
import urllib2
from urllib2 import urlopen, URLError, HTTPError
import re, sys, os

install_seq = []

def mirror_url(name):
    return "https://cran.r-project.org/web/packages/%s/" % name

def xtract_package(url):
    return url.replace("index.html","").split("/")[-2]

def dl_package(name):
    print "[ %s ]" % name
    url = mirror_url(name)
    install_seq.append(name)
    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page)

    for link in soup.find("td", text=" Package&nbsp;source: ").parent.parent.findAll('a', attrs={'href': re.compile("\.\./")}):
       dl_file(url+link.get('href'))

    deps = []
    imports = []

    try:
       for link in soup.find("td", text="Depends:").parent.parent.findAll('a', attrs={'href': re.compile("\.\./")}):
          deps.append(xtract_package(link.get('href')))
          install_seq.append(name)

       for link in soup.find("td", text="Imports:").parent.parent.findAll('a', attrs={'href': re.compile("\.\./")}):
          imports.append(xtract_package(link.get('href')))
          install_seq.append(name)

    except Exception, e:
       pass

    for pkg in deps:
       print ">>>>>> %s" % pkg
       dl_package(pkg)

    for pkg in imports:
       print ">>>>>> %s" % pkg
       dl_package(pkg)

def dl_file(url):
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
dl_package(module)

for p in reversed(install_seq):
    print "R CMD INSTALL %s" % p
