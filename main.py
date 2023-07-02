#!/home/dmitry/IT/Fun/message_parser/venv/bin/python
from bs4 import BeautifulSoup
import enum
import sys
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

# class ChatType(enum.Enum):
#     default = 0

# Base class for all messages

class Message:
    """
    :param _soup: source soup, protected
    :type _soup: bs4.element.Tag
    :param author: author of message
    :type author: str
    :param datetime: sending date and time of message
    :type datetime: datetime.datetime
    """
    __DATE_FORMAT = "%d.%m.%Y %H:%M:%S %Z"

    def __init__(self, soup, author, media=False):
        # self.type = MessageType.default
        self._soup = soup
        self.author = author
        body = soup.find("div", class_="body")
        my_date_time = body.find("div", class_="date")["title"]
        self.datetime = datetime.datetime.strptime(my_date_time, self.__DATE_FORMAT)


class Voice(Message):
    """
    :param duration: duration of message (in seconds)
    :type duration: int
    """
    def __init__(self, soup, author):
        super().__init__(soup, author)
        media_wrap = self._soup.find(class_="body").find(class_="media_wrap")
        voice_status_text = media_wrap.find(class_="media_voice_message").find(class_="body").find(class_="status")
        voice_status_text = voice_status_text.text.strip()
        voice_duration_text = voice_status_text.split(", ")[0]
        if len(voice_duration_text) > 5:
            print("Really? Voice message longer than 1 hour??", file=sys.stderr)
            sys.exit(1)
        minutes, seconds = map(int, voice_duration_text.split(":"))
        self.duration = minutes * 60 + seconds


class Circle(Message):
    """
    :param duration: duration of message (in seconds)
    :type duration: int
    """
    def __init__(self, soup, author):
        super().__init__(soup, author)
        media_wrap = self._soup.find(class_="body").find(class_="media_wrap")
        video_status_text = media_wrap.find(class_="media_video").find(class_="body").find(class_="status")
        video_status_text = video_status_text.text.strip()
        video_duration_text = video_status_text.split(", ")[0]
        if len(video_duration_text) > 5:
            print("Really? Circle message longer than 1 hour??", file=sys.stderr)
            sys.exit(1)
        minutes, seconds = map(int, video_duration_text.split(":"))
        self.duration = minutes * 60 + seconds


class Call(Message):
    """
    :param duration: duration of call (in seconds) (-1 if no duration)
    :type duration: int
    :param call_status: call status (Incoming, Outgoing, Cancelled, Declined)
    :type call_status: str
    """
    def __init__(self, soup, author):
        super().__init__(soup, author)
        media_wrap = self._soup.find(class_="body").find(class_="media_wrap")
        call_status_text = media_wrap.find(class_="media_call").find(class_="body").find(class_="status")
        call_status_text = call_status_text.text.strip()
        # Cancelled - отмененный
        self.call_status = call_status_text.split()[0]
        print(call_status_text)
        left_ind = call_status_text.find("(")
        if left_ind == -1:
            self.duration = -1
        else:
            right_ind = call_status_text.find(")")
            time = call_status_text[left_ind + 1:right_ind]
            self.duration = int(time.split()[0])


class Animation(Message):
    # GIF animation
    def __init__(self, soup, author):
        super().__init__(soup, author)


class Sticker(Message):
    def __init__(self, soup, author):
        super().__init__(soup, author)


class Poll(Message):
    def __init__(self, soup, author):
        super().__init__(soup, author)
    pass


class Common(Message):
    def __init__(self, soup, author):
        super().__init__(soup, author)
    pass


class Forwarded(Message):
    def __init__(self, soup, author):
        super().__init__(soup, author)

    pass


class Chat:
    """
    :param chat_name: name of chat
    :type chat_name: str
    :param messages: list of messages
    :type messages: list of class Message children
    """
    def __init__(self, file_chat_name):
        self.chat_name = get_real_chat_name(file_chat_name)
        soups = get_message_soups(file_chat_name)
        self.messages = []
        name = None
        for soup in soups:
            if not ("joined" in soup["class"]):
                name_tag = soup.find("div", class_="body").find("div", class_="from_name")
                name = name_tag.text.strip()
            assert not (name is None)
            self.messages.append(create_message(soup, name))


def get_all_message_files():
    #TODO: сделать параметр, от которого будет строиться путь к выгруженным сообщениям
    # (т.е. предусмотреть случай, когда main.py и data лежат в разных местах)
    """
    :return: All paths for message file in all chats
    """
    chats_path = os.path.join("data", "chats")
    all_message_files = []
    for chat_name in os.listdir(chats_path):
        for file in os.listdir(os.path.join(chats_path, chat_name)):
            if file[-5:] == ".html":
                all_message_files.append(os.path.join(chats_path, chat_name, file))
    return all_message_files


