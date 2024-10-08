# Import the following modules
from pushbullet import Pushbullet
from modules import query

# Get the access token from Pushbullet.com

alert = "⚠️ LufiHome - Alert ⚠️"
info = "✉️ LufiHome - Info ✉️"


def __sendNotification(access_token, header: str, message: str, username: str):
    try:
        pb = Pushbullet(access_token)
        pb.push_note(header, message)
    except:
        print(f'Error to send notification to: {username}')


def send_notification(recipient: str, header: str, message: str):
    users = query.get_allUsers()

    for user in users:
        if recipient == 'admin':
            if user['AccountType'] == 'admin':
                if user['SendMsg'] == 'yes':
                    print(
                        f"sending notification to: {user['UserName']}, {user['AccountType']}")
                    __sendNotification(
                        user['PushBulletToken'], header, message, user['UserName'])
        if recipient == 'all':
            if user['SendMsg'] == 'yes':
                print(
                    f"sending notification to: {user['UserName']}, {user['AccountType']}")
                __sendNotification(user['PushBulletToken'],
                                   header, message, user['UserName'])
