from opcodes import *

import cStringIO
import dtypes
import sys


example_out_script = "76a9141f1e8fd68ceb82f36c4df76b38b72dcda79acd8488ac".decode("hex")
example_in_script = "483045022046a36839568ab33126657f385e80c634a9c5588a6516db3a19746803c68c80180221008862e528bbd4cdc93a80353d45dfe5e3d31621fb783d69106c17da9a4a43c9c001210280f03066edf9629b03e64e9b3819213b7ead05d937cc88bf313f5dfbc830acaf".decode("hex")




def disassemble(script):
    disassembly = []
    stream = cStringIO.StringIO(script) 
    while stream.tell() < len(script):
        opcode = dtypes.uint8.unpack(stream)

        # Raw Stack Push (Input TXs)
        if (opcode > RAW_PUSH_START) and (opcode < RAW_PUSH_STOP):
            push_data = stream.read(opcode)
            print "RAW_PUSH: {0}".format(push_data.encode("hex"))
        
        # Stack
        elif opcode == OP_DUP:
            disassembly.append("OP_DUP")

        # Bitwise functions
        elif opcode == OP_EQUALVERIFY:
            disassembly.append("OP_EQUALVERIFY")

        # Crypto
        elif opcode == OP_HASH160:
            disassembly.append("OP_HASH160")
        elif opcode == OP_CHECKSIG:
            disassembly.append("OP_CHECKSIG")

        # Unknown
        else:
            print "Unknown opcode: {0}".format(hex(opcode))
            break

        print " ".join(disassembly)

def main():
    disassemble(example_out_script)
    disassemble(example_in_script)


main() if __name__ == "__main__" else None