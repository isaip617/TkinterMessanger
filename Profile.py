
import json, time
from pathlib import Path
from ds_messanger import *
from ds_protocol import *

"""
DsuFileError is a custom exception handler that you should catch in your own code. It
is raised when attempting to load or save Profile objects to file the system.

"""
class DsuFileError(Exception):
    pass

"""
DsuProfileError is a custom exception handler that you should catch in your own code. It
is raised when attempting to deserialize a dsu file to a Profile object.

"""
class DsuProfileError(Exception):
    pass


    
class Profile:

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver 
        self.username = username 
        self.password = password 
        self.messages_sent = {}
        self.messages_recieved = {}
        self.unread_messages = {}
        self.list_of_contacts = []


    def send_messages(self, message, recipient):
        new_user = DirectMessenger(self.dsuserver, self.username, self.password)
        x = new_user.send(message, recipient)
        if x == True:
            if recipient in self.messages_sent:
                self.messages_sent[recipient].append({'message': message, 'from': 'me', 'timestamp': time.time()})
            else:
                self.messages_sent[recipient] = [{'message': message, 'from': 'me', 'timestamp': time.time()}]
                if recipient not in self.list_of_contacts:
                    self.list_of_contacts.append(recipient)
    
    
    def retrieve_all_messages(self):
        new_user = DirectMessenger(self.dsuserver, self.username, self.password)
        list_of_objects = new_user.retrieve_all()
        for object in list_of_objects:
            friend = object.recipient
            if friend in self.messages_recieved:
                self.messages_recieved[friend] = []
        for object2 in list_of_objects:
            friend2 = object2.recipient
            if friend2 in self.messages_recieved:
                self.messages_recieved[friend2].append({'message': object2.message, 'from':friend2, 'timestamp': float(object2.timestamp)})
            else:
                self.messages_recieved[friend2] = [{'message': object2.message, 'from':friend2, 'timestamp': float(object2.timestamp)}]
                if friend2 not in self.list_of_contacts:
                    self.list_of_contacts.append(friend2)
    
    
    def retrieve_unread_messages(self):
        new_user = DirectMessenger(self.dsuserver, self.username, self.password)
        list_of_objects = new_user.retrieve_new()
        for object0 in list_of_objects:
            friend0 = object0.recipient
            if friend0 in self.messages_recieved:
                self.messages_recieved[friend0] = []
        for object in list_of_objects:
            friend = object.recipient
            if friend in self.unread_messages:
                self.unread_messages[friend].append({'message': object.message, 'from':friend, 'timestamp': object.timestamp})
            else:
                self.unread_messages[friend] = [{'message': object.message, 'from':friend, 'timestamp': object.timestamp}]
                if friend not in self.list_of_contacts:
                    self.list_of_contacts.append(friend)

    """

    save_profile accepts an existing dsu file to save the current instance of Profile 
    to the file system.

    Example usage:

    profile = Profile()
    profile.save_profile('/path/to/file.dsu')

    Raises DsuFileError

    """
    def save_profile(self, path: str) -> None:
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f, default=vars)
                f.close()
            except Exception as ex:
                raise DsuFileError("Error while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    """

    load_profile will populate the current instance of Profile with data stored in a 
    DSU file.

    Example usage: 

    profile = Profile()
    profile.load_profile('/path/to/file.dsu')

    Raises DsuProfileError, DsuFileError

    """
    def load_profile(self, path: str) -> None:
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.messages_sent = obj['messages_sent']
                self.messages_recieved = obj['messages_recieved']
                self.unread_messages = obj['unread_messages']
                self.list_of_contacts = obj['list_of_contacts']
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()

