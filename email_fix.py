#!/usr/bin/env python3
# Fix GitHub User's Email Address leak through commits
# Repo: https://github.com/bearlike/find-fix-git-email-leak
import requests
from os import system, environ, chdir, getcwd
from subprocess import check_output
from colorama import Style, Fore
from shutil import rmtree
from dotenv import load_dotenv

load_dotenv()

# GitHub Secrets
username = environ["GH_USERNAME"]
token = environ["GH_TOKEN"]
orgs = environ["ORGS"].split(",")

# Fixes
old_email = environ["OLD_EMAIL"]
correct_name = environ["CORRECT_NAME"]
correct_email = environ["CORRECT_EMAIL"]

# To supress git fliter warning
environ["FILTER_BRANCH_SQUELCH_WARNING"] = "1"

git_fix = """
git log --pretty=format:"%h %an %ae %s" | grep {leaked_email}
git filter-branch --env-filter '
if [ "$GIT_COMMITTER_EMAIL" = "{old_email}" ]
then
    export GIT_COMMITTER_NAME="{correct_name}"
    export GIT_COMMITTER_EMAIL="{correct_email}"
fi
if [ "$GIT_AUTHOR_EMAIL" = "{old_email}" ]
then
    export GIT_AUTHOR_NAME="{correct_name}"
    export GIT_AUTHOR_EMAIL="{correct_email}"
fi
' --tag-name-filter cat -- --all
git log --pretty=format:"%h %an %ae %s" | grep {leaked_email}"""

def main():
    repos = []
    print(Fore.YELLOW,
        "!! User must have write permissions for the repositories !!",
        Style.RESET_ALL)
    print(Fore.YELLOW, "!! Works only on parent branch !!", Style.RESET_ALL)
    print(Fore.YELLOW, "!! Commit hashes can be changed !!", Style.RESET_ALL)
    system("git config --local --bool core.bare false")
    for org in orgs:
        org = org.strip()
        query_url = f"https://api.github.com/users/{org}/repos".format(org)
        headers = {'Authorization': f'token {token}'}
        r = requests.get(query_url, headers=headers)
        objects = r.json()
        for obj in objects:
            repos.append(obj["html_url"].replace("https://github.com/", ""))
    count = 1
    tot = len(repos)
    for repo in repos:
        progress_str = f"{count} out of {tot} ({repo})..."
        print(Fore.BLUE, progress_str, Style.RESET_ALL)
        repo_name = repo.split("/")[1]
        system(f"git clone --bare https://{username}:{token}@github.com/{repo}")
        chdir(repo_name + ".git")
        system("git config --local remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'")
        system("git fetch origin")
        branches_output = check_output(["git", "branch", "-a"]).decode("utf-8")
        branches = [
            branch.strip().replace("* ", "")
            for branch in branches_output.split('\n')
            if len(branch) > 0
            and '->' not in branch
            and 'remotes/' not in branch
        ]
        repo_path = getcwd()
        for branch in branches:
            branch_name = branch.split('/')[-1]
            print(Fore.CYAN ,f"Working on branch {branch}", Style.RESET_ALL)
            email_fix = git_fix.format(
                old_email=old_email,
                correct_name=correct_name,
                correct_email=correct_email
            )
            branch_checkout = f"git --work-tree={repo_path} checkout {branch}"
            system(branch_checkout)
            system(email_fix)
            system(f"git --work-tree={repo_path} push --force origin {branch_name}")
        count += 1
        chdir("../")
        rmtree(repo_name + ".git")
        print(Style.RESET_ALL)

if __name__ == '__main__':
    main()
