from serpapi import GoogleSearch
from pprint import pprint

def serp_api(search_row, location):
    params = {
        'q': search_row,
        'location': location + ', United States',
        'google_domain': 'google.com',
        'hl': 'en',
        'gl': 'us',
        'api_key': '7e17865fc0010b82eb3dbc9e6107fcd274a22de57e3d610664fdbc8bec698c92'
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    pprint(results)

    if 'knowledge_graph' in results:
        knowledge_graph = results['knowledge_graph']
        # print(knowledge_graph)

        if 'title' and 'type' in knowledge_graph:
            title = knowledge_graph['title']
            type_comp = knowledge_graph['type']

        elif 'title' in knowledge_graph:
            title = knowledge_graph['title']
            type_comp = ''

        elif 'name' and 'extensions' in knowledge_graph['see_results_about'][0]:
            title = knowledge_graph['see_results_about'][0]['name']
            type_comp = knowledge_graph['see_results_about'][0]['extensions']

        else:
            title = '-'
            type_comp = '-'
    else:
        title = 'manual'
        type_comp = 'manual'

    return title, type_comp


row = 'TORONTO PARKING AUTHORITY AUTHORITYTORONTO ON'
loc = 'ON'

print(serp_api(row, loc))
