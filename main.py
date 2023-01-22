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


def get_all_message_files():
    chats_path = os.path.join("data", "chats")
    all_message_files_list = []
    for chat_num in os.listdir(chats_path):
        for file in os.listdir(os.path.join(chats_path, chat_num)):
            if file[-5:] == ".html":
                all_message_files_list.append(os.path.join(chats_path, chat_num, file))
    print(all_message_files_list)

# =============================================================================
# data_path = os.path.join("data", "chats", "chat_008", "messages.html")
# 
# with open(data_path, encoding="utf-8") as data_file:
#     soup = BeautifulSoup(data_file, "lxml")
#     messages_list = soup.body.div.find("div", class_="page_body").div
# 
#     messages_list = messages_list.find_all(\
#         lambda tag: tag.get("class") != None and "message" in tag.get("class"))
#     for i in range(5):
#         print(messages_list[i].prettify())
#         print("----------")
# =============================================================================



    # with open("out.html", "w", encoding="utf-8") as f_out:
    #     print(messages_list.prettify(), file=f_out)


# print(soup.prettify())






