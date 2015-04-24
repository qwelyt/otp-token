#!/usr/bin/python

import sys
import hmac
import base64
import struct
import hashlib
import time

def main(args):
        if args[1] == "--totp":
                print(get_totp_token(args[2]))
        elif args[1] == "--hotp":
                print(get_hotp_token(args[2], args[3]))
        else:
                print("Invalid key type")
                print("Available flags:")
                print("   --totp        generates token based on time (changed in 30-second intervals)")
                print("   --hotp        generates one-time token (that should validate after single use)")

def get_hotp_token(key, interval):
    realkey = base64.b32decode(key, True)
    msg = struct.pack(">Q", interval)
    h = hmac.new(realkey, msg, hashlib.sha1).digest()
    o = ord(h[19]) & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7ff ff fff) % 100 00 00
    return h

def get_totp_token(key):
    return get_hotp_token(key, interval=int(time.time())//30)

main(sys.argv)
