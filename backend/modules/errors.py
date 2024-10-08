
from datetime import datetime

Text_ReadOutput = "Error: Read output digital pin from database"
ErorrFile = "/home/jaffator/Home Security/Flask Server/Main_App/ErorrLog.txt"


def save_error(error_text):
    with open(ErorrFile, 'a') as f:
        dt = datetime.now().strftime('%y-%m-%d %H:%M:%S')
        f.write(f"{dt}  {error_text} \n")
