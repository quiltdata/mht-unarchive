#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import quopri
import sys
from pathlib import Path

from email import message_from_file

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def log(msg):
    logging.info(msg)

def unquote(quoted):
    decoded = quopri.decodestring(quoted)
    content = decoded.decode('utf-8')
    return content

class Extract():
    def __init__(self, source_file):
        with open(source_file, 'r') as f:
            self.msg = message_from_file(f)

        self.html = None
        self.files = {}
        for part in self.msg.walk():
            if not part.is_multipart():
                self.parse_part(part)

    def parse_part(self, part):
        ctype = part.get('Content-Type')
        quoted = part.get('Content-Type') == 'quoted-printable'
        url = part.get('Content-Location')
        payload = part.get_payload()

        file_path = Path(url)
        file_name = Path(file_path).name  # myfile.png
        file_stem = Path(file_path).stem  # myfile
        if file_stem not in ctype:
            print(f'ctype {ctype}')
            print(f'url {url}')
            print(f'file_name {file_name}')

        if quoted:
            payload = unquote(payload)

        if 'html' in ctype:
            assert None == self.html
            self.html = payload
        else:
            self.files[url] = payload

    def extra_text(self):
        print(self.msg.preamble)
        print(self.msg.epilogue)


def main():
    args = sys.argv
    if len(args) != 2:
        print("Usage: ./extract.py <mht file>")
        return
    mht = sys.argv[1]
    log('Extract multi-part of "%s" ...' % mht)
    parsed = Extract(mht)
    print(parsed.html)

if __name__ == '__main__':
    main()
