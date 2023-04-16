#!/home/dmitry/IT/Fun/message_parser/venv/bin/python

from bs4 import BeautifulSoup
import enum
import os
from tqdm import tqdm
import datetime


# class MessageType(enum.Enum):
#     default = 0
#     voice = 1
#     circle = 2
#     call = 3
#     sticker = 4
#     common = 5


class Message:
    def __init__(self, soup, author):
        # self.type = MessageType.default
        self.soup = soup
        self.author = author
        body = soup.find("div", class_="body")
        my_date_time = body.find("div", class_="date")["title"]
        self.datetime = datetime.datetime.strptime(my_date_time, "%d.%m.%Y %H:%M:%S %Z")


class Voice(Message):
    def __init__(self, soup, author):
        super().__init__(soup, author)

    pass


class Circle(Message):
    def __init__(self, soup, author):
        super().__init__(soup, author)

    pass


class Call(Message):
    pass


class Sticker(Message):
    pass


class Common(Message):
    pass


class Chat:
    def __init__(self, file_chat_name, real_name):
        self.chat_name = real_name
        soups = get_message_soups(file_chat_name)
        self.messages = []
        last_author = None
        for soup in soups:
            if not ("joined" in soup["class"]):
                name_tag = soup.find("div", class_="body").find("div", class_="from_name")
                name = name_tag.text.strip()
                last_author = name
                self.messages.append(Message(soup, name))
            else:
                assert last_author != None
                self.messages.append(Message(soup, last_author))


def get_all_message_files():
    chats_path = os.path.join("data", "chats")
    all_message_files = []
    for chat_name in os.listdir(chats_path):
        for file in os.listdir(os.path.join(chats_path, chat_name)):
            if file[-5:] == ".html":
                all_message_files.append(os.path.join(chats_path, chat_name, file))
    return all_message_files


def get_message_soups(chat):
    data_path = os.path.join("data", "chats", chat)
    message_file_paths = [os.path.join(data_path, file) for file in os.listdir(data_path) \
                          if file[-5:] == ".html"]
    message_soups = []
    for message_file_path in message_file_paths:
        with open(message_file_path, encoding="utf-8") as message_file:
            soup = BeautifulSoup(message_file, "lxml")
        page_body = soup.body.div.find("div", class_="page_body").div
        # У сообщений возможны только классы: 'message', 'joined', 'service', 'clearfix', 'default'
        messages_from_file = page_body.find_all(lambda tag: \
                                                    tag.get("class") != None and "message" in tag.get("class") \
                                                    and not ("service" in tag.get("class")))
        message_soups.extend(messages_from_file)
    return message_soups


def get_html_from_dir():
    pass


tmp_chats = ["chat_001", "chat_002", "chat_003", "chat_004", "chat_005", "chat_006", "chat_007", "chat_008", "chat_009",
             "chat_010", "chat_011", "chat_012", "chat_013", "chat_014"]
tmp_chats = ["chat_008"]

for chat_name in tmp_chats:
    chat = Chat(chat_name, "null")

for message in chat.messages:
    print(message.author, message.datetime)

# for i in messages_list:
#     print(i)
#     print("--------------------------")
# for i in range(5):
#     print(messages_list_part[i].prettify())
#     print("----------")


# with open("out.html", "w", encoding="utf-8") as f_out:
#     print(messages_list_part.prettify(), file=f_out)
