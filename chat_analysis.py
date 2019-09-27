import requests
import json
from time import sleep

def get_endpoint():
    '''Retrieves endpoint from authentication.json
    '''
    authentication = {}
    with open("authentication.json") as f:
        authentication = json.loads(f.read());

    return "".join([authentication["endpoint"], "/",
                    authentication["group_id"], "/",
                    "messages"])

def get_access_token():
    '''Retrieves access_token from authentication.json
    '''
    token = ""
    with open("authentication.json") as f:
        authentication = json.loads(f.read());
    return authentication["access_token"]

def get_query_args(access_token, before_id):
    '''Generates a appropriate dict of query parameters for GET request
    '''
    return {
        "token" : access_token,
        "before_id" : before_id,
        "limit" : 100
    }

def messages_still_remain(response):
    '''Returns whether if the end of messages has been reached
    '''
    return response["meta"]["code"] != 304

def load_messages_from_file():
    '''Returns a list of messages loaded from relevant json file
    '''
    chat_data_filename = None
    with open("authentication.json") as f:
        authentication = json.loads(f.read())
        chat_data_filename = authentication["chat_data"]

    chat_data = None
    with open(chat_data_filename) as f:
        chat_data = json.loads(f.read())

    return chat_data

def main():

    url = get_endpoint()
    access_token = get_access_token()
    initial_query_args = {
        "token" : access_token,
        "limit" : 2
    }

    # List of all messages
    all_messages = []

    current_res = requests.get(url, params=initial_query_args).json()
    all_messages.extend(current_res["response"]["messages"][::-1])
    next_id = current_res["response"]["messages"][-1]["id"]

    cycles = 0

    while  messages_still_remain(current_res) and cycles < 2:
        query_args = get_query_args(access_token, next_id)
        current_res = requests.get(url, params=query_args).json()
        all_messages.extend(current_res["response"]["messages"][::-1])
        next_id = current_res["response"]["messages"][-1]["id"]

        cycles += 1
        sleep(1)

        print("Retrieved cycle:", cycles)

    with open("chat_log.json", "w") as out:
        json.dump(all_messages, out)

if __name__ == '__main__':
    main()
