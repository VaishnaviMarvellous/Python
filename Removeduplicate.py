import os
import sys
import time
import hashlib
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from urllib.request import urlopen
from urllib.error import URLError
from pathlib import Path
from datetime import datetime

def hashfile(path, blocksize=1024):
    try:
        with open(path, 'rb') as afile:
            hasher = hashlib.md5()
            buf = afile.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(blocksize)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error hashing file {path}: {e}")
        return None

def display_checksum(path):
    if not os.path.isabs(path):
        path = os.path.abspath(path)

    if os.path.isdir(path):
        for dirName, subdirs, fileList in os.walk(path):
            print("Current folder is: " + dirName)
            for fileName in fileList:
                file_path = os.path.join(dirName, fileName)
                file_hash = hashfile(file_path)
                if file_hash:
                    print(file_path)
                    print(file_hash)
                    print(' ')
    else:
        print("Invalid path")

def removedup(path):
    try:
        if not os.path.isabs(path):
            path = os.path.abspath(path)

        if not os.path.isdir(path):
            print("Invalid path")
            return None, None, None

        files = {}
        dups = []
        total_files = 0
        total_duplicates = 0

        for dirName, subdirs, fileList in os.walk(path):
            for fileName in fileList:
                total_files += 1
                file_path = os.path.join(dirName, fileName)
                file_checksum = hashfile(file_path)
                if file_checksum:
                    if file_checksum in files:
                        dups.append(file_path)
                        os.remove(file_path)
                        total_duplicates += 1
                    else:
                        files[file_checksum] = file_path

        marvellous_dir = Path(path) / 'Marvellous'
        marvellous_dir.mkdir(exist_ok=True)
        log_filename = marvellous_dir / f'removeduplog_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        with open(log_filename, 'w') as logfile:
            logfile.write(f"Deletion run at: {datetime.now()}\n")
            logfile.write(f"Total files scanned: {total_files}\n")
            logfile.write(f"Total duplicates found: {total_duplicates}\n")
            for duplicate in dups:
                logfile.write(f"Deleted: {duplicate}\n")

        return log_filename, total_files, total_duplicates

    except Exception as e:
        print(f"Error occurred while processing files: {e}")
        return None, None, None

def Mailsender(logfile_path, recipient_email, start_time, total_files, total_duplicates):
    fromaddr = "kalmasevaishnavi@gmail.com"
    password =  fromaddr="kalmasevaishnavi@gmail.com"  
    password="azpb mwnj viwd evtp"


    msg = MIMEMultipart()
    msg["From"] = fromaddr
    msg["To"] = recipient_email
    msg["Subject"] = "Duplicate File Removal Log"

    body = f"""
    Hello,
    Welcome to Marvellous Infosystems.
    Please find attached document which contains log of running process.
    Log file is created at: {start_time}

    Total files processed: {total_files}
    Total duplicates removed: {total_duplicates}

    This is an auto-generated email.

    Thanks & Regards,
    Marvellous Infosystems
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(logfile_path, "rb") as attachment:
            p = MIMEBase("application", "octet-stream")
            p.set_payload(attachment.read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', f"attachment; filename={os.path.basename(logfile_path)}")
            msg.attach(p)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, password)
        text = msg.as_string()
        server.sendmail(fromaddr, recipient_email, text)
        server.quit()

        print("Log file successfully sent through email")
    except Exception as e:
        print(f"Unable to send email: {e}")

def is_connected():
    try:
        urlopen("https://www.google.com", timeout=5)
        return True
    except URLError:
        return False

def main():
    print("---- Marvellous Infosystem by Piyush Khairnar ----")
    print("Application name: " + sys.argv[0])

    if len(sys.argv) != 4:
        print("Error: Invalid number of arguments")
        print("Usage: DuplicateFileRemoval.py <Directory> <TimeInterval> <Email>")
        exit()

    try:
        path = sys.argv[1]
        interval = int(sys.argv[2])
        recipient_email = sys.argv[3]

        if not os.path.isdir(path):
            print("Error: Provided path is not a directory.")
            exit()

        if "@" not in recipient_email or "." not in recipient_email:
            print("Error: Invalid email format.")
            exit()

        while True:
            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            display_checksum(path)
            logfile_path, total_files, total_duplicates = removedup(path)
            if logfile_path and is_connected():
                Mailsender(logfile_path, recipient_email, start_time, total_files, total_duplicates)
            else:
                print("There is no internet connection")
            time.sleep(interval * 60)
    except ValueError:
        print("Error: Invalid datatype of input")
    except Exception as e:
        print("Error: Invalid input", e)

if __name__ == "__main__":
    main()