import os
import json
arr= []

for subdir, dirs, files in os.walk('/Users/jenita/PycharmProjects/TweetFinder/news_tweets_2018'):
    for file in files:
        filepath = subdir + os.sep + file

        if filepath.endswith(".json"):
            arr.append(filepath)

for i in range(len(arr)):
    try:
        with open(arr[i],'r') as tweets:
            final_list= []
            for line in tweets:
                line = json.loads(line.strip())

                with open("encode_input.json", 'a') as file1:

                    d = {
                        'timestamp_ms': line['timestamp_ms'],
                        'id_str': line['id_str'],
                        'text': line['text'],
                        'label': 0
                    }
                    file1.write(json.dumps(d) + '\n')

    except:
        continue

