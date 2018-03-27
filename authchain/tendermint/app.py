from abci import BaseApplication, Result , ABCIServer


class Application(BaseApplication):

    def start(self):
        self.server = ABCIServer(app=self)
        self.server.start()

    def info(self):
        """ Called by ABCI when the app first starts. A stateful application
        should alway return the last blockhash and blockheight to prevent Tendermint
        replaying from the beginning. If blockheight == 0, Tendermint will call init_chain
        """
        return super().info()

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
        return super().end_block()

    def commit(self):
        """Called to get the result of processing transactions.  If this is a
        stateful application using a Merkle Tree, this method should return
        the root hash of the Merkle Tree in the Result data field"""
        return super().commit()
