#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import sys
import re
import quopri
import base64
import os

from email import message_from_file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log(msg):
    logging.info(msg)

def main():
    args = sys.argv
    if len(args) != 2:
        print("Usage: extract.py <mht file>")
        return
    mht = sys.argv[1]
    log('Extract multi-part of "%s" ...' % mht)
    # open file
    with open(mht, 'r') as f:
        msg =  message_from_file(f)
        for part in msg.walk():

        print(f'is_multipart={msg.is_multipart()}')
        parts = msg.get_payload()
        for part in parts:
            print(f'part.is_multipart={part.is_multipart()}')
            print(f'part.items={part.items()}')
            payload = part.get_payload()
            decoded = quopri.decodestring(payload)
            content = decoded.decode('utf-8')
            print(len(content))



if __name__ == '__main__':
    main()
