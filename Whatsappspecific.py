import pywhatkit as kit
from datetime import datetime
import sys

def sendmessage(phone_no,message,target_hour,target_minute):
    now=datetime.now()
    hour=now.hour
    minute=now.minute+2

    if minute>=60:
        minute -=60
        if hour>=24:
            hour-=24

   
    kit.sendwhatmsg(phone_no,message,target_hour,target_minute)   


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <phone_no> <message> <target_hour> <target_minute>")
    else:
        phone_no = sys.argv[1]
        msg = sys.argv[2]
        target_hour = int(sys.argv[3])
        target_minute = int(sys.argv[4])
        sendmessage(phone_no, msg, target_hour, target_minute)

        

    
     
       

      