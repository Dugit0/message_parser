#!/home/dmitry/IT/Fun/message_parser/venv/bin/python

from bs4 import BeautifulSoup
import enum
import os
from tqdm import tqdm


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
    pass


class Chat:
    # TODO
    pass


def get_all_message_files():
    chats_path = os.path.join("data", "chats")
    all_message_files = []
    for chat_name in os.listdir(chats_path):
        for file in os.listdir(os.path.join(chats_path, chat_name)):
            if file[-5:] == ".html":
                all_message_files.append(os.path.join(chats_path, chat_name, file))
    return all_message_files


def get_html_from_dir():
    pass

tmp = ["chat_001", "chat_002", "chat_003", "chat_004", "chat_005", "chat_006", "chat_007", "chat_008", "chat_009", "chat_010", "chat_011", "chat_012", "chat_013", "chat_014"]
tmp = ["chat_006"]
for q in tqdm(tmp):
    data_path = os.path.join("data", "chats", q)
    message_file_paths = [os.path.join(data_path, file) for file in os.listdir(data_path) \
                    if file[-5:] == ".html"]
    messages = []
    for message_file_path in message_file_paths:
        with open(message_file_path, encoding="utf-8") as message_file:
            soup = BeautifulSoup(message_file, "lxml")
        page_body = soup.body.div.find("div", class_="page_body").div
        # У сообщений возможны только классы: 'message', 'joined', 'service', 'clearfix', 'default'
        messages_from_file = page_body.find_all(lambda tag: \
                        tag.get("class") != None and "message" in tag.get("class") \
                        and not ("service" in tag.get("class")))
        messages.extend(messages_from_file)
    print(len(messages))

# for i in messages_list:
#     print(i)
#     print("--------------------------")
    # for i in range(5):
    #     print(messages_list_part[i].prettify())
    #     print("----------")


# with open("out.html", "w", encoding="utf-8") as f_out:
#     print(messages_list_part.prettify(), file=f_out)







