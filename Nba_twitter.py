from bs4 import BeautifulSoup
import tweepy
import time
from datetime import datetime
import requests

#Get current time
def clock():
    current = datetime.now()
    return(str(current) + " EST")

#Twitter credentials
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#List of NBA teams
teams = {'Hawks',
'Celtics',
'Nets',
'Hornets',
'Bulls',
'Cavaliers',
'Mavericks',
'Nuggets',
'Pistons',
'Warriors',
'Rockets',
'Pacers',
'Clippers',
'Lakers',
'Grizzlies',
'Heat',
'Bucks',
'Timberwolves',
'Pelicans',
'Knicks',
'Thunder',
'Magic',
'76ers',
'Suns',
'Blazers',
'Kings',
'Spurs',
'Raptors',
'Jazz',
'Wizards'}

#teams_updated = [x.lower() for x in teams]
#tuple_teams = tuple(teams_updated)

headers = {
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Language':'en-US,en;q=0.9',
'Accept-Encoding':'Accept-Encoding',
}
games_found = 0
#function used to get link for specific team
def get_link(team):
    global games_found
    team = team.title()
    s = requests.session()
    url = 'http://nbastreams.xyz/games/'
    site = s.get(url,headers=headers)
    soup = BeautifulSoup(site.text, 'html.parser')

    table = soup.find('div',{"class": "col-xs-12 col-md-8 col-sm-12"})

    for me in table.find_all('a'):
        heading = me.find_all('h4', {"class": "media-heading"})[0].text
        info = me.find_all('p')[0].text
        link = me['href']
        if team in heading:
            games_found = 1
            time = info.split('-')[1]
            return heading + " " + "@" + link + ' the game starts at' + time
            time.sleep(5)
    if games_found == 0:
        return ' There is no link available for today. Try again on game day!'
        time.sleep(5)

#print(get_link('rockets'))

#Place file path to txt file here
FILE_NAME = ''


def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

#print(retrieve_last_seen_id(FILE_NAME))

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

#Check mentions for NBA team
def reply_to_tweets():
    #Starts off from last seen ID
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # Get mentions
    mentions = api.mentions_timeline(since_id=last_seen_id)
    # mentions = api.mentions_timeline(since_id=last_seen_id)
    for mention in reversed(mentions):
        #Going through str in mentions after @
        nba = mention.text[12:24].title()
        num = str(mention.id)
        name = mention.user.screen_name
        #NBA team name found in mentions
        if nba in teams:
            last_seen_id = num
            store_last_seen_id(last_seen_id, FILE_NAME)
            nba_team = nba
            game = get_link(nba_team)
            if game == None:
                time.sleep(5)
                reply_to_tweets()
            print(clock(), ('::::'), 'Getting link for the ' + nba_team + ' game')
            print(clock(), ('::::'), 'Replying to tweet')
            try:
                if games_found == 0:
                    api.update_status('@' + name + game, mention.id)
                    print(clock(), ('::::'), 'Sent reply')
                    print()
                    time.sleep(5)
                if games_found == 1:
                    api.update_status('@' + name + game, mention.id)
                    print(clock(), ('::::'), 'Sent reply')
                    print()
                    time.sleep(5)
            except:
                print(clock(), ('::::'), 'Error somewhere. Trying again')
                reply_to_tweets()

while True:
    reply_to_tweets()
    time.sleep(10)
