import sys, json, operator
import pandas as pd

# prunes a specified layer of the crawl

def prune(input_file_name, output_file_name, num_to_remove):
    with open('{0}.json'.format(input_file_name), 'r') as dest:
        video_data = json.load(dest)

    pruned_video_data = {}
    for key, value in video_data.items():
        if value['iterNum'] != num_to_remove:
            pruned_video_data[key] = video_data[key]

    with open('{0}.json'.format(output_file_name), 'w') as dest:
        json.dump(pruned_video_data, dest, indent=4)

    df = pd.DataFrame.from_dict(pruned_video_data, orient='index')
    export_csv = df.to_csv ('{0}.csv'.format(output_file_name), header=True)

    print('Pruned video data stored.')

# python prune.py <input_file_name> <output_file_name> <num_to_remove>
# input_file_name: the name of the file to be pruned. Must be a .json file with
# crawl data
# output_file_name: name of the output file
# num_to_remove: the number of the iteration to remove 
def main():
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    num_to_remove = int(sys.argv[3])
    prune(input_file_name, output_file_name, num_to_remove)

if __name__ == '__main__':
    main()
