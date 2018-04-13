
from cryptoconditions import Ed25519Sha256,ThresholdSha256
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


    return message



def sign_service(message,owner_priv_keys):
    """
    finalize the generated service message by adding condition attributes

    Args:
        message(dict) - a dictionary representing an unsigned attribute.
        owner_priv_keys([str]) - list of owner base58 private keys that will be used to create the conditions
        fullfillments([fullfillments]) -list of fullfillments needed to be fullfilled by the private keys
        returns :
            a message with fullfilled conditions representing a valid creation transaction
    raises:
        Invalid public private key pairing
        Insufficient private keys
    """
    fulfillment = None

    message = json.dumps(
        message,
        sort_keys=True,
        separators=(',', ':'),
        ensure_ascii=False,
    )

    encoded_message = sha3.sha3_256(message.encode())

    if len(owner_priv_keys) == 1:
        fulfillment =  ThresholdSha256(threshold=len(owner_priv_keys))
        for key in owner_priv_keys:
            f = Ed25519Sha256()
            f.sign(message.encode(), base58.b58decode(key))
            fulfillment.add_subfulfillment(f)
    else:
        fulfillment = Ed25519Sha256()
        fulfillment.sign(message.encode(),base58.b58decode(owner_priv_keys[0]))







def broadcast_transaction(messsage):
    """

    """
    pass
