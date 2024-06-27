# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Isai Perez
# isaip@uci.edu
# 75292336

import json
from Profile import *
from collections import namedtuple
import time
# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
DataTuple = namedtuple('DataTuple', ['token'])

def extract_json(json_msg: str) -> DataTuple:
    """Extract the Json."""
    '''
    Call the json.loads function on a json string and convert it to a DataTuple object
    '''
    try:
        json_obj = json.loads(json_msg)
        token = json_obj["response"]['token']
        return DataTuple(token)
    except json.JSONDecodeError:
        print("Json cannot be decoded.")


def directmessage(token:str, message:str, recipient:str) -> str:
    """Wrap directmessage in Json Format."""
    timestamp = time.time()
    msg = json.dumps({"token": token, "directmessage": {"entry": message, 'recipient': recipient, "timestamp": timestamp}})
    return msg

def request_unread_messages(token: str) -> str:
    """Wrap json messages to see Unread messages from server."""
    msg = json.dumps({"token": token, "directmessage": "new"})
    return msg

def request_all_messages(token: str) -> str:
    """Wrap json messages to see all messages from server."""
    msg = json.dumps({"token": token, "directmessage": "all"})
    return msg