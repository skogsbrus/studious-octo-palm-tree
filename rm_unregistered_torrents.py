from transmission_rpc import Client
from os import environ

import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=True)
    parser.add_argument('--port', type=str, required=True)
    parser.add_argument('--username', type=str)
    parser.add_argument('--password', type=str)
    return parser.parse_args()


def is_unregistered(torrent):
    return torrent.error != 0 and "unregistered" in torrent.error_string.lower()


def main():
    args = get_args()

    host = args.host
    username = environ.get("TRANSMISSION_RPC_USERNAME")
    password = environ.get("TRANSMISSION_RPC_PASSWORD")

    cli = Client(host=host, username=username, password=password, port=args.port)

    torrents = cli.get_torrents()
    unregistered = list(filter(is_unregistered, torrents))

    cli.remove_torrent([t.id for t in unregistered], delete_data=False)

    print(f"Removed {len(unregistered)} unregistered torrents")


if __name__ == "__main__":
    main()
