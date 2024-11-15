import requests
import creds
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

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
        batch = response.json() # list of commits returned by a single API request
        
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
def send_email(subject, text_file_path):
    sender = "singhritik2711@gmail.com"
    receivers = ["ritiksingh.is20@bmsce.ac.in", "divyamishra216june@gmail.com"]
    password = "yebmvzgchqqaeupe"  
    
    BODY_HTML = f"""
    <html> 
    <head></head> 
    <body style="font-family: 'Arial', sans-serif; color: #333333; line-height:1.6;"> 
        <h1 style="color: #333333; font-weight: bold; text-align: center">{subject}</h1> 
        
        <p>New commit made to repository</p>
        <p>Here is the log</p>
    </body> 
    </html>
    """
    
    msg = MIMEMultipart("alternative")
    msg['From'] = sender
    msg['To'] = ", ".join(receivers)  # Join the list of recipients into a single string separated by commas
    msg['Subject'] = subject
    msg.attach(MIMEText(BODY_HTML, "html"))
    
    # Attach the text file
    try:
        with open(text_file_path, "r") as f:
            file_content = f.read()
            attachment = MIMEText(file_content, "plain")
            attachment.add_header("Content-Disposition", "attachment", filename=text_file_path)
            msg.attach(attachment)
    except FileNotFoundError:
        print("Error: File path not found.")
        return

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receivers, msg.as_string())  # Send to multiple recipients
        print("Email sent successfully")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:

        server.quit()
def write_to_file(list1: list, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, "w") as f:
        for item in list1:
            f.write(f"{item}\n")
            
if __name__=='__main__':
    subject="Changes made to repository"
    path_to_file = "./report.txt"
    ls=[]
    l1=get_commit_history(ls)
    write_to_file(l1,path_to_file)
    send_email(subject,path_to_file)
    print(l1)        
