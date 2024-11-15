import requests
import json
import creds
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
username="singhritik09"
token = creds.NEWTOKEN

gh_session=requests.Session()
gh_session.auth=(username,token)

URL = "https://api.github.com/user/repos"
params = {'per_page': 100, 'page': 1}
repos = []

def get_commit_history(commits_list: list):
    selected_repo = 'sky-vault'
    commits_url = f"https://api.github.com/repos/{username}/{selected_repo}/commits"
    params = {'per_page': 100, 'page': 1}
    
    while True:
        response = gh_session.get(commits_url, params=params)
        response.raise_for_status()  # Ensure the request was successful
        batch = response.json()
        
        for commit in batch:
            commit_message = commit['commit']['message']
            commit_author = commit['commit']['author']['name']
            commit_date = commit['commit']['author']['date']
            commits_list.append([commit_message, commit_author, commit_date])
        
        # Check if there's another page of results
        if 'next' not in response.links:
            break
        params['page'] += 1
    
    return commits_list
    
if __name__=='__main__':
    subject="Changes made to repository"
    path_to_file="C:/Users/singh/Github_History_Pipeline/report.txt"
    ls=[]

    l1=get_commit_history(ls)
    print(l1)        
