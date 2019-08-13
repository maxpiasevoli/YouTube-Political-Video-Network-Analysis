from apiclient.discovery import build
from apiclient.errors import HttpError
import re, os

#
# A majority of this code is taken from the examples provided on the Youtube
# Data API documentation website where they provide code samples. Slight alterations
# were made as needed for this project.
#

# Define constants
DEVELOPER_KEY = os.environ['DEVELOPER_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# search related videos
def youtube_search_related(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options['q'],
    #q='Mueller', # for Mueller topic crawl
    #q='economy', # for world news topic crawl
    part="id,snippet",
    maxResults=options['max_results'],
    relatedToVideoId=options['relatedToVideoID'],
    relevanceLanguage='en', # newly added,
    #videoCategoryId=25, # newly added
    type='video'
  ).execute()

  videos = []
  channels = []
  playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))

  return videos, channels, playlists, search_response

# given part and videoId, return video list dict
def videos_list_by_id(**kwargs):

  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  response = youtube.videos().list(
    **kwargs
  ).execute()

  return response

# uses commentThreads instead of comments
def comment_threads_list_by_video_id(**kwargs):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  response = youtube.commentThreads().list(
    **kwargs
  ).execute()

  return response

# indendation might be screwed here
def channel_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    part="id,snippet",
    channelId=options['channelId'],
    maxResults=50,
    pageToken=options['pageToken'],
    videoCategoryId=25,
    type='video'
  ).execute()

  videos = []
  channels = []
  playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))

  return videos, channels, playlists, search_response

# The remove_emojis method was taken from a stackoverflow post cited below:
# https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
#

# removes emojis
def remove_emojis(pre_comments):
    edited_comments = []
    for comment in pre_comments:
        emoji_pattern = re.compile("["
                    u"\U0001F600-\U0001F64F"  # emoticons
                    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                    u"\U0001F680-\U0001F6FF"  # transport & map symbols
                    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                       "]+", flags=re.UNICODE)
        new_comment = emoji_pattern.sub(r'', comment)
        edited_comments.append(new_comment)
    return edited_comments
