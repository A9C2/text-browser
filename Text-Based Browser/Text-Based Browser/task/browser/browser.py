import os
import requests
import sys
import validators
from bs4 import BeautifulSoup
from collections import deque
from colorama import Fore

if len(sys.argv) != 2:
    print("error: Invalid number of command-line arguments")
    exit()

saved_tabs_dir = sys.argv[1]
# saved_tabs_dir = "test-dir"
if not os.path.exists(saved_tabs_dir):
    os.mkdir(saved_tabs_dir)


def read_page_file(page_file_name):
    with open(f"{saved_tabs_dir}/{page_file_name}.txt", "r", encoding="utf-8") as f:
        return f.read()


def write_page_file(page_file_name, text):
    with open(f"{saved_tabs_dir}/{page_file_name}.txt", "w", encoding="utf-8") as f:
        f.write(text)


saved_pages = set()
previous_pages_stack = deque()
last_page_content = ""
while True:
    input_str = input()
    if input_str == "exit":
        exit()

    if input_str == "back":
        if len(previous_pages_stack) > 0:
            print(previous_pages_stack.pop())
            continue
    else:
        previous_pages_stack.append(last_page_content)
        last_page_content = ""

    if input_str in saved_pages:
        page_content = read_page_file(input_str)
        last_page = page_content
        print(page_content)
    else:
        url = "https://" + input_str if not input_str.startswith("https://") else input_str
        if not validators.url(url):
            print(f"error: Invalid URL: {url}")
            continue
        r = requests.get(url)
        if not r:
            print("error: Get request did not succeed")
            continue
        page_content = r.text
        soup = BeautifulSoup(page_content, "html.parser")
        TAGS = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "ul", "ol", "li"}
        text = ""
        for accepted_tag in TAGS:
            for tag in soup.find_all(accepted_tag):
                text += tag.get_text()
                print(Fore.BLUE + text if accepted_tag == "a" else text)
        write_page_file(input_str, text)
        last_page = text
