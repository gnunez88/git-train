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

    def _set_env(self, pwd:str) -> None:
        """
        You cannot make: os.environ = self.env because
        type(os.environ) is os._Environ and 
        type(self.env) is dict
        """
        os.environ['HOME'] = self.env['HOME']
        os.environ['PWD'] = pwd

    def _gethome(self) -> str:
        cwd = pathlib.Path().cwd()
        return f'{cwd}/home/{self.user}'

    def clone(self, url:str, project_name:str) -> None:
        self._set_env(self.env['HOME'])  # Setting the environment
        self.repos[project_name] = dict()
        self.repos[project_name]["url"] = url
        path = f'{self.env["HOME"]}/{project_name}'
        self.repos[project_name]["path"] = path
        object_path = pathlib.Path(path)
        if object_path.exists():
            shutil.rmtree(object_path)
        cmd = subprocess.run(['git', 'clone', url, path], capture_output=True)

    def mkchanges(self, level:int, project_name:str) -> None:
        self._set_env(self.env['HOME'])
        if level == 1:
            with open(f"{self.repos[project_name]['path']}/l1.info", "a+") as f:
                content  = "#!/usr/bin/env python3\n"
                content += "print('Level 1')\n"
                f.write(content)

    def pull(self, url:str) -> None:
        pass

    def push(self, project_name:str) -> None:
        self._set_env(self.repos[project_name]['path'])
        subprocess.run(['git', 'push'], capture_output=True)

    def stage(self, project_name:str, files:dict=['-A']) -> None:
        self._set_env(self.repos[project_name]['path'])
        subprocess.run(['git', 'add'] + files, capture_output=True)

    def commit(self, project_name:str, message:str) -> None:
        self._set_env(self.repos[project_name]['path'])
        subprocess.run(['git', 'commit', '-m', message], capture_output=True)

    def branch(self, project_name:str, branch_name:str) -> None:
        pass

    def merge(self, project_name:str, branch_name:str) -> None:
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
    # User names
    names = ['captain', 'thor', 'hulk']
    # Instantiating user objects
    users = dict()
    for name in names:
        users[name] = User(name)
    # Cloning the project
    project = parse_url(args.project)
    for user in users:
        users[user].clone(project["url"], project["name"])
    # Level 1: A user makes a modification and pushes it to the repository
    level = 1
    l1_user = random.choice(names)
    users[l1_user].mkchanges(level, project["name"])
    users[l1_user].stage(project["name"])
    users[l1_user].commit(project["name"], "L1 message added")
    users[l1_user].push(project["name"])


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
