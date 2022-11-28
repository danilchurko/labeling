from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import re
import time
import random

mem_index = 0
limit = 5

df = pd.read_csv("book.csv")  # file
df = df.loc[:, 'MERCHANT NAME FOR GOOGLE SEARCH'] + ' ' + df.loc[:, 'Original Transaction Descriptor (Use this field ' \
                                                                    'for reference)'] # columns

print(df)

fin_list = []  # final list with search row


#  List without dupes
def unique_list(dirt_list):
    ulist = []
    [ulist.append(x) for x in dirt_list if x not in ulist]
    return ulist


#  Creating list without spaces
def create_list():
    for row in df:
        result = re.sub(r'\s+', ' ', row)
        result2 = ' '.join(unique_list(result.split()))
        fin_list.append(result2)


def launch_browser(fin_list, mem_index):
    index = 0

    chrome_options = Options()
    chrome_options.add_argument("--incognito, detach")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    for itm in fin_list[mem_index:]:
        index += 1

        i_ns = itm.replace(" ", "+")
        driver.get('https://www.google.com/search?q=' + i_ns + '&gl=us&hl=en&pws=0&gws_rd=cr')

        if itm == fin_list[0]:
            time.sleep(5)
        else:
            time.sleep(random.randint(0, 2))

        driver.switch_to.new_window('tab')

        mem_index += 1

        if index == limit:
            break

    print(mem_index)
    return driver, mem_index


def start():
    drv, memi = launch_browser(fin_list, mem_index)

    if input('>>> ') == 'n':
        time.sleep(1)

    return drv, memi


create_list()

for run in range(len(fin_list)):
    driver, mem_index = start()
