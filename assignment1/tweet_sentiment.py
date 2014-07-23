import sys
import json
import re

def score_terms(afinn_file): # build the dictionary of term-score pairs
    scores = {} # initialize an empty dictionary
    for line in afinn_file:
        term, score  = line.split("\t")  
        scores[term] = int(score)  # convert the score to an integer.
    return scores

def find_ngrams(scores):
    n = []
    for score in scores:
        if " " in score:
            n.append(len(re.split("\W+", score)))
    return max(n)
    
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

def score_tweet(scores, tweet, max_n):
    tweet_score = 0
    if "text" in tweet:
        words = parse_tweet(tweet)
        n = max_n # need to deal with ngrams
        while n > 0:
            for i in range(len(words) - n): 
                nwords = words[i:(i + n)]
                ngram = " ".join(nwords)
                if ngram in scores:
                    tweet_score += scores[ngram] # sum the word-scores for each tweet
                    del words[i:(i + n)] # remove the ngram from words and repeat
                    n += 1
                    break 
            n -= 1
    return tweet_score
    
def score_tweets(scores, tweets, max_n): # score sweets based on the term-score dictionary
    for tweet in tweets:
        tweet_score = score_tweet(scores, tweet, max_n)
        sys.stdout.write(str(tweet_score) + "\n")

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    scores = score_terms(sent_file) 
    max_n = find_ngrams(scores)

    tweets = read_tweets(tweet_file)
        
    score_tweets(scores, tweets, max_n)

if __name__ == '__main__':
    main()
    

