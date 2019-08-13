import Youtube_Methods as yt
import pickle
import pandas as pd
import sys, json


# given videoId of starting video, perform webcrawl
def crawl(crawl_name, video_id, num_suggested, iter_num_max):
    Queue = None
    video_data = None
    ITER_NUM_MAX = iter_num_max
    videos_added = 0

    # if video_id is None, read in queue and video_data
    if(video_id == None):
        with open('{0}_queue.pickle'.format(crawl_name), 'rb') as dest:
            Queue = pickle.load(dest)
        with open('{0}_video_data.json'.format(crawl_name), 'r') as dest:
            video_data = json.load(dest)

    #if not, start new file
    else:
        Queue = []
        first_tuple = (video_id, 0, None)
        Queue.append(first_tuple)
        video_data = {}

    # perform crawl
    next_tuple = None
    mid_retrieval = False
    try:
        while(len(Queue) > 0):
            next_tuple = Queue.pop(0)
            video_id = next_tuple[0]
            iter_num = next_tuple[1]
            pointer = next_tuple[2]
            mid_retrieval = True # indicates whether retrieval in-process

            # if video_id is already exists, add
            if video_id in video_data.keys():
                video_data[video_id]['pointers'].append(pointer)

                # add next num_suggested videos to Queue
                if (iter_num != ITER_NUM_MAX):
                    options = {'q':'politics', 'max_results':50, 'relatedToVideoID':video_id}
                    _, __, ___, search_response_related = yt.youtube_search_related(options)
                    video_id_list = []

                    try: # add next interval of num_suggested videos to Queue
                        offset = len(video_data[video_id]['pointers'])
                        for i in range(offset * num_suggested, (offset + 1) * num_suggested):
                            video = search_response_related.get("items", [])[i]
                            onboarding_tuple = (video ['id']['videoId'], iter_num + 1, video_id)
                            video_id_list.append(onboarding_tuple)
                    except: # array overflow; visit first interval of num_suggested videos again
                        video_id_list = []
                        for i in range(num_suggested):
                            #print(i)
                            video = search_response_related.get("items", [])[i]
                            onboarding_tuple = (video ['id']['videoId'], iter_num + 1, video_id)
                            video_id_list.append(onboarding_tuple)

                    # add related videos to Queue
                    Queue += video_id_list
            else:
                # retrieve current video's data
                video_list_result = yt.videos_list_by_id(
                    part='snippet,contentDetails',
                    id=video_id)
                video_list_result = video_list_result.get('items', [])[0]
                title = video_list_result['snippet']['title']
                description = video_list_result['snippet']['description']
                publishedAt = video_list_result['snippet']['publishedAt']
                channelTitle = video_list_result['snippet']['channelTitle']
                try:
                    tags = video_list_result['snippet']['tags']
                except:
                    tags = ['']
                duration = video_list_result['contentDetails']['duration']

                # try except here in case comments are disabled for current video
                try:
                    comment_thread = yt.comment_threads_list_by_video_id(
                        part='snippet',
                        videoId=video_id,
                        maxResults=100)

                    comments = []
                    for comment in comment_thread.get("items", []):
                        comments.append(comment['snippet']['topLevelComment']['snippet']['textOriginal'])

                    comments = yt.remove_emojis(comments)
                except:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print('Type: {0} \n Line Number: {1}'.format(exc_type, exc_tb.tb_lineno))
                    #print('Error: {0}'.format(e))
                    comments = ['']
                    print('Empty Comment Array Inserted')


                # retrieve related videos if iter_num != ITER_NUM_MAX
                if (iter_num != ITER_NUM_MAX):
                    options = {'max_results':50, 'relatedToVideoID':video_id}
                    _, __, ___, search_response_related = yt.youtube_search_related(options)
                    video_id_list = []
                    for i in range(num_suggested):
                        video = search_response_related.get("items", [])[i]
                        onboarding_tuple = (video ['id']['videoId'], iter_num + 1, video_id)
                        video_id_list.append(onboarding_tuple)

                    # add related videos to Queue
                    Queue += video_id_list

                # add current video's data to dictionary
                video_data[video_id] = {}
                video_data[video_id]['title'] = title
                video_data[video_id]['description'] = description
                video_data[video_id]['publishedAt'] = publishedAt
                video_data[video_id]['channelTitle'] = channelTitle
                video_data[video_id]['tags'] = tags
                video_data[video_id]['comments'] = comments
                video_data[video_id]['pointers'] = [pointer]
                video_data[video_id]['iterNum'] = iter_num
                video_data[video_id]['duration'] = duration
                mid_retrieval = False
                videos_added += 1
                print(videos_added)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print('Type: {0} \n Line Number: {1}'.format(exc_type, exc_tb.tb_lineno))
        print('Error: {0}'.format(e))
        print(next_tuple)

        #pop back most recent tuple if quota limit reached mid retrieval
        if (mid_retrieval):
            Queue.insert(0, next_tuple)

        #pickle queue
        with open('{0}_queue.pickle'.format(crawl_name), 'wb') as dest:
            pickle.dump(Queue, dest)

        with open('{0}_queue_backup.pickle'.format(crawl_name), 'wb') as dest:
            pickle.dump(Queue, dest)

        #json dump video_data
        with open('{0}_video_data.json'.format(crawl_name), 'w') as dest:
            json.dump(video_data, dest, indent=4)

        with open('{0}_video_data_backup.json'.format(crawl_name), 'w') as dest:
            json.dump(video_data, dest, indent=4)

        #create csv of data so far with length of video_data
        vd_length = len(video_data)
        df = pd.DataFrame.from_dict(video_data, orient='index')
        export_csv = df.to_csv (r'{0}_data_{1}.csv'.format(crawl_name, vd_length), header=True)

        print('Quota Cost Limit Reached. Data stored and CSV printed.')
        print('{0} videos added.'.format(videos_added))

        exit()

    # export completed data to csv
    df = pd.DataFrame.from_dict(video_data, orient='index')
    export_csv = df.to_csv ('{0}_data_complete.csv'.format(crawl_name), header=True)
    print('Crawl complete.')
    print('{0} videos added.'.format(videos_added))

    # save video_data in json format
    with open('{0}_video_data_complete.json'.format(crawl_name), 'w') as dest:
        json.dump(video_data, dest, indent=4)

    with open('{0}_video_data_complete_backup.json'.format(crawl_name), 'w') as dest:
        json.dump(video_data, dest, indent=4)

# python crawler.py <crawl_name> <video_id> <num_suggested> <iter_num_max>
def main():
    crawl_name = sys.argv[1]
    video_id = sys.argv[2]
    print('Video Exists: ', video_id == '0')
    if (video_id == '0'):
        video_id = None
    num_suggested = int(sys.argv[3])
    iter_num_max = int(sys.argv[4])
    print('Crawl Name: {0}'.format(crawl_name))
    print('Video_id: {0}'.format(video_id))
    print('Number of Suggested Videos: {0}'.format(num_suggested))
    print('Max number of iterations: {0}'.format(iter_num_max))
    
    crawl(crawl_name, video_id, num_suggested, iter_num_max)

if __name__ == '__main__':
    main()
