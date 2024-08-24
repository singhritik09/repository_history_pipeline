import requests
import json

username="singhritik09"
token = ""

gh_session=requests.Session()
gh_session.auth=(username,token)

URL="https://api.github.com/user/repos"
repos=json.loads(gh_session.get(URL).text)

print(type(repos))

print("Repositories:")
for i, repo in enumerate(repos):
    print(f"{i + 1}: {repo['name']}")

# repo_index = int(input("Enter the number of the repository you want to get commits for: ")) - 1
# selected_repo = repos[repo_index]

commits_url = f"https://api.github.com/repos/{username}/mail-AI/commits"
commits = json.loads(gh_session.get(commits_url).text)

print(f"\nCommit history for repository mail-AI: ")
ls=[]
for commit in commits:
    commit_message = commit['commit']['message']
    commit_author = commit['commit']['author']['name']
    commit_date = commit['commit']['author']['date']
    print(f"Author: {commit_author}, Date: {commit_date}, Message: {commit_message}")
    ls.append([commit_message,commit_author,commit_date])
    
print(ls)

with open("report.txt","a") as f:
    for i in ls:
        f.write(f"{i}\n")