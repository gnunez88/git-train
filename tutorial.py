#!/usr/bin/env python3

import argparse
import os
import pathlib
import subprocess

class User(object):

    def __init__(self, user=user:str) -> None:
        self.user = user
        self.env = os.environ
        self.env['HOME'] = _gethome()

    def _gethome(self) -> str:
        cwd = pathlib.Path().cwd()
        return f'{cwd}/home/{self.user}'


def main(args):
    pass


# Execution
if __name__ == '__main__':
    parser = argparse.ArgumentParser("tutorial")
    parser.add_argument(
            '-user',
            type=str,
            choices=['captain', 'thor', 'hulk'],
            help="User")
    args = parser.parse_args()
    main(args)
