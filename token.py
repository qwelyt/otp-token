#!/usr/bin/python

import sys
import hmac, base64, struct, hashlib, time

def main(args):
        if args[1] == "--totp":
                print(get_totp_token(args[2]))
        elif args[1] == "--hotp":
                print(get_hotp_token(args[2], args[3]))
        else:
                print("Invalid key type")
                print("Available flags:")
                print("   --totp        generates token based on time (changed i                                                  n 30-second intervals)")
                print("   --hotp        generates one-time token (that should in                                                  validate after single use)")

def get_hotp_token(secret, intervals_no):
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = ord(h[19]) & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h

def get_totp_token(secret):
    return get_hotp_token(secret, intervals_no=int(time.time())//30)

main(sys.argv)
