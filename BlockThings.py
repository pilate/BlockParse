from pprint import pprint

import datetime
import dtypes
import os
import sys


# Handle iterating through the block file
class BlockFileIterator(object):
    def __init__(self, file_name):
        self.stream = open(file_name, "rb")
        self.file_size = os.stat(file_name).st_size
        self.coinbase = Block(self.stream)
        self.blocks = []
        while self.stream.tell() < self.file_size:
            try:
                self.blocks.append(Block(self.stream))
            except:
                print sys.exc_info()
        print "End of File: {0} blocks".format(len(self.blocks))
        print self.blocks[-1].__dict__

# Parse an entire block
class Block(object):
    def __init__(self, stream):
        self.stream = stream
        self.magic = self.stream.read(4)
        self.block_len = dtypes.int32.unpack(self.stream)
        self.parse_header()
        self.tx_count = dtypes.varint.unpack(self.stream)
        self.transactions = []
        for _ in xrange(self.tx_count):
            self.transactions.append(Transaction(self.stream))
        #print "Block:", self.__dict__

    def parse_header(self):
        self.version = dtypes.int32.unpack(self.stream)
        self.hashPrevBlock = self.stream.read(32)
        self.hashMerkleRoot = self.stream.read(32)
        self.time = dtypes.int32.unpack(self.stream)
        self.bits = dtypes.int32.unpack(self.stream)
        self.nonce = dtypes.int32.unpack(self.stream)

# Parse a block transaction
class Transaction(object):
    def __init__(self, stream):
        self.stream = stream
        self.parse()

    def parse(self):
        self.version = dtypes.int32.unpack(self.stream)
        self.in_tx_count = dtypes.varint.unpack(self.stream)
        self.in_txs = []
        for _ in xrange(self.in_tx_count):
            self.in_txs.append(Input(self.stream))
        self.out_tx_count = dtypes.varint.unpack(self.stream)
        self.out_txs = []
        for _ in xrange(self.out_tx_count):
            self.out_txs.append(Output(self.stream))
        self.lock_time = dtypes.int32.unpack(self.stream)

class Output(object):
    def __init__(self, stream):
        self.stream = stream
        self.parse()
        #print "Output:", self.__dict__

    def parse(self):
        self.value = dtypes.uint64.unpack(self.stream)
        self.script_length = dtypes.varint.unpack(self.stream)
        self.script = self.stream.read(self.script_length)

class Input(object):
    def __init__(self, stream):
        self.stream = stream
        self.parse()
        #print "Input:", self.__dict__

    def parse(self):
        self.prev = self.stream.read(32)
        self.prev_txout_idx = dtypes.int32.unpack(self.stream)
        self.script_length = dtypes.varint.unpack(self.stream)
        self.script = self.stream.read(self.script_length)
        self.sequence = dtypes.int32.unpack(self.stream)