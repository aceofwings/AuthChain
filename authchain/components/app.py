
from authchain.tendermint.server import ABCIServer
from authchain.tendermint.application import BaseApplication, Result
from authchain.protobuf.types1_pb2 import ResponseInfo, ResponseQuery ,ResponseEndBlock
from authchain.protobuf.varint import encode, decode_bytes

class Application(BaseApplication):

    def start(self):
        self.server = ABCIServer(app=self)
        self.server.run()

    def info(self):
        r = ResponseInfo()
        r.last_block_height = 0
        r.last_block_app_hash = b''
        return r

    def query(self, reqQuery):
        """Return the last tx count"""
        v = encode(self.txCount)
        rq = ResponseQuery(
            code=0, key=b'count', value=v, height=self.last_block_height)
        return rq

    def __valid_input(self, tx):
        """Check to see the given input is the next sequence in the count"""
        value = decode_bytes(tx)
        return value == (self.txCount + 1)


    def init_chain(self, v):
        """Set initial state on first run"""
        self.txCount = 0
        self.last_block_height = 0

    def deliver_tx(self,tx):
        """Called to calculate state on a given block during the consensus process"""
        self.txCount += 1
        print(tx)
        return Result.ok(log='transaction passed',data=bytes([0x4]))


    def check_tx(self,tx):
        """Use to validate incoming transactions.  If Result.ok is returned,
        the Tx will be added to Tendermint's mempool"""

        print(" checking transaction")
        return Result.ok(log='thumbs up',data=bytes([0x4]))

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
