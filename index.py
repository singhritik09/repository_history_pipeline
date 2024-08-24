import requests
import json
import creds
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

username="singhritik09"
token = creds.token

gh_session=requests.Session()
gh_session.auth=(username,token)

URL="https://api.github.com/user/repos"
repos=json.loads(gh_session.get(URL).text)

print(type(repos))
# print(repos)
# print("Repositories:")
# for i, repo in enumerate(repos):
#     print(f"{i + 1}: {repo['name']}")

# repo_index = int(input("Enter the number of the repository you want to get commits for: ")) - 1
repo_index=24
selected_repo = repos[repo_index]

commits_url = f"https://api.github.com/repos/{username}/{selected_repo['name']}/commits"
commits = json.loads(gh_session.get(commits_url).text)
def get_commit_history(ls:list):
    print(f"\nCommit history for repository '{selected_repo['name']}':")
    for commit in commits:
        commit_message = commit['commit']['message']
        commit_author = commit['commit']['author']['name']
        commit_date = commit['commit']['author']['date']
        # print(f"Author: {commit_author}, Date: {commit_date}, Message: {commit_message}")
        ls.append([commit_message,commit_author,commit_date])
        
    print(ls)
def write_to_file(list1):
    with open("report.txt","a") as f:
        for i in list1:
            f.write(f"{i}\n")
        

def send_email(subject, text_file_path):
    sender = "singhritik2711@gmail.com"
    receivers = ["ritiksingh.is20@bmsce.ac.in", "additionalrecipient@example.com"]
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
        
if __name__=='__main__':
    subject="Changes made to repository"
    path_to_file="C:/Users/singh/Github_History_Pipeline/report.txt"
    ls=[]
    get_commit_history(ls)
    write_to_file(ls)
    send_email(subject,path_to_file)
        
        
time.sleep(300)  # 300 seconds = 5 minutes
