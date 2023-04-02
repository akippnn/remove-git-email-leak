<h1 align="center">
  Remove Leaked Git Emails
</h1>

<h4 align="center">Find and remove publicly accessible git commit email addresses.</h4>

<p align="center">
  <a href="https://www.python.org"><img src="https://img.shields.io/badge/language-python-blue.svg?style=flat"></a>
  <a href="/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=flat"></a>

GitHub uses your commit email address to associate commits with your GitHub account. When a user makes commits to a public repository, their email address is pushed with the commit. 

If you'd like to keep your personal email address private, you can use a GitHub-provided `no-reply` email address as your commit email address. GitHub provides some [instructions](https://help.github.com/articles/setting-your-email-in-git/) on keeping your personal email address private, but it seems that GitHub users either don't know or don't care that their email address may be exposed.

However, any commits you made before changing your commit email address are still associated with your previous email address. This is why this repository exists.  The script will clone all accessible repositories, change the committer email from all commits and push it back to GitHub. 

## Getting Started

### Prerequisites
- The `email_fix.py` script is meant to run on Linux.  
  If you are not using Linux, a `Dockerfile` is included for you but you will need `Docker` to use it. Inside the repository, please run the following command:
  ```pwsh
  docker build -t remove-git-email-leak . && docker run -it remove-git-email-leak
  ```
  Then please skip ahead to (usage)[#usage].
- What things you need to run the program:
- [Python3](https://www.python.org/) and PIP can be installed using `APT package manager` by running: 
  ```bash
  sudo apt install python3 python3-pip
  ```
- Install the following Packages from PyPi by using the following commands:
  ```bash
  pip3 install -r requirements.txt
  ```

### Usage
- First, we need to generate a personal access token that will allow us to authenticate against the API. We can get one at https://github.com/settings/tokens and by clicking on *Generate new token*. Select `Repo` and `User` scopes for the token.
- Rename `.env.sample` to `.env` and populate the appropriate values. 
- Run `retrieve_email.py` to check for all leaked email addresses. This script uses [recent events](https://developer.github.com/v3/activity/events/) via the GitHub API to find the leaked email addresses. An example screenshot is attached:
  - ```bash
    python3 retrieve_email.py
    ```
  -  ![Sample Run for retrieve_email.py](docs/retrieval_example.png)
- Once you identified the leaked email addresses, populate them back to the `.env` file.
- Now, run `email_fix.py` to replace the committer email addresses with the `CORRECT_EMAIL` from `.env` (preferably the GitHub-provided `no-reply` email address). Changes might take up to 90 days to reflect in the GitHub Events API.
- Repeat the process if you have multiple leaked email addresses.
- [GitHub Docs: Block commits you push from the command line that expose your personal email address](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-user-account/managing-email-preferences/blocking-command-line-pushes-that-expose-your-personal-email-address)

### Notes
- The script does not preserve the `SHA1`s for previous tags, versions and objects. 
- The `retrieve_email.py` uses GitHub Events API to scan for leaked email(s) which limits scanning upto 100 recent results per page
- `TODO` Each Git commits needs to be scanned for email(s). This will also increase coverage for git repositories outside GitHub.
- `TODO` Currently, works only on the `HEAD` or parent branch (`master`, `main`, etc). Will increase the scope to other branches if I have the time.

### Acknowledgments
- Hat tip to anyone whose code was used.

## Disclaimer
```
I shall not be liable for any consequential, incidental, direct, indirect, special, or other damages whatsoever (including, without limitation, damages for loss of business profits, business interruption, loss of business information, or other pecuniary loss). Run this at your own risk.  
```

<p align="center">
  Made with ❤️ by <a href="https://kanth.tech/github">Krishnakanth Alagiri</a>
</p>
