import sys, json, operator
import pandas as pd

# converts video duration from 'PT#H#M#S' to minutes

def convertDuration(file_name):
    with open('{0}_video_data_complete_pre.json'.format(file_name), 'r') as dest:
        video_data = json.load(dest)

    for key, value in video_data.items():
        duration_string = value['duration']
        last_field = duration_string.find('T')
        hours = 0
        minutes = 0
        seconds = 0
        if duration_string.find('H') > 0:
            stop = duration_string.find('H')
            hours = int(duration_string[last_field + 1:stop])
            last_field = stop
        if duration_string.find('M') > 0:
            stop = duration_string.find('M')
            minutes = int(duration_string[last_field + 1:stop])
            last_field = stop
        if duration_string.find('S') > 0:
            stop = duration_string.find('S')
            seconds = int(duration_string[last_field + 1:stop])

        total_mins = hours * 60 + minutes + seconds/60
        video_data[key]['time'] = total_mins

    with open('{0}_video_data_complete_pre.json'.format(file_name), 'w') as dest:
        json.dump(video_data, dest, indent=4)

    df = pd.DataFrame.from_dict(video_data, orient='index')
    export_csv = df.to_csv ('{0}_data_complete_pre.csv'.format(file_name), header=True)

    print('Time fields generated. Dictionary stored. ')

# python durationConvertToTime.py <file_name>
# file_name: the prefix preceding _video_data_complete_pre.json of the input file
def main():
    file_name = sys.argv[1]
    convertDuration(file_name)

if __name__ == '__main__':
    main()
