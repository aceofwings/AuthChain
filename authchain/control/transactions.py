import requests
import logging
import json
import base64


URI = "http://localhost:46657"

class Transmitter(object):

    def __init__():
        pass

    def postCreateTransaction(self,transaction):
        payload = {
            'method': "CREATE",
            'jsonrpc': '2.0',
            'params': [Transaction.encode(transaction.to_dict())],
            'id': str(uuid4())
        }
        requests.post(url, json=payload)

class Transaction(object):

    inputs = []
    outputs = []

    @classmethod
    def encode(self,tx):
        return base64.b64encode(json.dumps(tx).encode('utf8')).decode('utf8')

    @classmethod
    def decode(cls, tx):
        return json.loads(tx.decode('utf8'))

    def decode_transaction_base64(value):
        """Decode a transaction from Base64."""
        return json.loads(base64.b64decode(value.encode('utf8')).decode('utf8'))

    def to_dict(self):
        return {cow : "1"}
