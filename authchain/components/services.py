


class MessageShell(object):

    @classmethod
    def messageForType(cls,msg_type):
        return  {"type" : msg_type, "data": {}}

class MSGTYPE(object):
    REGISTER = "REGISTER"
    GRANT = "GRANT"
    DENY = "DENY"

def generate_service(service_keys, owner_keys,auth_keys,):
    """
    create a an unsigned service msg
    """
    message = MessageShell.messageForType(MSGTYPE.REGISTER)
    message =

def sign_service(service_hash,):
    pass

def broadcast_transaction():
    pass
