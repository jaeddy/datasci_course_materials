import sys
import json
import re
import operator

def read_tweets(tweet_file): # read tweets from JSON format into a list
    tweets = []
    for line in tweet_file:
        tweets.append(json.loads(line))
    return tweets

def clean_words(words):            
    cleaned_words = words
    for i in range(len(words)):
        new_word = re.match(r"(.*\w+'*\w*)", words[i])
        if new_word != None:
            new_word = new_word.groups()
            cleaned_words[i] = new_word[0]
        else:
            cleaned_words[i] = ""
    return cleaned_words

def parse_tweet(tweet):
    tweet = tweet["text"].encode("utf-8").lower()
    words = re.split(" ", tweet) # split tweets by spaces or punctuation
    words = clean_words(words)
    return words

def parse_tweet_hashtag(tweet):
    tweet_hashtags = []
    if "entities" in tweet:
        hashtags = tweet["entities"]["hashtags"]
        if len(hashtags) > 0:
            for entry in hashtags:
                hashtag = entry["text"]
                tweet_hashtags.append(hashtag)
    return tweet_hashtags
    
def count_hashtags(tweets):
    hashtag_counts = {}
    for idx, tweet in enumerate(tweets):
        hashtags = parse_tweet_hashtag(tweet)
        if len(hashtags) > 0:
            for hashtag in hashtags:
                if hashtag in hashtag_counts:
                    hashtag_counts[hashtag] += 1
                else:
                    hashtag_counts[hashtag] = 1
    return hashtag_counts 

def main():
    tweet_file = open(sys.argv[1])
    
    tweets = read_tweets(tweet_file)
    hashtag_counts = count_hashtags(tweets)

    sorted_hashtags = sorted(hashtag_counts.iteritems(), key = operator.itemgetter(1),
        reverse = True)
    for i in range(10):
        hashtag = sorted_hashtags[i][0]
        freq = sorted_hashtags[i][1]
        sys.stdout.write(hashtag + " " + str(float(freq)) + "\n")

if __name__ == '__main__':
    main()