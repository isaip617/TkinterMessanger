import time
import socket
import json
from ds_protocol import *


class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None


class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.token = None
    self.port = 3021
    self.dsuserver = dsuserver
    self.username = username
    self.password = password
  def send(self, message:str, recipient:str) -> bool:
    # must return true if message successfully sent, false if send failed.
    SERVER = self.dsuserver
    PORT = self.port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER, PORT))
        send = client.makefile("w")
        recv = client.makefile("r")
        msg = json.dumps({"join": {"username": self.username, "password": self.password, "token": ""}})
        send.write(msg + "\r\n")
        send.flush()
        srv_msg = recv.readline()
        srv_msg_checker = json.loads(srv_msg)
        if srv_msg_checker["response"]["type"] == "error":
            print(f'ERROR: {srv_msg_checker["response"]["message"]}')
            x = False
        else:
            token1 = extract_json(srv_msg)
            self.token = token1.token
            message_to_send = directmessage(self.token, message, recipient)
            send.write(message_to_send + "\r\n")
            send.flush()
            x = True
    return x
  
  
  def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new messages
    SERVER = self.dsuserver
    PORT = self.port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER, PORT))
        send = client.makefile("w")
        recv = client.makefile("r")
        msg = json.dumps({"join": {"username": self.username, "password": self.password, "token": ""}})
        send.write(msg + "\r\n")
        send.flush()
        srv_msg = recv.readline()
        srv_msg_checker = json.loads(srv_msg)
        if srv_msg_checker["response"]["type"] == "error":
            return False
        else:
            token1 = extract_json(srv_msg)
            self.token = token1.token
            unread_messages_request = request_unread_messages(self.token)
            send.write(unread_messages_request + "\r\n")
            send.flush()
            srv_msg = recv.readline()
            srv_msg_checker = json.loads(srv_msg)
            if srv_msg_checker["response"]["type"] == "error":
                return False
            else:
                list_of_messages = []
                for num in range(len(srv_msg_checker['response']['messages'])):
                    user = DirectMessage()
                    user.message = srv_msg_checker['response']['messages'][num]['message']
                    user.recipient = srv_msg_checker['response']['messages'][num]['from']
                    user.timestamp = srv_msg_checker['response']['messages'][num]['timestamp']
                    list_of_messages.append(user)
                return list_of_messages
                

  def retrieve_all(self) -> list:
    # must return a list of DirectMessage objects containing all messages
    SERVER = self.dsuserver
    PORT = self.port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER, PORT))
        send = client.makefile("w")
        recv = client.makefile("r")
        msg = json.dumps({"join": {"username": self.username, "password": self.password, "token": ""}})
        send.write(msg + "\r\n")
        send.flush()
        srv_msg = recv.readline()
        srv_msg_checker = json.loads(srv_msg)
        if srv_msg_checker["response"]["type"] == "error":
            return False
        else:
            token1 = extract_json(srv_msg)
            self.token = token1.token
            all_messages_request = request_all_messages(self.token)
            send.write(all_messages_request + "\r\n")
            send.flush()
            srv_msg = recv.readline()
            srv_msg_checker = json.loads(srv_msg)
            if srv_msg_checker["response"]["type"] == "error":
                print(f'ERROR: {srv_msg_checker["response"]["message"]}')
                x = False
            else:
                list_of_messages = []
                for num in range(len(srv_msg_checker['response']['messages'])):
                    user = DirectMessage()
                    user.message = srv_msg_checker['response']['messages'][num]['message']
                    user.recipient = srv_msg_checker['response']['messages'][num]['from']
                    user.timestamp = srv_msg_checker['response']['messages'][num]['timestamp']
                    list_of_messages.append(user)
                return list_of_messages