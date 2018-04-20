
from cryptoconditions import Ed25519Sha256,ThresholdSha256
from authchain.control.transactions import Transaction
from copy import deepcopy

import sha3
import json
import base58


class MessageShell(object):

    @classmethod
    def messageForType(cls,msg_type):
        return  {"type" : msg_type, "data": {}}


class MSGTYPE(object):
    """
    Class encompassing message types
    """
    REGISTER = "REGISTER"
    GRANT = "GRANT"
    DENY = "DENY"

def generate_service(service_key, owner_keys, auth_keys = [], owners_authorize = True):
    """
    create a an unsigned service msg
    Args:
        service_keys ([str])- service denoted by base58 encoded keys
        owner_keys ([str]) - public keys recognizing ownership of the services and therefore administrators
        auth_keys ([str])- those who can give access to a resource. Generally owners must also be authorizers

        returns:
            a message without any signature or identity resolution
    """
    message = MessageShell.messageForType(MSGTYPE.REGISTER)
    message['data']['service'] = service_key
    message['data']['owners'] = owner_keys
    if owners_authorize:
        message['data']['authorities'] = owner_keys + auth_keys
    else:
        message['data']['authorities'] = auth_keys

    condition = None

    if len(owner_keys) != 1:
        condition = ThresholdSha256(threshold=len(owner_keys))
        for key in owner_keys:
            condition.add_subfulfillment(Ed25519Sha256(public_key= base58.b58decode(key)))
    else:
        condition = Ed25519Sha256(public_key= base58.b58decode(owner_keys[0]))

    message['data']['condition']  = condition.to_dict()
    message['data']['condition_uri'] = condition.condition_uri
    message['data']['fulfillment'] = None
    message['id'] = None


    return message



def sign_service(message,owner_priv_keys):
    """
    finalize the generated service message by adding condition attributes

    Args:
        message(dict) - a dictionary representing an unsigned attribute.
        owner_priv_keys([str]) - list of owner base58 private keys that will be used to create the conditions
        fulfillments([fulfillments]) -list of fulfillments needed to be fulfilled by the private keys
        returns :
            a message with fulfilled conditions representing a valid creation transaction
    raises:
        Invalid public private key pairing
        Insufficient private keys
    """
    fulfillment = None

    jsonMessage = json.dumps(
        message,
        sort_keys=True,
        separators=(',', ':'),
        ensure_ascii=False,
    )

    encoded_message = sha3.sha3_256(jsonMessage.encode())

    message['data']['fulfillment'] = {}

    if len(owner_priv_keys) == 1:
        fulfillment = ThresholdSha256(threshold=len(owner_priv_keys))
        message['data']['fulfillment']['type'] = ThresholdSha256.TYPE_NAME
        for key in owner_priv_keys:
            f = Ed25519Sha256()
            f.sign(encoded_message.digest(), base58.b58decode(key))
            fulfillment.add_subfulfillment(f)
    else:
        fulfillment = Ed25519Sha256()
        fulfillment.sign(encoded_message.digest() ,base58.b58decode(owner_priv_keys[0]))
        message['data']['fulfillment']['type'] = Ed25519Sha256.TYPE_NAME

    message['data']['fulfillment']['fulfillment_uri'] = fulfillment.serialize_uri()
    message['id'] = encoded_message.hexdigest()
    return message


def validateTransactionId(msg_wo_fulfull):
    tx = deepcopy(msg_wo_fulfull)
    proposed_tx_id = msg_wo_fulfull['id']
    tx['id'] = None
    jsonMessage = json.dumps(
            tx,
            sort_keys=True,
            separators=(',', ':'),
            ensure_ascii=False,
        )

    tx_id = sha3.sha3_256(jsonMessage.encode())

    if proposed_tx_id == tx_id.hexdigest():
        return True
    else:
        return False





def verifyService(message):
    """
    Args:
        message - Dictionary(hash) representing the serivce message to verify \

    returns:
        Boolean - True if the messages is correct and meets conditions otherwise false
    """
    transaction = Transaction.CREATETransactionFromDict(message)
    MessageWithoutFulfillment =  Transaction.REMOVETransactionFromDict(message)

    print(validateTransactionId(MessageWithoutFulfillment))

    jsonMessage = json.dumps(
        MessageWithoutFulfillment,
        sort_keys=True,
        separators=(',', ':'),
        ensure_ascii=False,
    )
    tx_id = sha3.sha3_256(jsonMessage.encode())

    if transaction.fulfillment.TYPE_NAME == ThresholdSha256.TYPE_NAME:
        if transaction.fulfillment.validate(tx_id.digest()):
            return True
    elif transaction.fulfilment.TYPE_NAME == Ed25519Sha256.TYPE_NAME:
        if transaction.fulfillment.validate(tx_id):
            return True
    else:
        return False


    return False








def broadcast_transaction(messsage):
    """

    """
    pass
