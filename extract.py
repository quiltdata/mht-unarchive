#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import quopri
import sys
from pathlib import Path
from urllib.parse import urlparse

from email import message_from_file

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def log(msg):
    logging.info(msg)

def unquote(quoted):
    decoded = quopri.decodestring(quoted)
    content = decoded.decode('utf-8')
    return content

def extract_file_ext(file_name):
    return Path(file_name).suffix.replace('.','')

def extract_filename(file_path, ctype):
    file_name = file_path.name  # myfile.png
    ext = extract_file_ext(file_name)
    if ctype[-1] == 'svg+xml': 
        ctype.append('svg')

    if ext in ctype: 
        return file_name 

    split = file_name.split('@')
    if split[-1] == 'mhtml.blink':
        return f'{split[-0]}.css'

    return f'{file_name}.{ctype[-1]}'

class Extract():
    def __init__(self, source_file):
        with open(source_file, 'r') as f:
            self.msg = message_from_file(f)

        self.html = None
        self.attrs = {}
        self.payloads = {}
        for part in self.msg.walk():
            if not part.is_multipart():
                self.parse_part(part)

    def files(self):
        return list(self.attrs.keys())

    def add_file(self, uri, ctype):
        sections = urlparse(uri)
        file_path = Path(sections.path)
        file_name = extract_filename(file_path, ctype)
        file_ext = extract_file_ext(file_name)

        attrs = {
            "uri": uri,
            "uri.sections": sections,
            "path": file_path,
            "name": file_name,
            "ext": file_ext,
        }
        self.attrs[file_name] = attrs
        return attrs

    def parse_part(self, part):
        ctype = part.get('Content-Type').split('/')
        quoted = part.get('Content-Type') == 'quoted-printable'
        uri = part.get('Content-Location')
        payload = part.get_payload()
        if quoted:
            payload = unquote(payload)

        if 'html' in ctype:
            assert None == self.html
            self.html = payload
        else:
            attrs = self.add_file(uri, ctype)
            self.payloads[attrs["name"]] = payload
            logging.debug(f'file_name {attrs["name"]}')

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
