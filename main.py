#!/usr/bin/env python
""" Run Question rewrite. """
import argparse
from src.server import app

parser = argparse.ArgumentParser(description='Start Question rewrite interface.')
parser.add_argument('--host', default='0.0.0.0', type=str)
parser.add_argument('--port', default=6380, type=int)

args = parser.parse_args()

app.run(host=args.host, port=args.port, debug=False)
