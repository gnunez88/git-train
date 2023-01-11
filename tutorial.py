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

    def _set_env(self, pwd:str="") -> None:
        """
        You cannot make: os.environ = self.env because
        type(os.environ) is os._Environ and 
        type(self.env) is dict
        """
        os.environ['HOME'] = self.env['HOME']
        os.chdir(pwd if pwd else self.env['HOME'])

    def _gethome(self) -> str:
        cwd = pathlib.Path().cwd()
        return f'{cwd}/home/{self.user}'

    def testssh(self) -> bool:
        self._set_env(self.env['HOME'])  # Setting the environment
        cmd = ["ssh", "github.com", "-vT"]
        ssh = subprocess.run(cmd, capture_output=True)
        print(ssh.stdout.decode('utf-8').strip())
        print("Error")
        print(ssh.stderr.decode('utf-8').strip())

    def config(self, project:dict, private_key_path:str) -> None:
        # Creating the directory structure if not exists
        path = f'{self.env["HOME"]}/.ssh'
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        # Configuring the key
        with open(f'{path}/config', 'w+') as f:
            content  = f"Host {project['domain']}\n"
            content += f"\tHostname {project['domain']}\n"
            content += f"\tUser git\n"
            content += f"\tPreferredAuthentications publickey\n"
            content += f"\tIdentityFile ~/.ssh/origin\n"
            f.write(content)
        # Copying the private key
        with open(private_key_path, 'r') as f:
            private_key = f.read()
        with open(f'{path}/origin', 'w') as f:
            f.write(private_key)
        # Changing the permissions to the private key
        os.chmod(f'{path}/origin', 0o600)

    def clone(self, url:str, ssh:str, project_name:str) -> None:
        self._set_env(self.env['HOME'])  # Setting the environment
        self.repos[project_name] = dict()
        self.repos[project_name]["url"] = url
        self.repos[project_name]["ssh"] = ssh
        path = f'{self.env["HOME"]}/{project_name}'
        self.repos[project_name]["path"] = path
        object_path = pathlib.Path(path)
        if object_path.exists():
            shutil.rmtree(object_path)
        cmd = subprocess.run(['git', 'clone', url, path], capture_output=True)

    def mkchanges(self, level:int, project_name:str) -> None:
        self._set_env(self.env['HOME'])
        if level == 1:
            file = "easy.txt"
            with open(f"{self.repos[project_name]['path']}/{file}", "a+") as f:
                content  = "#!/usr/bin/env python3\n"
                content += "print('level 1')\n"
                f.write(content)
        if level == 2:
            with open(f"{self.repos[project_name]['path']}/{file}", "a+") as f:
                content = "print('level 2')\n"
                f.write(content)
        if level == 3:
            with open(f"{self.repos[project_name]['path']}/{file}", "a+") as f:
                content  = f.read()
                content  = content.replace("level", "Level")
                content += "print('Level 3')\n"
                f.write(content)

    def pull(self, url:str) -> None:
        pass

    def push(self, project_name:str, origin:str, branch:str="main") -> None:
        self._set_env(self.repos[project_name]['path'])
        cmd_rm_origin = ['git', 'remote', 'rm', 'origin']
        subprocess.run(cmd_rm_origin, capture_output=True)
        cmd_add_origin = ['git', 'remote', 'add', 'origin', origin]
        subprocess.run(cmd_add_origin, capture_output=True)
        cmd_push = ['git', 'push', '-u', 'origin', branch, '-v']
        push = subprocess.run(cmd_push, capture_output=True)
        #print("push")
        #print(push.stdout.decode('utf-8').strip())
        #print(push.stderr.decode('utf-8').strip())

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
        ssh = f'git@{domain}:{username}/{project}.git'
        project = {"name": project, 
                   "username": username, 
                   "ssh": ssh, 
                   "url": url, 
                   "domain": domain}
    else:
        message = "Either the username or project name is missing"
        raise Exception(message)
    return project


def main(args):
    # Checking the private key path
    if pathlib.Path(args.key).exists():
        private_key = args.key
    else:
        message = "The path to the private key does not exist"
        raise Exception(message)
    # User names
    names = ['captain', 'thor', 'hulk', 'black_widow', 'iron_man']
    # Instantiating user objects
    users = dict()
    for name in names:
        users[name] = User(name)
    # Setting the project info
    project = parse_url(args.project)

    # Level 1: A user adds a new file
    # Cloning the project
    level = 1
    user = random.choice(names)
    users[user].clone(project["url"], project["ssh"], project["name"])
    users[user].mkchanges(level, project["name"])
    users[user].stage(project["name"])
    users[user].commit(project["name"], "L1: file added")
    #users[user].config(project, private_key)
    #users[user].testssh()
    users[user].push(project["name"], project["ssh"])
    input(f"L{level}: Make a pull...[Enter]")

    # Level 2: A user adds a new line on an existing file
    level = 2
    user = random.choice(names)
    users[user].mkchanges(level, project["name"])
    users[user].stage(project["name"])
    users[user].commit(project["name"], "L2: line added")
    users[user].push(project["name"], project["ssh"])
    input(f"L{level}: Make a pull...[Enter]")

    # Level 3: A user makes a small modification on an existing file
    level = 3
    user = random.choice(names)
    users[user].mkchanges(level, project["name"])
    users[user].stage(project["name"])
    users[user].commit(project["name"], "L3: file modified")
    users[user].push(project["name"], project["ssh"])
    input(f"L{level}: Make a pull...[Enter]")

    # Level 4: A user adds a file when you have a commit to push
    level = 4
    user = random.choice(names)
    users[user].mkchanges(level, project["name"])
    users[user].stage(project["name"])
    users[user].commit(project["name"], "L4: save your pulls")
    users[user].push(project["name"], project["ssh"])
    input(f"L{level}: Make a pull...[Enter]")

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
    parser.add_argument(
            '-key',
            type=str,
            required=True,
            help="Path to private key")
    args = parser.parse_args()
    main(args)
