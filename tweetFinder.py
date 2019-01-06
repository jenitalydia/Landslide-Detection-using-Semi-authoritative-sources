#!/usr/bin/env python

import getopt
import os
import sys
import json
import tweepy
import pdb

file_name = 'counter_file.json'

access_token = sys.argv[1]
access_token_secret = sys.argv[2]
consumer_key = sys.argv[3]
consumer_secret = sys.argv[4]


def main():



    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    dict1= {}
    counter = 0


    true_counter = 0
    if os.path.exists('counter_file.json'):
        with open('counter_file.json', 'r') as count_file:
            true_counter = int(count_file.read())

    if not os.path.exists('f.json'):
        open('f.json', 'w').close()


    with open("f.json","r") as f1:
        for line in f1:
            test_dict = json.loads(line.strip())
            dict1[test_dict.keys()[0]] = test_dict[test_dict.keys()[0]]
    #pdb.set_trace()
    #true counter exists, counter exists and the dictionary is loaded into the file
    file = open("tweet-ids-002.txt", "r")

    for line in file:
        counter+=1
        if counter <= true_counter:
            continue

        else:
            #pdb.set_trace()
            line = line.strip()
            try:

                status = api.get_status(line)
            except:

                counter += 1
                with open("counter_file.json", 'w') as c:
                    c.write(json.dumps(counter))
                continue
            #pdb.set_trace()
            status.user.id = str(status.user.id)
            #if status.user.id == "241223988":
                #pdb.set_trace()
            if status.user.id in dict1:
                counter += 1
                with open("counter_file.json", 'w') as c:
                    c.write(json.dumps(counter))
                continue
            else:
                dict1[status.user.id] = status.user.name
                with open("f.json",'a') as f1:
                    test_dict = {status.user.id : dict1[status.user.id]}
                    f1.write(json.dumps(test_dict) + '\n')
            counter += 1
            with open("counter_file.json",'w') as c:
                c.write(json.dumps(counter))



if __name__ == "__main__":

    main()