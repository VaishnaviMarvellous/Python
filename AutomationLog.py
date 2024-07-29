from urllib.error import URLError
import os
import time
import psutil
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import schedule
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

def Mailsender(filename,time,toaddr):
    fromaddr="kalmasevaishnavi@gmail.com"  
    password="azpb mwnj viwd evtp"

    msg=MIMEMultipart()
    msg["From"]=fromaddr
    msg["To"]=toaddr

    body=f"""
    Hello,

    Welcome to Marvellous Infosystems.
    Please find attached document which contains log of running process.
    Log file is created at:{time}

    This is auto generated mail.

    Thanks&Regards,
    Marvellous Infosystems
    """

    msg.attach(MIMEText(body,'plain'))

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
    
        print("Log file successfully send through mail") 
    except Exception as e:
        print(f"Unable to send mail:{e}")    

def ProcessLog(log_dir):
    listprocess=[]

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    separator="-" *80
    log_path=os.path.join(log_dir,f"MarvellousLog_{time.strftime('%Y%m%d-%H%M%S')}.log")
    with open(log_path,'w') as f:
        f.write(f"Marvellous Infosystem Process Logger:{time.ctime()}\n")  
        f.write(separator +"\n")      

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
    if len(sys.argv)!=3:
        print("Error:Invalid number of arguments")
        print("Usage:Demo.py <Directory> <Email>")  
        exit(1)

    log_dir=sys.argv[1]
    toaddr=sys.argv[2]

    connected=is_connected()
    if connected:
        startTime=time.time()
        log_path=ProcessLog(log_dir)      
        Mailsender(log_path,time.ctime(),toaddr)
        endTime=time.time()
        print(f"Took {endTime - startTime} seconds to send mail")
    else:
        print("There is no internet connection")

if __name__ == "__main__":
    main()            