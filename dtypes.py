import struct

"""
typeNames = {
    'int8'   :'b',
    'uint8'  :'B',
    'int16'  :'h',
    'uint16' :'H',
    'int32'  :'i',
    'uint32' :'I',
    'int64'  :'q',
    'uint64' :'Q',
    'float'  :'f',
    'double' :'d',
    'char'   :'s'
}
"""

class dtype(object):
	struct_fmt = ""
	read_len = 1

	@classmethod
	def unpack(class_obj, stream):
		read_len = struct.calcsize(class_obj.struct_fmt)
		read_data = stream.read(read_len)
		return struct.unpack(class_obj.struct_fmt, read_data)[0]

	@classmethod
	def pack(class_obj, value):
		try:
			iter(value)
		except:
			value = [value]
		return struct.pack(class_obj.struct_fmt, *value)

class uint8(dtype):
	struct_fmt = "B"

class uint16(dtype):
	struct_fmt = "H"

class uint32(dtype):
	struct_fmt = "I"

class uint64(dtype):
	struct_fmt = "Q"

class int32(dtype):
	struct_fmt = "i"

class varint(dtype):
	@classmethod
	def unpack(class_obj, stream):
		read_data = uint8.unpack(stream)
		if read_data < 0xfd:
			return read_data
		elif read_data == 0xfd:
			return uint16.unpack(stream)
		elif read_data == 0xfe:
			return uint32.unpack(stream)
		elif read_data == 0xff:
			return uint64.unpack(stream)
		else:
			return -1
