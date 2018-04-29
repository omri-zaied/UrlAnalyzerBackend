
from bs4 import BeautifulSoup
from numpy.lib.function_base import extract
import itertools
from bs4.element import Doctype
from html import parser
import requests
from flask import jsonify, json
from flask.app import Flask, request
from urllib.parse import urlparse
from itertools import groupby

def __CountOccurences(soup, value):
    count = len(soup.find_all(value))
    return count

def __PageContainsLogin(soup):
    # A login form would contain a field for password.
    # It might be more then a single occurence for this password field since in some cases you can log in or register in the same page
    number = len(soup.find_all('input', {'type':'password'}))  
    if number > 0:
        return True
    else:
        return False

def __GetHostFromUrl(url):
    parsedUrl = urlparse(url)
    return parsedUrl.hostname

def __IsLinkInternal(origUrl, linkUrl):
    origHostname = __GetHostFromUrl(origUrl)
    linkHostname = __GetHostFromUrl(linkUrl)
    if origHostname == linkHostname or not linkHostname:
        return True
    else:
        return False

def __LinkIsBroken(link):
    page = requests.get(link)
    if page.ok:
        return False
    else:
        return True

def __GroupLinksToInternalExternal(url, links):
    internalLinks = {}
    externalLinks = {}
    for link in links:
        if not link:
            continue
        if __IsLinkInternal(url, link):
            localizedLink = url + link
            internalLinks[link] = __LinkIsBroken(localizedLink)
        else:
            externalLinks[link] = __LinkIsBroken(link)
    return internalLinks, externalLinks

def __GetHtmlVersionFromDoctype(doctype):
    # Taken from https://www.w3.org/QA/2002/04/valid-dtd-list.html
    if not doctype:
        return "N/A"
    elif "//W3C//DTD XHTML 1.0 Strict" in doctype:
        return "XHTML 1.0 Strict"
    elif "//W3C//DTD XHTML 1.0 Transitional" in doctype:
        return "XHTML 1.0 Transitional"
    elif "//W3C//DTD XHTML 1.0 Frameset" in doctype:
        return "XHTML 1.0 Frameset"
    elif "//W3C//DTD XHTML 1.1" in doctype:
        return "XHTML 1.1 DTD"
    elif "//W3C//DTD XHTML Basic 1.1" in doctype:
        return "XHTML 1.1 Basic"
    elif "//W3C//DTD HTML 4.01 Transitional" in doctype:
        return "HTML 4.01 Transitional"
    elif "//W3C//DTD HTML 4.01 Frameset" in doctype:
        return "HTML 4.01 Frameset"
    elif "//W3C//DTD HTML 4.01" in doctype:
        return "HTML 4.01 Strict"
    elif "//IETF//DTD HTML 2.0" in doctype:
        return "HTML 2"
    elif "//W3C//DTD HTML 3.2 Final" in doctype:
        return "HTML 3.2"
    elif "<!DOCTYPE HTML>" in doctype:
        return "HTML 5"
    else:
        return "Unknown"

def __ToJson(url, title, h1, h2, h3, h4, h5, h6, internalLinks, externalLinks, containsLogin, htmlVersion):
    dict = {
        "URL": url
        ,"Title": title
        ,"H1Number":  h1
        ,"H2Number":  h2
        ,"H3Number":  h3
        ,"H4Number":  h4
        ,"H5Number":  h5
        ,"H6Number":  h6
        ,"HtmlVersion":  htmlVersion
        ,"ContainsLogin":  containsLogin
        ,"InternalLinks":  internalLinks
        ,"ExternalLinks":  externalLinks
        }
    jsonStr =json.dumps(dict)
    return jsonify(Analysis=jsonStr)

def AnalyzeUrl(url):
    try:
        page = requests.get(url)
        page.raise_for_status()
        text = page.text
        statusCode = page.status_code
        soup = BeautifulSoup(text, 'html.parser')
        links = [ x.get('href') for x in soup.findAll('a') ]
        internalLinks, externalLinks = __GroupLinksToInternalExternal(url, links)
        h1 = __CountOccurences(soup, "h1")
        h2 = __CountOccurences(soup, "h2")
        h3 = __CountOccurences(soup, "h3")
        h4 = __CountOccurences(soup, "h4")
        h5 = __CountOccurences(soup, "h5")
        h6 = __CountOccurences(soup, "h6")
        containsLogin = __PageContainsLogin(soup)
        htmlVersion = __GetHtmlVersionFromDoctype(soup.Doctype)
        title = soup.title.text
    except Exception:
        raise
    return jsonify(
        url=url
        ,title=title
        ,h1=h1
        ,h2=h2
        ,h3=h3
        ,h4=h4
        ,h5=h5
        ,h6=h6
        ,containsLogin=containsLogin
        ,htmlVersion=htmlVersion
        ,internalLinks=internalLinks
        ,externalLinks=externalLinks
        )
    #return __ToJson(url, title, h1, h2, h3, h4, h5, h6, internalLinks, externalLinks, containsLogin, htmlVersion)



        
