# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 16:27:04 2023

@author: Dmitry
"""

def get_all_message_classes():
    set_classes = set()
    for data_path in tqdm(get_all_message_files()):
        with open(data_path, encoding="utf-8") as data_file:
            soup = BeautifulSoup(data_file, "lxml")
            messages_list = soup.body.div.find("div", class_="page_body").div
            # messages_list = messages_list.find_all(\
            #     lambda tag: tag.get("class") != None and "message" in tag.get("class"))
            for tag in messages_list.children:
                try:
                    if tag.get("class") != None and "message" in tag.get("class"):
                        # print(set(tag.get("class")))
                        set_classes.update(set(tag.get("class")))
                except:
                    pass
    print(set_classes)