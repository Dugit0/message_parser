#!/bin/python

from bs4 import BeautifulSoup
import enum
import os


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









data_path = os.path.join("data", "chats", "chat_008", "messages.html")

with open(data_path, encoding="utf-8") as data_file:
    soup = BeautifulSoup(data_file, "lxml")
    messages_list = soup.body.div.find("div", class_="page_body").div.find_all(lambda tag: tag["id"][:7] == "message")
    for i in range(5):
        print(messages_list[i].prettify())
        print("----------")
    # with open("out.html", "w", encoding="utf-8") as f_out:
    #     print(messages_list.prettify(), file=f_out)



# print(soup.prettify())






