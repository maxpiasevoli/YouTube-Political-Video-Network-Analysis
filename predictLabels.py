import sys, json, operator
import pandas as pd
import numpy as np
import pickle

#predicts labels of videos using bias classifier

def predictLabels(bow_file, combined_file_name, output_name):
    X = (np.load('{0}.npy'.format(bow_file)))
    X = X.item()

    # load classifier
    with open('BiasClassifier_ntnc.pickle', 'rb') as dest:
        classifier = pickle.load(dest)

    # load rfecv support
    with open('ClassifierSupport_ntnc.pickle', 'rb') as dest:
        support = pickle.load(dest)
    X = X[:, support]

    # predict labels
    predicted_labels = classifier.predict(X)

    # load in combined dictionary
    with open('{0}.json'.format(combined_file_name), 'r') as dest:
        video_data = json.load(dest)

    # load in order of video ids
    with open('reference_{0}.txt'.format(bow_file), 'r') as dest:
        video_ids = dest.read().split('\n')
        video_ids = video_ids[0:-1] # omit empty string

    for i in range(len(video_ids)):
        video_data[video_ids[i]]['Predicted Label'] = predicted_labels[i]

    with open('{0}_predicted.json'.format(output_name), 'w') as dest:
        json.dump(video_data, dest, indent=4)

    df = pd.DataFrame.from_dict(video_data, orient='index')
    export_csv = df.to_csv ('{0}_predicted.csv'.format(output_name), header=True)

    print('Video data updated with predicted labels.')

# python predictLabels.py <bow_file> <combined_file_name> <output_name>
def main():
    bow_file = sys.argv[1] # file name of bag of words output of WordCountVectorizer.py
    combined_file_name = sys.argv[2] # combined crawl data file name
    output_name = sys.argv[3] # desired name of output file
    predictLabels(bow_file, combined_file_name, output_name)

if __name__ == '__main__':
    main()
