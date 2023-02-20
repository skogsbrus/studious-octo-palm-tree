#!/usr/bin/env python3
from transmission_rpc import Client
from os import environ
from pathlib import Path

import argparse
import json


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=True)
    parser.add_argument('--port', type=str, required=True)
    parser.add_argument('--username', type=str)
    parser.add_argument('--password', type=str)
    parser.add_argument('--secrets-file', type=Path)
    return parser.parse_args()


def is_unregistered(torrent):
    return torrent.error != 0 and "unregistered" in torrent.error_string.lower()


def main():
    args = get_args()

    host = args.host
    username = environ.get("TRANSMISSION_RPC_USERNAME")
    password = environ.get("TRANSMISSION_RPC_PASSWORD")

    if args.secrets_file:
        with open(args.secrets_file, "r") as f:
            secrets = json.load(f)
        username = secrets['rpc-username']
        password = secrets['rpc-password']


    cli = Client(host=host, username=username, password=password, port=args.port)

    torrents = cli.get_torrents()
    unregistered = list(filter(is_unregistered, torrents))

    if unregistered:
        cli.remove_torrent([t.id for t in unregistered], delete_data=False)
        print(f"Removed {len(unregistered)} unregistered torrents")
    else:
        print(f"No unregistered torrents found")


if __name__ == "__main__":
    main()