def get_message_soups(chat):
    """
    :param chat: chat for getting message from itself
    :return: list of not service message soups
    """
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


def get_real_chat_names():
    """
    :return: dict in format "chat_01" : "real_name" (number of zeros depended on size max chat number)
    """
    list_chats_file_path = os.path.join("data", "lists", "chats.html")
    with open(list_chats_file_path, encoding="utf-8") as list_chats_file:
        soup = BeautifulSoup(list_chats_file, "lxml")
    chats_lists = soup.body.find("div", class_="page_wrap").find("div", class_="page_body")
    chats_lists = chats_lists.find_all("div", class_="entry_list")
    all_chats = []
    for chats_list in chats_lists:
        all_chats.extend(chats_list.find_all(class_="entry"))
    max_len = len(str(len(all_chats)))
    res_dict = dict()
    for i in range(len(all_chats)):
        real_name = all_chats[i].find(class_="body").find(class_="name").text.strip()
        res_dict[f"chat_{i + 1:0{max_len}}"] = real_name
    return res_dict


def get_real_chat_name(chat_name):
    """
    :param chat_name:
    :return: real chat name
    """
    global REAL_CHAT_NAMES
    return REAL_CHAT_NAMES[chat_name]


def create_message(soup, author):
    media_wrap = soup.find("div", class_="media_wrap")
    if media_wrap is None:
        return Message(soup, author)
        # print("media_wrap is None")
        # sys.exit(1)
    else:
        if media_wrap.find("div", class_="media") is None:
            # TODO rewrite on logger
            print("Media classes is None", file=sys.stderr)
            print("Maybe is poll?", file=sys.stderr)
            return Message(soup, author)
            # deb_message = Message(soup, author)
            # print(deb_message.author, deb_message.datetime, file=sys.stderr)
            # print(deb_message._soup, file=sys.stderr)
            # sys.exit(1)
        media_classes = media_wrap.find("div", class_="media")["class"]
        if "media_photo" in media_classes:
            title = media_wrap.find(class_="media").find(class_="body").find(class_="title").text.strip()
            if title == "Sticker":
                return Sticker(soup, author)
            elif title == "Photo":
                return Common(soup, author)
            else:
                print(f"Not common and not sticker photo file:\nTitle is {title}", file=sys.stderr)
                deb_message = Message(soup, author)
                print(deb_message.author, deb_message.datetime, file=sys.stderr)
                return deb_message
                # sys.exit(1)
        elif "media_video" in media_classes:
            title = media_wrap.find(class_="media").find(class_="body").find(class_="title").text.strip()
            if title == "Video file":
                return Common(soup, author)
            elif title == "Video message":
                return Circle(soup, author)
            elif title == "Animation":
                return Animation(soup, author)
            else:
                print(f"Not common and not circle video file:\nTitle is {title}", file=sys.stderr)
                deb_message = Message(soup, author)
                print(deb_message.author, deb_message.datetime, file=sys.stderr)
                return deb_message
                # sys.exit(1)
        elif "media_call" in media_classes:
            return Call(soup, author)
        elif "media_voice_message" in media_classes:
            return Voice(soup, author)
        elif "media_file" in media_classes:
            return Message(soup, author)
        elif "media_audio_file" in media_classes:
            return Message(soup, author)
        elif "media_poll" in media_classes:
            return Message(soup, author)
        else:
            print("Message class not found! {message.author, message.datetime}", file=sys.stderr)
            print(media_classes, file=sys.stderr)
            sys.exit(1)


def init():
    """
    Init global variable and prepare program to start
    :return:
    """
    global REAL_CHAT_NAMES
    REAL_CHAT_NAMES = get_real_chat_names()
    # print(REAL_CHAT_NAMES)


# ======================================================================================================================
init()

# tmp_chats = ["chat_001", "chat_002", "chat_003", "chat_004", "chat_005", "chat_006", "chat_007", "chat_008", "chat_009", "chat_010", "chat_011", "chat_012", "chat_013", "chat_014"]
# tmp_chats = ["chat_005", "chat_006", "chat_007", "chat_008", "chat_009", "chat_010"]
tmp_chats = ["chat_008"]
# tmp_chats = ["chat_001", "chat_002", "chat_008"]

for chat_name in tmp_chats:
    chat = Chat(chat_name)

for message in chat.messages:
    # print(message.author, message.datetime)
    pass
    # if isinstance(message, Call):
    #     print(message.author, message.datetime)
    #     print(message.call_status, message.duration)

# if __name__ == "__main__":
#     init()
