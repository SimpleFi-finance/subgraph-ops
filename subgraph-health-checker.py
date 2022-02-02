import requests
import json



BASE_QUERY = """{ indexingStatusForCurrentVersion
        (subgraphName: \"simplefi-finance/<SUBGRAPH_NAME>\") 
        { subgraph health synced fatalError { message } nonFatalErrors {message} } 
        }"""


ONE_QUERY = """{ indexingStatusForCurrentVersion
        (subgraphName: \"simplefi-finance/oneinch\") 
        { subgraph health synced fatalError { message } nonFatalErrors {message} } 
        }"""



GRAPH_INDEX_URL = 'https://api.thegraph.com/index-node/graphql'
#SUBGRAPH_URL = 'https://api.thegraph.com/subgraphs/name/gvladika/simplefi-sushiswap-farms'

def check_subgraph_status(subgraph_name):
    print(subgraph_name)

    query = BASE_QUERY.replace("<SUBGRAPH_NAME>", subgraph_name)
    resp = requests.post(GRAPH_INDEX_URL, json={'query': query})

    if resp.status_code != 200:
        print("Response code:", resp.status_code)
        print('')
        return

    resp_json = json.loads(resp.text)

    health = resp_json['data']['indexingStatusForCurrentVersion']['health']
    print("Health:", health)

    if health != 'healthy':
        error = resp_json['data']['indexingStatusForCurrentVersion']['fatalError']['message']
        print('Error:', error)
    print('')

with open("production-subgraphs.txt", "r") as subgraph_list:
    for line in subgraph_list:
        check_subgraph_status(line.rstrip("\n"))





