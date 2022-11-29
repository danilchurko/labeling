from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from serpapi import GoogleSearch
from pprint import pprint

import pandas as pd
import re
import time

mem_index = 0
limit = 5

df = pd.read_csv('book1.csv')  # file

# columns name
df = df.loc[:, 'MERCHANT NAME FOR GOOGLE SEARCH'] + ' ' + \
     df.loc[:, 'Original Transaction Descriptor (Use this field for reference)'].str[:-2] + ' ' + \
     df.loc[:, 'lowest_amount_descriptor'].str[-2:]

fin_list = []  # final list with search row
fin_list_tt = []  # final list with title and type of merchant

print(df)


def state_check(st):
    state = {'AK': 'Alaska',
             'AL': 'Alabama',
             'AR': 'Arkansas',
             'AS': 'American Samoa',
             'AZ': 'Arizona',
             'CA': 'California',
             'CO': 'Colorado',
             'CT': 'Connecticut',
             'DC': 'District of Columbia',
             'DE': 'Delaware',
             'FL': 'Florida',
             'GA': 'Georgia',
             'GU': 'Guam',
             'HI': 'Hawaii',
             'IA': 'Iowa',
             'ID': 'Idaho',
             'IL': 'Illinois',
             'IN': 'Indiana',
             'KS': 'Kansas',
             'KY': 'Kentucky',
             'LA': 'Louisiana',
             'MA': 'Massachusetts',
             'MD': 'Maryland',
             'ME': 'Maine',
             'MI': 'Michigan',
             'MN': 'Minnesota',
             'MO': 'Missouri',
             'MS': 'Mississippi',
             'MT': 'Montana',
             'NC': 'North Carolina',
             'ND': 'North Dakota',
             'NE': 'Nebraska',
             'NH': 'New Hampshire',
             'NJ': 'New Jersey',
             'NM': 'New Mexico',
             'NV': 'Nevada',
             'NY': 'New York',
             'OH': 'Ohio',
             'OK': 'Oklahoma',
             'OR': 'Oregon',
             'PA': 'Pennsylvania',
             'PR': 'Puerto Rico',
             'RI': 'Rhode Island',
             'SC': 'South Carolina',
             'SD': 'South Dakota',
             'TN': 'Tennessee',
             'TX': 'Texas',
             'UT': 'Utah',
             'VA': 'Virginia',
             'VI': 'Virgin Islands',
             'VT': 'Vermont',
             'WA': 'Washington',
             'WI': 'Wisconsin',
             'WV': 'West Virginia',
             'WY': 'Wyoming'}

    if st in state:
        return True
    else:
        return False


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
        result2 = ''.join([i for i in result2 if not i.isdigit()])

        result2 = result2.replace('*', ' ')
        result2 = result2.replace('#', ' ')
        result2 = result2.replace('--', ' ')
        result2 = result2.replace('-', ' ')

        result2 = re.sub(r'\s+', ' ', result2)
        result2 = ' '.join(unique_list(result2.split()))

        fin_list.append(result2)


def serp_api(search_row, location):
    params = {
        'q': search_row,
        'location': location + 'United States',
        'google_domain': 'google.com',
        'hl': 'en',
        'gl': 'us',
        'api_key': '47f73bf698c331bb37369d7a328fe47f2e74d5b3755f8231c43daca95a48c7b6'
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    if 'knowledge_graph' in results:
        knowledge_graph = results['knowledge_graph']
        print(knowledge_graph)

        if 'title' and 'type' in knowledge_graph:
            title = knowledge_graph['title']
            type_comp = knowledge_graph['type']

        elif 'title' in knowledge_graph:
            title = knowledge_graph['title']
            type_comp = '-'

        elif 'name' and 'extensions' in knowledge_graph['see_results_about'][0]:
            title = knowledge_graph['see_results_about'][0]['name']
            type_comp = knowledge_graph['see_results_about'][0]['extensions']

        else:
            print(results)
            title = '-'
            type_comp = '-'
    else:
        title = 'manual'
        type_comp = 'manual'


    # create check from aka file for merchant name

    return title, type_comp


def launch_browser(fin_list, mem_index):
    index = 0

    for itm in fin_list[mem_index:]:
        index += 1

        # Create check, is state exist
        #location = state(str(itm[-2:]))
        if state_check(str(itm[-2:])):
            location = str(itm[-2:]) + ', '
        else:
            location = ''

        title, type_comp = serp_api(itm, location)

        fin_list_tt.append(str(title) + '|' + str(type_comp))

        mem_index += 1

        if index == limit:
            break

    print(mem_index)
    pprint(fin_list_tt)
    return mem_index


def start():
    memi = launch_browser(fin_list, mem_index)

    if input('>>> ') == 'n':
        time.sleep(1)

    return memi


create_list()

print(fin_list)

for run in range(limit):
    mem_index = start()
