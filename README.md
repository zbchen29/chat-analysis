# GroupMe Chat Analysis
Suite of functions for parsing and analyzing GroupMe group chat data from servers or from a local file.  Performs sentiment analysis, message aggregation, alias retrieval, etc.

### Sentiment Analysis
```
def get_person_average_sentiment(messages, ignore_zero=False, analyzer="default"):
    '''Returns a dictionary mapping most common aliases to their average sentiment'''
```

### Message Aggregation
```
def save_messages_from_server():
    '''Saves messages to a local JSON file specified in authentication.json'''
```
```
def load_messages_from_file():
    '''Returns a list of messages loaded from relevant json file'''
```
```
def get_person_to_texts(messages):
    '''Returns a dictionary mapping most common aliases to their messages'''
```
```
def count_message_frequency(messages):    
    '''Returns a dictionary mapping most common aliases to their message count'''    
```
```
def count_favorites_given_frequency(messages):
    '''Returns a dictionary mapping most common aliases to their favorites given count'''
```
```
def count_favorites_received_frequency(messages):
    '''Returns a dictionary mapping most common aliases to their favorites received count'''
```

### Alias Retrieval

```
def get_id_to_name_map(messages, canonical=False):
    '''Returns a dictionary mapping ids to set of names, or a single canonical name'''
```
