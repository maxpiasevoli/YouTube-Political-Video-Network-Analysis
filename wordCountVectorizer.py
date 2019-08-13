import sys, json, operator
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pickle
from operator import itemgetter

# generates bag of words for each video in a dataset. used both for test and training data

def wordCountVectorize(input_file_name, name, min_df, vocab):

    # read in next dictionary
    video_data = None
    videos_single_string = {}
    with open('{0}.json'.format(input_file_name), 'r') as dest:
        video_data = json.load(dest)

    if vocab:
        with open(vocab, 'rb') as dest:
            vocab = pickle.load(dest)

    video_data_list = []
    if vocab == None:
        for key, value in video_data.items():
            temp = [key,value['label'], value['string']]
            video_data_list.append(temp)
        video_data_list = sorted(video_data_list, key=itemgetter(1))
    if vocab:
        for key, value in video_data.items():
            temp = [key,None, value['string']]
            video_data_list.append(temp)

    strings = []
    sample_num = 1
    # construct known labels if training set
    if vocab == None:
        with open('classes_{0}_{1}.txt'.format(name, min_df), 'w') as dest:
            for item in video_data_list:
                string = item[2].encode('ascii', 'ignore').decode("utf-8").replace("\n","")
                strings.append(string)
                sample_num += 1
                dest.write(str(item[1]) + '\n')
    else:
        for item in video_data_list:
            string = item[2].encode('ascii', 'ignore').decode("utf-8").replace("\n","")
            strings.append(string)
            sample_num += 1
    with open('reference_{0}_{1}.txt'.format(name, min_df), 'w') as dest:
        num_ids = 0
        for item in video_data_list:
            dest.write(item[0] + '\n')
            num_ids += 1
    print('Num Ids: ', num_ids)

    stop_words = stopwords.words('english') + ['facebook', 'twitter', 'https', 'subscriber',
                'facebookhttps', 'bit', 'ly', 'http', 'com', 'fb', 'visit', 'www', 'subscribe',
                'watch', 'full', 'episode', 'snapchat', 'feb', 'mar', 'watch',
                'full', 'episode', 'playlist', 'video', 'pinterest', 'videos',
                'click', 'network', 'pg', 'ep', 'youtube', 'itunes', 'instagram',
                'fuck', 'shit', 'bitch', 'google', 'plus', 'follow', 'tv', 'fucking',
                'damn', 'media', 'actually', 'happening', 'latest', 'onlinevisit', 'funny', 'go', 'discusses', 'homepage'] + ['late', 'show',
                'daily', 'wire', 'stephen', 'abcnews', 'facebook', 'twitter',
                'likemsnbcfollow', 'abcnewsfollow','wsjon', 'followmsnbcfollow',
                'cbs', 'wall', 'street', 'journal', 'gma', 'fnc', 'news',
                'anderson', 'cooper', 'rachel', 'maddow', 'ari', 'melber',
                'mika', 'ben', 'klavan', 'shapiro', 'knowles','tucker', 'juan',
                'michael', 'matt', 'letterman', 'hannity', 'laura', 'tucker',
                'carlson', 'nightline', 'morning', 'chris', 'david', 'andrew',
                'comvisit', 'videoon', 'sean', 'wsjvideofollow', 'ingraham', 'joe', 'don',
                 'lemon', 'roger', 'lawrence', 'abcgood', 'jordan', 'martha', '2ratjsm', 'headlines',
                  '14q81xymore', 'wsjlivefollow', 'wsjfollow', 'larry', 'current', 'events', 'newsletter', 'talk'] + ['news', 'like', '20', '2016',
                   '2017', '2018', '2019', '35', '11th', 'pm', 'channel', 'newsroom', 'comfollow', 'postsfollow',
                   'exclusive', 'tonight' ,'speaks','special', 'america', 'good',
                   'beautiful', 'great', 'dont', 'report', 'miss']


    stop_words = stop_words + ['fox', 'foxnews', 'bloomberg', 'abc','wsj', 'dailywire', 'cnn', 'msnbc', 'colbert']

    vectorizer = CountVectorizer(stop_words = stop_words, max_df=len(strings), min_df=int(min_df), ngram_range=(1,2), vocabulary=vocab)
    X = vectorizer.fit_transform(strings)
    print('Array dim: ', X.shape)

    np.save('{0}_{1}'.format(name, min_df), X)

    if vocab == None:
        with open('vocab_{0}_{1}.pickle'.format(name, min_df), 'wb') as dest:
            pickle.dump(vectorizer.get_feature_names(), dest)
        np.save('vocab_{0}_{1}'.format(name, min_df), vectorizer.get_feature_names())

    print('Strings Vectorized.')

def main():
    # python wordCountVectorizer.py <output file name> <crawl file name> <min_df> <vocabulary>
    input_file_name = sys.argv[1]
    name = sys.argv[2]
    min_df = sys.argv[3]
    vocab = sys.argv[4]
    if vocab == 'None':
        vocab = None
    else:
        vocab = vocab + '.pickle'

    wordCountVectorize(input_file_name, name, min_df, vocab)

if __name__ == '__main__':
    main()
