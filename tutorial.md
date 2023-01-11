# Tutorial

To parse this Markdown file:
- `pandoc -t <plain|html> <file>.md`
Better alternatives:
- You can also use `grip` (`pip3 install grip`) to parse it with the GitHub API.
- Cloning and compiling a Go project ([`glow`](https://github.com/charmbracelet/glow.git)).
    - Usage: `glow [-p] [-w80] <file>.md`

## 01 - Basic Level

### Steps to Follow

00. Configure your information:
    - The next commands will create a `.gitconfig` file within your `HOME` directory.
```bash
git config --global user.name "Your Name"
git config --global user.email "your@e.mail"
```
01. Make a directory "project01" and go into it:
    - `mkdir project01`
    - `cd project01`
02. Initiate a `git` repository:
    - `git init`
03. Create simple Python3 script called `hello.py`:
```py
#!/usr/bin/env python3
print("Hello world")
```
04. Check the status of the repository:
    - `git status`
    - There should be an untracked file (`hello.py`).
05. Stage the changes (add the changes to the index to commit):
    - `git add -A`
06. Check the status of the repository:
    - `git status`
    - The untracked file is now on the index (staging area).
07. Commit the changes with a simple message:
    - `git commit -m "Simple hello world script"`
08. Check the logs:
    - `git log`
09. Make some complicated changes to the script:
    - `sed -i 's/Hello/Goodbye/' hello.py`
10. Check the status of the repository:
    - `git status`
11. Check all the differences between the unstaged changes and the last commit:
    - `git diff`
12. Stage the changes and commit them again:
    - `git add -A`
    - `git commit -m "Changing Hello for Goodby on hello.py"`
13. See the logs in one line:
    - `git log --oneline`
14. Change the script so it can read the information from a file:
```py
#!/usr/bin/env python3
with open("name.txt", "r") as f:
    name = f.read()
    print(f"Hello {name}")
```
15. Create a file `name.txt` with your name
16. Check the status of the repository:
    - `git status`
17. You may not want to save `name.txt` or any `.txt` files, then you should create a `.gitignore` file:
    - `echo '*.txt' > .gitignore`
18. Check the status of the repository:
    - `git status`
    - The `name.txt` file does not show up any longer.
19. Add the `.gitignore` file to the staging area and commit it:
    - `git add .gitignore`
    - `git commit -m ".gitignore added"`
20. Check the status of the repository:
    - `git status`
    - There are still changes to commit. We only have commited the `.gitignore` file.
21. Add the new changes to index and commit.
    - `git add -A`
    - `git commit -m "hello.py reads name from file"`



