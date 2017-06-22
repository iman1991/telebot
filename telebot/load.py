import sys
import os
import argparse

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', nargs='*')
    parser.add_argument('--server', nargs='?')
    parser.add_argument('--login', nargs='?')
    parser.add_argument('--password', nargs='?')
    parser.add_argument('--dir', nargs='?')
    return parser

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    os.system(r"ssh -p 22 -r /Users/frontjss/desktop/bot frontjss@194.124.180.25:/home/frontjss/srv")