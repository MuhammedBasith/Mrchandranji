from config import create_api



api = create_api()


#Function which sends message to the specified User.
def send_messages(screen_name, message_text):
    profile_id = api.get_user(screen_name).id
    api.send_direct_message(str(profile_id), text=message_text)
