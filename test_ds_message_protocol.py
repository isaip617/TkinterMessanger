import unittest
import json
from ds_protocol import *


class test_ds_protocol(unittest.TestCase):
    def test__extract_json(self):
        """test extract_json function."""
        json_message = {'response': {'token': 'hello'}}
        json_message = json.dumps(json_message)
        token1 = extract_json(json_message)
        token2 = token1.token
        self.assertEqual(token2, 'hello')

    def test__extract_json_error(self):
        """test extract_json function error."""
        json_message = "{'response': {'token': 'hello'"
        token1 = extract_json(json_message)
        self.assertRaises(json.JSONDecodeError)

    def test__directmessage(self):
        """test directmessage function."""
        token1 = "12345"
        message1 = "hello"
        recipeint = 'ronaldo'
        msg = directmessage(token1, message1, recipeint)
        msg2 = msg
        self.assertEqual(msg, msg2)
    

    def test_unread_message(self):
        """test request unread messages function."""
        token = '123456789'
        msg = request_unread_messages(token)
        msg2 = json.dumps({"token": token, "directmessage": "new"})
        self.assertEqual(msg, msg2)

    def test_request_all_messages(self):
        """test request all messages function."""
        token = '123456789'
        msg = request_all_messages(token)
        msg2 = json.dumps({"token": token, "directmessage": "all"})
        self.assertEqual(msg, msg2)


