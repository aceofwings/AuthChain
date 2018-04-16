import requests
import logging
import json
import base64

from cryptoconditions import Ed25519Sha256, ThresholdSha256, Fulfillment

"""
Modes of transaction

broadcast_tx_async

"""
URI = "http://localhost:46657"

class Transmitter(object):


    MODE_LIST = ('broadcast_tx_async',
                 'broadcast_tx_sync',
                 'broadcast_tx_commit')

    def __init__():
        pass

    def postCreateTransaction(self,transaction,mode):
        """

        """
        payload = {
            'mode': "CREATE",
            'jsonrpc': '2.0',
            'params': [Transaction.encode(transaction.to_dict())],
            'id': str(uuid4())
        }
        requests.post(url, json=payload)

class Transaction(object):

    condition= None
    fullfillment = None
    owners = None
    service = None
    auths = None


    def __init__(self):
        pass

    @classmethod
    def CREATETransactionFromDict(cls,dictionary):
        transaction = Transaction()
        try:
            if dictionary["data"]["condition"]["type"] == Ed25519Sha256.TYPE_NAME:
                transaction.condition = dictionary['data']["condition_uri"]
            elif dictionary["data"]["condition"]["type"] == ThresholdSha256.TYPE_NAME:
                transaction.condition = dictionary['data']["condition_uri"]
            else:
                raise InvalidCreateTransaction()

            transaction.fullfillment = Fulfillment.from_uri(dictionary["data"]["fulfillment_uri"])

        except:
            raise InvalidCreateTransaction()
        return transaction


    @classmethod
    def AUTHORIZETransactionFromDict(cls,dictionary):
        pass
    @classmethod
    def REMOVETransactionFromDict(cls,dictionary):
        pass
    @classmethod
    def verifyTransaction(cls,transaction):
        pass







class Message(object):

    message = None

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

class InvalidCreateTransaction(Exception):
    pass
