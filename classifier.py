import pdb
import pandas as pd
import json

TRAIN_SET_PATH = "apriori_data.json"
TEST_SET_DATA = {}



def bow_generate(source_data):
    #we use the bow file in train_src to create our vocabulary
    from sklearn.feature_extraction.text import TfidfVectorizer
    bow_file = 'bow.txt'
    with open(bow_file, 'r') as bow_file:
        bow_doc = bow_file.read()

    # Create the vectorizer and fit the bow document to create the vocabulary
    vectorizer = TfidfVectorizer()
    vectorizer.fit([bow_doc])

    return vectorizer.transform(source_data['text'].values)

def load_file(file_name):
    test = {}
    with open(file_name, 'r') as test_file:
        for line in test_file:
            line = json.loads(line.strip())
            test[line['id_str']] = {}
            test[line['id_str']]['text'] = line['text']
            test[line['id_str']]['label'] = line['label']

    return test


# to run file: /expansion2/afnu6/litmus_studies/_litmus_/bin/python
if __name__ == "__main__":
    #training data
    apriori_file = load_file("apriori_data.json")
    source_data = pd.DataFrame.from_dict(apriori_file, orient='index')
    encoded_data = bow_generate(source_data)


    #testing set:
    aibek_test_file = load_file("aibek_test_converted.json")
    test_source_data = pd.DataFrame.from_dict(aibek_test_file, orient='index')
    encoded_test_data = bow_generate(test_source_data)

    #classifier:
    from sklearn.linear_model import SGDClassifier
    classifier = SGDClassifier()
    classifier.fit(encoded_data, source_data['label'].values)

    from sklearn.metrics import f1_score, precision_score, recall_score

    predictions = classifier.predict(encoded_test_data)
    precision = precision_score(test_source_data['label'].values, predictions)
    recall = recall_score(test_source_data['label'].values, predictions)
    score = f1_score(test_source_data['label'].values, predictions)

    print("precision: " + str(precision))
    print("recall" + str(recall))
    print("score" + str(score))

    parsed_file = load_file("encode_input.json")
    parsed_data = pd.DataFrame.from_dict(parsed_file, orient='index')
    encode_parsed_data = bow_generate(parsed_data)

    prediction = classifier.predict(encode_parsed_data)
    #pdb.set_trace()
    prediction = prediction.tolist()
    se = pd.Series(prediction)
    parsed_data['prediction'] = prediction
    parsed_data.to_csv("prediction_result1.csv",encoding="utf-8")
   
    #keyword matching 
    landslide =  parsed_data.loc[parsed_data['text'].str.contains('landslide',case='False',regex='False')]
    rockslide = parsed_data.loc[parsed_data['text'].str.contains('rockslide',case='False',regex='False')]
    mudslide = parsed_data.loc[parsed_data['text'].str.contains('mudslide',case='False',regex='False')]
    landslides = parsed_data.loc[parsed_data['text'].str.contains('landslides',case='False',regex='False')]
    mudslides = parsed_data.loc[parsed_data['text'].str.contains('mudslides',case='False',regex='False')]
    rockslides = parsed_data.loc[parsed_data['text'].str.contains('rockslides',case='False',regex='False')]
    #pdb.set_trace()
    df = pd.concat([landslide,mudslide,rockslide,landslides,mudslides,rockslides],axis=0)
    df.to_csv("final_output.csv",encoding="utf-8") 
