import unittest
import json
from ds_messanger import *

class test_ds_messanger(unittest.TestCase):
    def test_DirectMessage_class1(self):
        direct_message = DirectMessage()
        self.assertEqual(direct_message.message, None)

    
    def test_DirectMessage_class2(self):
        direct_message = DirectMessage()
        self.assertEqual(direct_message.timestamp, None)


    def test_DirectMessage_class3(self):
        direct_message = DirectMessage()
        self.assertEqual(direct_message.recipient, None)


    def test_DirectMessanger_all_messages(self):
        user1 = DirectMessenger('168.235.86.101', "isaip617777", "ginger2buck")
        user2 = DirectMessenger('168.235.86.101', "Ronaldo2222", "ginger")
        msg = user2.retrieve_all()
        self.assertEqual(bool(msg), True)

    def test_DirectMessanger_send_message(self):
        user1 = DirectMessenger('168.235.86.101', "isaip617777", "ginger2buck")
        value = user1.send('hello', 'Isaip617')
        self.assertTrue(value)

    
    def test_DirectMessanger_new_messages(self):
        user1 = DirectMessenger('168.235.86.101', "bob12345", "ginger2buck")
        user2 = DirectMessenger('168.235.86.101', "lebronjemes", "ginger")
        user1.send('hello', 'lebronjemes')
        msg = user2.retrieve_new()
        msg = msg[0]['message']
        self.assertEqual(msg, 'hello')
    
    def test_DirectMessanger_send_messages_error(self):
        user1 = DirectMessenger('168.235.86.101', "bob12345", "ginge")
        user1 = user1.send('hello', 'Isaip617')
        self.assertFalse(user1)