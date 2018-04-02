
from authchain.tendermint.server import ABCIServer
from authchain.tendermint.application import BaseApplication, Result
from authchain.protobuf.types1_pb2 import ResponseInfo, ResponseQuery ,ResponseEndBlock

class Application(BaseApplication):

    def start(self):
        self.server = ABCIServer(app=self)
        self.server.run()

    def info(self):
        r = ResponseInfo()
        r.last_block_height = 0
        r.last_block_app_hash = b''
        return r


    def deliver_tx(self,tx):
        """Called to calculate state on a given block during the consensus process"""
        return super().deliver_tx(self,tx)

    def check_tx(self,tx):
        """Use to validate incoming transactions.  If Result.ok is returned,
        the Tx will be added to Tendermint's mempool"""
        return super().deliver_tx(self,tx)

    def end_block(self,height):
        """Called at the end of processing. If this is a stateful application
        you can use the height from here to record the last_block_height"""
        self.last_block_height = height
        return ResponseEndBlock()

    def commit(self):
        """Called to get the result of processing transactions.  If this is a
        stateful application using a Merkle Tree, this method should return
        the root hash of the Merkle Tree in the Result data field"""
        return super().commit()
