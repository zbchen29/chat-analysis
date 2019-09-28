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
    authentication = {}
    with open("authentication.json") as f:
        authentication = json.loads(f.read());
    return authentication["access_token"]

def get_chat_log_name():
    '''Get the name of the chat data file from authentication.json
    '''
    authentication = {}
    with open("authentication.json") as f:
        authentication = json.loads(f.read());
    return authentication["chat_data"]

def get_query_args(access_token, before_id=None, limit=100):
    '''Generates a appropriate dict of query parameters for GET request
    '''
    query_args = {
        "token" : access_token,
        "limit" : limit
    }
    if before_id != None:
        query_args["before_id"] = before_id

    return query_args

def is_valid_response(response):
    '''Returns whether if the end of messages has been reached
    '''
    return response.status_code == 200

def load_messages_from_file():
    '''Returns a list of messages loaded from relevant json file
    '''
    chat_data = None
    with open(get_chat_log_name()) as f:
        chat_data = json.loads(f.read())

    return chat_data

def save_messages_from_server():
    # Set up variables for requests
    url = get_endpoint()
    access_token = get_access_token()

    # List of all messages
    all_messages = []

    # Get the first page
    initial_query_args = get_query_args(access_token)
    current_res = requests.get(url, params=initial_query_args)
    if is_valid_response(current_res):
        current_data = current_res.json()
        all_messages.extend(current_data["response"]["messages"])
        next_id = current_data["response"]["messages"][-1]["id"]

    # Cycle through pages until the start
    cycles = 0
    while  is_valid_response(current_res):
        query_args = get_query_args(access_token, next_id)
        current_res = requests.get(url, params=query_args)
        if is_valid_response(current_res):
            current_data = current_res.json()
            all_messages.extend(current_data["response"]["messages"])
            next_id = current_data["response"]["messages"][-1]["id"]

            cycles += 1
            sleep(0.25)
            print("Retrieved cycle:", cycles)

    # Write to output file
    with open(get_chat_log_name(), "w") as out:
        json.dump(all_messages, out)

def count_message_frequency(messages):
    '''Returns a dictionary mapping most common aliases to their message count
    '''
    messages_per_person = {}
    id_to_person = get_id_to_name_map(messages, True)
    # Count messages total by name
    for m in messages:
        messages_per_person[id_to_person[m["user_id"]]] = messages_per_person.get(id_to_person[m["user_id"]], 0) + 1
    return messages_per_person

    messages_per_name = {}
    id_to_person = get_id_to_name_map(messages, True)
    name_to_id = get_name_to_id_map(messages)
    # Count message totals by name
    for m in messages:
        messages_per_name[m["name"]] = messages_per_name.get(m["name"], 0) + 1

    messages_per_person = {}
    for name, count in messages_per_name.items():
        messages_per_person[id_to_person[name_to_id[name]]] = messages_per_person.get(id_to_person[name_to_id[name]], 0) + count

    return messages_per_person

def count_favorites_given_frequency(messages):
    '''Returns a dictionary mapping most common aliases to their favorites given count
    '''
    favorites_per_person = {}
    id_to_person = get_id_to_name_map(messages, True)
    # Counts favorites by name
    for m in messages:
        for id in m["favorited_by"]:
            favorites_per_person[id_to_person[id]] = favorites_per_person.get(id_to_person[id], 0) + 1
    return favorites_per_person

def count_favorites_received_frequency(messages):
    '''Returns a dictionary mapping most common aliase to their favorites received count
    '''
    favorites_per_person = {}
    id_to_person = get_id_to_name_map(messages, True)
    # Counts favorites by name
    for m in messages:
        favorites_per_person[id_to_person[m["user_id"]]] = favorites_per_person.get(id_to_person[m["user_id"]], 0) + len(m["favorited_by"])
    return favorites_per_person

def get_name_to_id_map(messages):
    '''Returns a dictionary mapping names to ids
    '''
    name_to_id = {}
    for m in messages:
        if m["user_id"] not in name_to_id:
            name_to_id[m["name"]] = m["user_id"]
    return name_to_id

def get_id_to_name_map(messages, canonical=False):
    '''Returns a dictionary mapping ids to set of names
    '''
    if not canonical:
        id_to_name = {}
        for m in messages:
            if m["user_id"] not in id_to_name:
                id_to_name[m["user_id"]] = {m["name"]}
            else:
                id_to_name[m["user_id"]].add(m["name"])
        return id_to_name
    else:
        id_to_name_count = {}
        for m in messages:
            if m["user_id"] not in id_to_name_count:
                id_to_name_count[m["user_id"]] = {m["name"]:1}
            else:
                id_to_name_count[m["user_id"]][m["name"]] = id_to_name_count[m["user_id"]].get(m["name"], 0) + 1

        id_to_cannon_name = {}
        for id, names in id_to_name_count.items():
            cannon_name = max(names.items(), key=lambda x : x[1])[0]
            id_to_cannon_name[id] = cannon_name

        return id_to_cannon_name

def print_dict(dict):
    '''Cleanly prints the key, value pairs of a dictionary
    '''
    for key, item in dict.items():
        print(key, ":", item)

def main():
    # save_messages_from_server()

    messages = load_messages_from_file()
    print("Total Message Count:", len(messages))

    # print("\nMessage counts:")
    # print_dict(count_message_frequency(messages))
    # print("\nFavorites given:")
    # print_dict(count_favorites_given_frequency(messages))
    # print("\nFavorites received:")
    # print_dict(count_favorites_received_frequency(messages))

if __name__ == '__main__':
    main()
