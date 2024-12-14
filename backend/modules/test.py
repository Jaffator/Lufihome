import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/home/jaffator/Home_Security/Flask_Server/Main_App/backend')))
from classes import temperature
import query



import json

# Příklad slovníku
tempdict = {
        "id": int,
        "temp": int,
        "status": bool
    }
templist = []
tempdict['id'] = 12
templist.append(tempdict)


print(templist)