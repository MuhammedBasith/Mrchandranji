import tweepy
import logging
import time
from direct import send_messages
from config import create_api
from id import sinceid_generator, last_id_generator, screen_name_generator, last_tweet_text_generator


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


#Recursively fetches tweets in a thread and returns a list with each tweets as it's elements.
def unroll_thread(tweet, api):
    
    text = []
    rep_status = tweet.in_reply_to_status_id
    user_id = tweet.in_reply_to_user_id
    
    def recur(rep_status):
        
#         print(rep_status)
        if rep_status == None:
            return 
        status = api.get_status(rep_status, tweet_mode='extended')
        text.append(status.full_text)
        
        rep_status = status.in_reply_to_status_id
        user2_id = status.in_reply_to_user_id
#         print(user_id,rep_status)
        if user_id == user2_id:
            recur(rep_status)

    recur(rep_status)
            
    return text[::-1]


#Writes each tweets by joining each element of the list obtained from the previous function in to a specified file. 
def Thread_unroll(api,since_id):

    logger.info("Collecting info")

    new_since_id = since_id

    for tweet in tweepy.Cursor(api.mentions_timeline,since_id=since_id).items():

        new_since_id = max(tweet.id, new_since_id)

        if tweet.in_reply_to_status_id is not None:

            text = unroll_thread(tweet,api)


            if len(text) > 1:

                # name = tweet.id
                txt = open('thread_saver_file.txt','w+')
                text = "\n".join(text)
                txt.write(text)

    return new_since_id

#--------------------------------------------Main Function----------------------------------------------------

def main():
    api = create_api()
    since_id = sinceid_generator()
    text_last_tweet = last_tweet_text_generator()

    while True:
        #Checks for the keyword 
        if 'comeon' in text_last_tweet.lower():
            print('Keyword found!')
            print('Extracting the thread...')

            since_id = Thread_unroll(api,since_id)
            
            try:

                screen_name_of_user = screen_name_generator()
                # file_name = file_name_generator()
                last_tweet_id = last_id_generator()

                with open('thread_saver_file.txt', 'r') as test_file:
                    value = test_file.read().strip()
                    
                    #To retrieve the last Succesfull DMed tweet ID and saves it to a variable for further checking
                    with open('last_tweet_id.txt', 'r') as read_saved:
                        last_id_to_check = read_saved.read().strip()

                    #Condition to check if message already sent once
                    if int(last_tweet_id) != int(last_id_to_check):
                        send_messages(screen_name_of_user, value)
                        print(f'DM Successfully sent to {screen_name_of_user}!')
                        print()

                        #If successfuly DMed, Saves the current tweet id in to the `last_tweet_id` text file
                        with open('last_tweet_id.txt', 'w') as save:
                            save.write(str(last_tweet_id))
                            
                    #TODO Testing pourpouses
                    else:
                        print('Multiple DM\'s restricted')



            except FileNotFoundError:
                pass

        #TODO Testing pourpouses
        else:
            print('\'Comeon\' not found')


        logger.info("Waiting...")
        time.sleep(15)


#------------------------------------------------Body---------------------------------------------------------


if __name__ == "__main__":
    main()
