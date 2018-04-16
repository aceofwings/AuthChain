import unittest
from authchain.components import services
from authchain.components import crypto
from cryptoconditions import Ed25519Sha256,ThresholdSha256
from authchain.control.transactions import Transaction


class TestServices(unittest.TestCase):

    def setUp(self):
        self.service = crypto.generate_key_pair()
        self.alice = crypto.generate_key_pair()
        self.bob = crypto.generate_key_pair()
        self.singleMessage = services.generate_service(self.service.public_key, [self.alice.public_key])
        self.multimessage = services.generate_service(self.service.public_key, [self.alice.public_key,self.bob.public_key])
        self.signedmessage = services.sign_service(self.singleMessage, [self.alice.private_key])
        self.signedmultimessage = services.sign_service(self.multimessage, [self.alice.private_key, self.bob.private_key])


    def tearDown(self):
        pass


    def test_TransactionFromDict(self):
        Transaction.CREATETransactionFromDict(self.signedmessage)

    def test_MultiCondtionTransactionFromDict(self):
        pass
        #Transaction.CREATETransactionFromDict(self.signedmultimessage)
