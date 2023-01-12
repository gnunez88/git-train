# Tutorial

To parse this Markdown file:
- `pandoc -t <plain|html> <file>.md`
Better alternatives:
- You can also use `grip` (`pip3 install grip`) to parse it with the GitHub API.
- Cloning and compiling a Go project ([`glow`](https://github.com/charmbracelet/glow.git)).
    - Usage: `glow [-p] [-w80] <file>.md`

## 01 - Basic Level

- `config`, `init`, `status`, `add`, `commit`, `diff`, `.gitignore`

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
    - `git commit -m "hello.py reads name from a fly"`
22. Check the logs:
    - `git log`
    - You might notice you did not want to write `a fly`, but `a file`.
23. Ammend your commit message:
    - `git commit --amend -m "hello.py reads name from a file"`
    - Note: you can do this only with the last commit.
24. Check the logs to see if the message was changed:
    - `git log`

## 02 - Still Basic Level

- `clone`, `pull`, `branch`, `switch`, `merge`, `remote`, `push`

### Steps to Follow

00. Create a SSH-key pair:
```bash
ssh-keygen -t rsa -b 2048 -N '' -f ~/.ssh/github -q
```
01. Create the proper settings to access GitHub with this key:
```bash
cat > ~/.ssh/config << EOF
Host github
    Hostname github.com
    User git
    Port 22
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/github
```
02. Upload your **public** key to your GitHub account:
    01. Click on your user's profile image.
    02. Click on `Settings` 
    03. Click on `SSH and GPG keys` within the `Access` section
    04. Click on the `New SSH key` button
    05. Choose a title
    06. Select the `Authentication type` on `Key type`.
    07. Paste the PUBLIC (`.pub`) key on the `Key` text area.
    08. Click on `Add SSH key` button.
03. Test the connection:
```bash
ssh -vT github
```
    - Notes: 
        01. The `ssh` client will get the information from the `~/.ssh/config` file.
        02. It knows what information to choose because it is specified with the `github` word.
        03. We can have more than one section for other repositories.
04. Create a new repository on GitHub:
    01. Go to your profile (`https://github.com/<username>`)
    02. Select the `Repositories` tab.
    03. Click on the `New` button.
    04. On repository name choose the project name, e.g.: `git-test`.
    05. If you are going to push (upload) an existing repository, do not add anything (license, README.txt, gitignore)
    06. Click on the `Create repostory` button.
05. Since, by default, `git` creates the `master` branch and GitHub/GitLab use the `main` branch, you should
    rename your branch:
    - `git branch -m master main`
06. Push (upload) your existing repository.
```bash
git remote add github-ssh git@github:<username>/git-test.git
git push -u github-ssh main
```
    - Notes:
        01. Most people use `origin`, however you can put whatever you want.
        02. I have use `github` as a hostname, instead of `github.com` because the information is going
            to be taken from `~/.ssh/config`, where `github` is the key to the information.
        03. With the `push` command we choose the *remote* key to use (`github-ssh`) and the branch
            to push (`main`).

# More commands and concepts

## revert vs reset

- `git revert` makes a new commit with the changes undone.
- `git reset` sets back the HEAD and TREE.
    - `--soft`: this option allows us to go back to the future (changes).
    - `--hard`: this removes forever the changes.

## merge vs rebase vs fast-forward vs squash

- `git merge <feature-branch>`: merges two branches in a new commit without merging their history.
    - `--ff`: (fast-forward)
    - `--squash`: combine multiple commits into one.
- `git rebase`: merges two branches merging their history.

```bash
git log --oneline --graph --all
```

```bash
git show-branch -a
```

# Recommendations

What to commit?
- source code
- non-sensitive settings
What not to commit?
- credentials
- API keys
- usernames
- emails
- binaries

# Workflow

01. Main branch with consistent code.
02. Feature branches where to work in.
03. Several and consistent commits.
    - Descriptive commit messages.
    - Make commits about one whole thing is easier to maintain when reading the history.
04. Squash the commits on merging to the main branch.
    - You should squash your local commits.
05. Before pushing a commit, you should fetch the remote repository to synchronise.
06. Use tags for the most important commits.
    - Follow to [semantic versioning](https://semver.org/)
07. Whenever there is an important and functional commit, make a release.
    - Within a release we can upload binaries if necessary (max.: 100MB).
08. Use of CI/CD: GitHub Actions to test the code automatically before merging.


