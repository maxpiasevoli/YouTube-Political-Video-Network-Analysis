import sys, json, operator
import pandas as pd

# combines classifier data into a single dataset. also combines text fields into a single string field
def combine(combine_name, file_names, labels, isTrain):
    all_data = {}

    for file in file_names:

        # read in next dictionary
        video_data = None
        videos_single_string = {}
        with open('{0}_video_data_complete.json'.format(file), 'r') as dest:
            video_data = json.load(dest)

        # reconstruct dictionary after combining text fields
        for key in video_data:
            combined_text = ''
            combined_text += video_data[key]['title'] + ' '
            combined_text += video_data[key]['description'] + ' '

            for comment in video_data[key]['comments']:
                combined_text += comment + ' '

            videos_single_string[key] = {}
            videos_single_string[key]['string'] = combined_text
            if isTrain:
                videos_single_string[key]['label'] = labels[file]
            videos_single_string[key]['publishedAt'] = video_data[key]['publishedAt']
            videos_single_string[key]['channelTitle'] = video_data[key]['channelTitle']
            videos_single_string[key]['title'] = video_data[key]['title']
            videos_single_string[key]['description'] = video_data[key]['description']
            videos_single_string[key]['tags'] = video_data[key]['tags']
            videos_single_string[key]['comments'] = video_data[key]['comments']
            videos_single_string[key]['pointers'] = video_data[key]['pointers']
            videos_single_string[key]['iterNum'] = video_data[key]['iterNum']
            videos_single_string[key]['duration'] = video_data[key]['duration']

        # merge current dictionary with all_data
        all_data = {**all_data, **videos_single_string}

    # export completed data to csv
    df = pd.DataFrame.from_dict(all_data, orient='index')
    export_csv = df.to_csv ('{0}_data_complete_pre.csv'.format(combine_name), header=True)
    print('Dictionaries combined.')

    # save video_data in json format
    with open('{0}_video_data_complete_pre.json'.format(combine_name), 'w') as dest:
        json.dump(all_data, dest, indent=4)

# python combineCrawls.py <combine_name> <train_or_test> **files
# combine_name: the prefix name to be included in all output files
# train_or_test: must either be 'train' or 'test' specifying whether this is
# train or test data for the bias classifier
# **files: a list of files of the form *_video_data_complete.json to be combined
def main():
    num_files = len(sys.argv) - 3
    combine_name = sys.argv[1]
    train_or_test = sys.argv[2]
    file_names = []
    for i in range(3, 3 + num_files):
        file_names.append(sys.argv[i])
    if train_or_test == 'train':
        labels = {}
        print('0 for liberal, 1 for conservative, 2 for centrist')
        for name in file_names:
            next = int(input('Bias of {0}?'.format(name)))
            labels[name] = next
    elif train_or_test == 'test':
        labels = None
        isTrain = False
    else:
        print('Please specify train or test as second argument.')
        exit()
    print(combine_name)
    print(file_names)
    print(labels)

    combine(combine_name, file_names, labels, isTrain)

if __name__ == '__main__':
    main()
