from urllib.error import URLError
import os
import time
import psutil
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from urllib.request import urlopen
import sys

def is_connected():
    test_urls=["http://www.google.com","http://www.amazon.com","http://www.microsoft.com"]
    for url in test_urls:
        try:
            urlopen(url,timeout=5)
            return True
        except URLError as e:
            print(f"Connection check failed for {url}:{e}")
    return False    

def Mailsender(filename, time, toaddr, subject, body):
    fromaddr="kalmasevaishnavi@gmail.com"  
    password="azpb mwnj viwd evtp"

    msg=MIMEMultipart()
    msg["From"]=fromaddr
    msg["To"]=toaddr
    msg["Subject"]=subject

    msg.attach(MIMEText(body,'plain'))

    if filename:
        with open(filename,"rb") as attachment:
            p=MIMEBase('application','octet-stream')
            p.set_payload(attachment.read()) 
            encoders.encode_base64(p)
            p.add_header('Content-Disposition',f"attachment; filename={filename}")
            msg.attach(p)

    try:
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(fromaddr,password)     
        text=msg.as_string()
        server.sendmail(fromaddr,toaddr,text)
        server.quit()
    
        print("Email successfully sent") 
    except Exception as e:
        print(f"Unable to send email: {e}")    

def ProcessLog(log_dir):
    listprocess=[]

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    separator="-" *80
    log_path=os.path.join(log_dir,f"VaishnaviLog_{time.strftime('%Y%m%d-%H%M%S')}.log")
    with open(log_path,'w') as f:
        f.write(f"Vaishnavi kalmase Process Logger: {time.ctime()}\n")  
        f.write(separator + "\n")      

        for proc in psutil.process_iter(attrs=['pid','name','username']):
            try:
                pinfo=proc.info
                listprocess.append(pinfo)
            except (psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
                pass

        for element in listprocess:
            f.write(f"{element}\n")            

    print(f"Log file is successfully generated at location {log_path}")
    return log_path

def main():
    if len(sys.argv) != 3:
        print("Error: Invalid number of arguments")
        print("Usage: Demo.py <Directory> <Email>")  
        exit(1)

    log_dir=sys.argv[1]
    toaddr=sys.argv[2]

    connected=is_connected()
    if connected:
        startTime = time.time()
        log_path = ProcessLog(log_dir) 

        subject = "Happy Birthday!"
        body = """
        Hello,

        Wishing you a very Happy Birthday!
        May your day be filled with joy, love, and laughter.

        Best wishes,
        Vaishnavi kalmase
        """

        Mailsender(log_path, time.ctime(), toaddr, subject, body)
        endTime = time.time()
        print(f"Took {endTime - startTime} seconds to send the email")
    else:
        print("There is no internet connection")

if __name__ == "__main__":
    main()