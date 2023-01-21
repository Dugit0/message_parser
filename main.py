#!/bin/python

from bs4 import BeautifulSoup
import enum


class MessageType(enum.Enum):
    voice = 1
    circle = 2
    call = 3
    sticker = 4
    common = 5


class Message:
    def __init__(self, soup, author):
        self.author = author
    pass


class Chat:
    pass


# def get_name()











data_path = r"data/messages.html"

with open(data_path) as data_file:
    soup = BeautifulSoup(data_file, "lxml")

# print(soup.prettify())






