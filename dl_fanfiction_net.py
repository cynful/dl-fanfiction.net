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
import argparse

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

def find_storyid(author, title):
    """Find id number of story using author and title"""
    author_url = f'{URL}~{author}'
    try:
        soup = get_beautifulsoup(author_url)
        story_div = soup.find('div', {'data-title':title})
        story_id = story_div['data-storyid']
        return story_id
    except:
        print('Check input.', end='')

def main():
    """Prints all chapters of story given author's username without spaces and story title."""
    disable_warnings()
    parser = argparse.ArgumentParser(description='accept story author username without spaces, and story title')
    parser.add_argument('-author', '--username')
    parser.add_argument('-story', '--title')
    args = parser.parse_args()
    storyID = find_storyid(args.username, args.title)
    story_url = f'{URL}s/{storyID}'
    chapter = 1
    chapter_exists = True
    while chapter_exists:
        url = f'{story_url}/{str(chapter)}/'
        soup = get_beautifulsoup(url)
        print_soup(soup)
        chapter += 1
        chapter_exists = next_chapter_exists(soup)
        print()
        time.sleep(1)

if __name__ == "__main__":
    main()
