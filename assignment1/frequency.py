import sys
import json
import re

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
    words = []
    if "text" in tweet:
        tweet = tweet["text"].encode("utf-8").lower()
        words = re.split(" ", tweet) # split tweets by spaces or punctuation
        words = clean_words(words)
    return words
    
def count_terms(tweets):
    term_counts = {}
    for idx, tweet in enumerate(tweets):
        words = parse_tweet(tweet)
        if len(words) > 0:
            for word in words:
                if len(word) > 0:
                    if word in term_counts:
                        term_counts[word] += 1
                    else: term_counts[word] = 1
    return term_counts 

def main():
    tweet_file = open(sys.argv[1])
    
    tweets = read_tweets(tweet_file)
    term_counts = count_terms(tweets)
    term_total = float(0)
    for term in term_counts:
        term_total += term_counts[term]
    for term in term_counts:
        sys.stdout.write(term + " " + str(float(term_counts[term])/term_total) + "\n")

if __name__ == '__main__':
    main()