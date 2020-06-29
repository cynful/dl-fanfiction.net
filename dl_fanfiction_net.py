#!/usr/bin/env python
"""Scrape fanfiction.net html and create a pdf of ebook.
Todo:
    * argparse for author and story title
    * switch print_soup to pdf format
    * support ebook format
"""
import requests
import urllib3
import bs4
import time

URL = 'http://fanfiction.net/'

def disable_warnings():
    """Disables InsecureRequestWarning thrown by requests when getting untrusted SSL certifcate."""
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_beautifulsoup(url):
    """Get beautifulsoup from given url.

    Args:
        url (string): complete fanfiction.net url

    Returns:
        A beautifulsoup object.
    """
    # Set verify=False for fanfiction.net untrusted SSL cert
    result = requests.get(url, verify=False)
    html = result.content
    soup = bs4.BeautifulSoup(html, "html.parser")
    return soup

def print_soup(soup):
    """Prints paragraphs in beautifulsoup.

    Args:
        soup (beautifulsoup): beautifulsoup object from url
    """
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        print(paragraph.getText())

def next_chapter_exists(soup):
    """check if page has a next chapter button"""
    buttons = soup.find_all('button')
    for button in buttons:
        if button.getText() == 'Next >':
            return True

def main():
    """Prints first chapter of storyID:7241166."""
    disable_warnings()
    chapter = 1
    chapter_exists = True
    while chapter_exists:
        url = f'{URL}s/7241166/' + str(chapter) + '/Lord-Charming'
        soup = get_beautifulsoup(url)
        print_soup(soup)
        chapter += 1
        chapter_exists = next_chapter_exists(soup)
        time.sleep(1)

if __name__ == "__main__":
    main()
