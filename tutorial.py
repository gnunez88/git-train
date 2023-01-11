#!/usr/bin/env python3

import argparse
import os
import pathlib
import random
import re
import shutil
import subprocess
from git import Repo  # gitpython

class User(object):

    def __init__(self, user:str) -> None:
        self.user = user
        self.env = os.environ.copy()
        self.env['HOME'] = self._gethome()
        self.repos = dict()

    def _get_env(self, text) -> None:
        print(f"In: {text}")
        print(f"self.user: {self.user}")
        print(f"self.env['HOME']: {self.env['HOME']}")

    def _set_env(self) -> None:
        """
        You cannot make: os.environ = self.env because
        type(os.environ) is os._Environ and 
        type(self.env) is dict
        """
        os.environ['HOME'] = self.env['HOME']

    def _gethome(self) -> str:
        cwd = pathlib.Path().cwd()
        return f'{cwd}/home/{self.user}'

    def clone(self, url:str, project_name:str):
        self._set_env()  # Setting the environment
        self.repos[project_name] = dict()
        self.repos[project_name]["url"] = url
        path = f'{self.env["HOME"]}/{project_name}'
        self.repos[project_name]["path"] = path
        object_path = pathlib.Path(path)
        if object_path.exists():
            shutil.rmtree(object_path)
        self.repos[project_name]["repo"] = Repo.clone_from(url, path)

    def mkchanges(self, level:int, project_name:str):
        pass

    def pull(self, url:str):
        pass

    def push(self, url:str):
        pass

    def commit(self, project_name:str):
        pass

    def branch(self, project_name:str, branch_name:str):
        pass

    def merge(self, project_name:str, branch_name:str):
        pass


def parse_url(raw_url:str) -> dict:
    pattern  = r'((?P<scheme>https?)://)?'
    pattern += r'((?P<domain>github\.com)/)?'
    pattern += r'(?P<username>.*?)/'
    pattern += r'(?P<project>.*?)(\.git)?$'
    extracted = re.search(pattern, raw_url)
    if extracted:
        parts = extracted.groupdict()
        scheme = parts['scheme'] if parts['scheme'] else 'https'
        domain = parts['domain'] if parts['domain'] else 'github.com'
        username = parts['username']
        project = parts['project']
        if not (username and project):
            message = "Either the username or project name is missing"
            raise Exception(message)
        url = f'{scheme}://{domain}/{username}/{project}.git'
    return {"url": url, "name": project}


def main(args):
    # Instantiating user objects
    users = dict()
    users['captain'] = User("captain")
    users['thor'] = User("thor")
    users['hulk'] = User("hulk")
    # Cloning the project
    project = parse_url(args.project)
    for user in users:
        users[user].clone(project["url"], project["name"])
    # Level 1: A user makes a modification and pushes it to the repository
    user = random.choice(users)


# Execution
if __name__ == '__main__':
    parser = argparse.ArgumentParser("tutorial")
    parser.add_argument(
            '-project',
            type=str,
            required=True,
            help="GitHub Project URL")
    parser.add_argument(
            '-user',
            type=str,
            choices=['captain', 'thor', 'hulk'],
            help="User")
    args = parser.parse_args()
    main(args)
