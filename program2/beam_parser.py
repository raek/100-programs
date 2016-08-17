from collections import OrderedDict
import io
import json
import struct
import sys

def main(file_path):
    result = OrderedDict()
    with open(file_path, "rb") as f:
        b = BeamStream(f)
        file_end = process_header(b)
        while b.current_position() < file_end:
            tag, chunk_result = process_chunk(b, result)
            result[tag] = chunk_result
    json.dump(result, sys.stdout, indent=4)

def process_header(b):
    b.match_tag(b"FOR1")
    file_end = b.read_int() + 8
    b.match_tag(b"BEAM")
    return file_end

def process_chunk(b, result):
    tag = b.read_tag()
    length = b.read_int()
    end = b.current_position() + length
    string_tag = tag.decode("utf-8")
    fn_name = "decode_{}_chunk".format(string_tag.lower())
    if fn_name in globals():
        chunk_result = globals()[fn_name](b, result)
    else:
        chunk_result = None
        b.skip(length)
    assert b.current_position() == end
    b.align()
    return string_tag, chunk_result

def decode_atom_chunk(b, result):
    chunk_result = []
    n = b.read_int()
    for _ in range(n):
        l = b.read_byte()
        atom = b.read_data(l).decode("utf-8")
        chunk_result.append(atom)
    return chunk_result

def decode_expt_chunk(b, result):
    chunk_result = OrderedDict()
    n = b.read_int()
    for _ in range(n):
        fun_idx = b.read_int()
        arity = b.read_int()
        label = b.read_int()
        fun_name = result["Atom"][fun_idx - 1]
        full_name = "{}/{}".format(fun_name, arity)
        chunk_result[full_name] = label
    return chunk_result

def decode_impt_chunk(b, result):
    chunk_result = []
    n = b.read_int()
    for _ in range(n):
        mod_idx = b.read_int()
        fun_idx = b.read_int()
        arity = b.read_int()
        mod_name = result["Atom"][mod_idx - 1]
        fun_name = result["Atom"][fun_idx - 1]
        full_name = "{}:{}/{}".format(mod_name, fun_name, arity)
        chunk_result.append(full_name)
    return chunk_result

class BeamStream:
    def __init__(self, f):
        self.f = f

    def match_tag(self, expected):
        actual = self.read_tag()
        assert actual == expected

    def read_tag(self):
        tag = self.f.read(4)
        assert len(tag) == 4
        return tag

    def read_int(self):
        s = self.f.read(4)
        assert len(s) == 4
        i, = struct.unpack(">i", s)
        return i

    def read_byte(self):
        s = self.f.read(1)
        assert len(s) == 1
        return s[0]

    def read_data(self, n):
        left = n
        data = b""
        while left > 0:
            block = self.f.read(left)
            assert len(block) > 0
            data += block
            left -= len(block)
        return data

    def current_position(self):
        return self.f.tell()

    def skip(self, n):
        self.f.seek(n, io.SEEK_CUR)

    def align(self):
        rem = self.f.tell() % 4
        if rem != 0:
            self.f.seek(4 - rem, io.SEEK_CUR)

if __name__ == "__main__":
    main(*sys.argv[1:])
