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

def state_abbr():
    state_dict = {
        "Alaska": "AK", "Alabama": "AL", "Arkansas": "AR", "American Samoa": "AS",
        "Arizona": "AZ", "California": "CA", "Colorado": "CO", "Connecticut": "CT",
        "District of Columbia": "DC", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
        "Guam": "GU", "Hawaii": "HI", "Iowa": "IA", "Idaho": "ID", "Illinois": "IL",
        "Indiana": "IN", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
        "Massachusetts": "MA", "Maryland": "MD", "Maine": "ME", "Michigan": "MI",
        "Minnesota": "MN", "Missouri": "MO", "Northern Mariana Islands": "MP", 
        "Mississippi": "MS", "Montana": "MT", "National": "NA", "North Carolina": "NC",
        "North Dakota": "ND", "Nebraska": "NE", "New Hampshire": "NH", "New Jersey": "NJ",
        "New Mexico": "NM", "Nevada": "NV", "New York": "NY", "Ohio": "OH",
        "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Puerto Rico": "PR",
        "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
        "Tennesee": "TN", "Texas": "TX", "Utah": "UT", "Virginia": "VA",
        "Virgin Islands": "VI", "Vermont": "VT", "Washington": "WA", "Wisconsin": "WI",
        "West Virginia": "WV", "Wyoming": "WY"
    }
    abbrs = []
    for state in state_dict:
        abbrs.append(state_dict[state])
    return state_dict, abbrs
    
def parse_tweet_state(tweet):
    state = "Unknown"
    if "place" in tweet:
            if tweet["place"] != None:
                tweet_place = tweet["place"]
                if tweet_place["country_code"] == "US":
                    place_name = re.split(", ", tweet_place["full_name"])
                    state_to_abbr, abbrs = state_abbr()
                    for name in place_name:
                        if name in abbrs:
                            state = name
                        elif name in state_to_abbr:
                            state = state_to_abbr[name]
    return state
    
def find_states(tweets):
    tweet_states = {}
    for idx,tweet in enumerate(tweets):
        state = parse_tweet_state(tweet)
        if state in tweet_states:
            tweet_states[state].append(idx)
        else:
            tweet_states[state] = [idx]
    return tweet_states

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
    tweet_scores = []
    for tweet in tweets:
        tweet_score = score_tweet(scores, tweet, max_n)
        tweet_scores.append(tweet_score)
    return tweet_scores
        
def score_states(tweet_scores, states):
    state_scores = {}
    for idx,state in enumerate(states):
        tweet_idx = states[state]
        state_score = 0
        for idx in tweet_idx:
            state_score += tweet_scores[idx]
        state_score = float(state_score)/float(len(tweet_idx))
        state_scores[state] = state_score
    return state_scores

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    scores = score_terms(sent_file) 
    max_n = find_ngrams(scores)
    
    tweets = read_tweets(tweet_file)
    tweet_states = find_states(tweets)
    
    tweet_scores = score_tweets(scores, tweets, max_n)

    state_scores = score_states(tweet_scores, tweet_states)
    sys.stdout.write(str(max(state_scores, key = state_scores.get)) + "\n")
    
if __name__ == '__main__':
    main()