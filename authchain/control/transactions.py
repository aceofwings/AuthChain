import requests
import logging

class Transactions(object):

    def __init__():
        pass

    def postCreateTransaction(self,transaction):
        payload = {
            'method': "CREATE",
            'jsonrpc': '2.0',
            'params': [encode_transaction(transaction.to_dict())],
            'id': str(uuid4())
        }


class Transaction(object):
    pass
