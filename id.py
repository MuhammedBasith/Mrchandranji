from config import create_api


api = create_api()


#Returns the screen name of the user who tagged the bot in the last mmetionmention 
def screen_name_generator():

    mentions = api.mentions_timeline()
    user_screen_name = mentions[0].user.screen_name

    return user_screen_name


#For the file name, Returns the second last mentions tweet id
def sinceid_generator():

    mentions = api.mentions_timeline()
    mention_id = mentions[1].id

    return mention_id


#Last mentions tweet id
def last_id_generator():

    mentions = api.mentions_timeline()
    mention_id = mentions[0].id

    return mention_id


#Returns the text of the last mentioned tweet
def last_tweet_text_generator():
    mentions = api.mentions_timeline()
    text = mentions[0].text

    return text
