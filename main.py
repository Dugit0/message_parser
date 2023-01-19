#!/bin/python

from bs4 import BeautifulSoup

data_path = r"data/messages.html"

with open(data_path) as data_file:
    soup = BeautifulSoup(data_file, "lxml")

# print(soup.prettify())






