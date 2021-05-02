import argparse
import json
from socket import *
import sys
from os.path import exists


def _argparse():
    parser = argparse.ArgumentParser(description='input current node')
    parser.add_argument('--node', action='store', required=True, dest='node', help='this node')
    return parser.parse_args().node


def vector_sender(socket, my_node, addresses, vector):
    pass


def main():
    my_node = _argparse()
    print(my_node)


if __name__ == '__main__':
    main()