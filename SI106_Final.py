import requests_oauthlib
import json
import webbrowser
client_key = input('Please enter valid client key')
client_secret = input('Please enter valid client secret')
if not client_secret or not client_key:
    print("You need to fill in client_key and client_secret. See comments in the code around line 8-14.")
def tokens():
    oauth = requests_oauthlib.OAuth1Session(client_key, client_secret=client_secret)
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    fetch_response = oauth.fetch_request_token(request_token_url)
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')
    base_authorization_url = 'https://api.twitter.com/oauth/authorize'
    authorization_url = oauth.authorization_url(base_authorization_url)
    print("""Please click on the URL below, 
          click on "Authorize App", 
          and then copy the authorization code and paste it below.""")
    print(authorization_url)
    verifier = input('Please input the verifier>>> ')
    oauth = requests_oauthlib.OAuth1Session(client_key,
                              client_secret=client_secret,
                              resource_owner_key=resource_owner_key,
                              resource_owner_secret=resource_owner_secret,
                              verifier=verifier)
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')
    return (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier)
new_session = tokens()
resource_owner_key = input('Please enter valid resource owner key')
resource_owner_secret = input('Please enter valid resource owner secret')
protected_url = 'https://api.twitter.com/1.1/account/settings.json'
oauth = requests_oauthlib.OAuth1Session(client_key,
                        client_secret,
                        resource_owner_key,
                        resource_owner_secret)
hashtag = input('Insert hashtag here with # symbol in front')
base_search_url = 'https://api.twitter.com/1.1/search/tweets.json'
data = oauth.get(base_search_url,
                 params = {'q':hashtag, 'count':200, 'include_entities':False})
all_tweets = data.json()
all_tweets_narrowed = all_tweets['statuses']
class Tweet():
    def __init__(self, tweet_info={}):
        self.text = tweet_info['text']
        self.name = tweet_info['user']['name']
        self.tweet_id = tweet_info['id']
    def __str__(self):
        return "{} tweeted '{}' with ID #{}".format(self.name, self.text, self.tweet_id)
    def strip_remove_list(self):
        stop_words_lst = ['', "a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the", "rt"]
        punctuation = ['+', '=', ".", "'", '"', "!", ",", "[", "]", "{", "}", "#", "?", "/", "*", "-", "_", "<", ">", "@", ":", ";", '&', '$', '%']
        lst_word_text = self.text.lower().split()
        list_2 = []
        list_3 = []
        final_list = []
        for word in lst_word_text:
            list_2.append(list(word))
        for item in list_2:
            for char in item:
                if char in punctuation:
                    item.remove(char)
            list_3.append(''.join(item))
        for new_word in list_3:
            if new_word not in stop_words_lst and len(new_word) > 4:
                final_list.append(new_word)
        return final_list
list_instances_twitter = []
for tweet in all_tweets_narrowed:
    list_instances_twitter.append(Tweet(tweet))
def most_frequent_word(tweet_list):
    hashtag_stripped = input('Type your hashtag with no # symbol and all lowercase.')
    list_all_words = []
    for tweet in tweet_list:
        for word in tweet.strip_remove_list():
            list_all_words.append(word)
    for word in list_all_words:
        if word == hashtag_stripped:
            list_all_words.remove(word)
    most_frequent_count = 0
    most_frequent_word = ''
    for word in list_all_words:
        if list_all_words.count(word) > most_frequent_count:
            most_frequent_count = list_all_words.count(word)
            most_frequent_word = word
    return most_frequent_word
most_frequent_word = most_frequent_word(list_instances_twitter)
import requests
baseurl = 'https://itunes.apple.com/search'
params = {'term':most_frequent_word, 'media':'music', 'entity':'song'}
itunes = requests.get(baseurl, params)
song_info = itunes.json()
itunes_results = song_info['results']
class Song():
    def __init__(self, song_info={}):
        self.artist_name = song_info['artistName'] 
        self.song_name = song_info['trackName']
        self.song_length_millis = song_info['trackTimeMillis']
        self.song_length_s = str(int(self.song_length_millis)/1000)
        self.album_name = song_info['collectionName']
        self.explicitness = song_info['trackExplicitness']
    def __str__(self):
        return '{} by {} is {} seconds long'.format(self.song_name, self.artist_name, self.song_length_s)
    def is_track_explicit(self):
        if self.explicitness == 'explicit':
            return 'Track is explicit'
        else:
            return 'Track is not explicit'
if len(itunes_results) > 0:
    print(Song(itunes_results[0]))
    print(Song(itunes_results[0]).is_track_explicit())
else:
    None
def create_instance_list(lst):
    list_instances = []
    for song in lst:
        list_instances.append(Song(song))
    return list_instances
if len(itunes_results) > 0:
    list_instances_itunes = create_instance_list(itunes_results)
    sorted_itunes_instances = sorted(list_instances_itunes, key = lambda x: float(x.song_length_s), reverse = True)
else:
    None
import csv
outfile =  open('songs.csv', 'w', newline = '')
writer = csv.DictWriter(outfile, fieldnames = ['song_name', 'artist_name', 'song_length_s', 'album_name', 'explicitness'], delimiter = ',', quotechar = '"', quoting = csv.QUOTE_NONNUMERIC)
writer.writeheader()
for song in sorted_itunes_instances:
    writer.writerow({'song_name':song.song_name, 'artist_name':song.artist_name, 'song_length_s':song.song_length_s, 'album_name':song.album_name, 'explicitness':song.is_track_explicit()})
outfile.close()  