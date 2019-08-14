# YouTube-Political-Video-Network-Analysis
This repository contains the code related to my junior, spring independent work conducted through the Princeton Computer Science Department. In my independent work, I used the YouTube Data API to crawl political videos on YouTube, construct a political bias classifier, and then used Network X to analyze trends in the YouTube recommendation algorithm.

A poster displaying my research results is contained in poster.pdf.

Below I provide a list explaining the purpose of each program, how to run each file in terminal, and the output files. Run the programs in the following order to reproduce my experiment:

## crawler.py
This program conducts the crawl of YouTube videos by calling methods in Youtube_Methods.py which directly interacts with the YouTube Data API. In order
to use Youtube_Methods.py, you'll have to register with the YouTube Data API
using the Google Developer Console and configure an environment variable for your
developer key titled DEVELOPER_KEY. One required runtime argument of crawler.py
is a video ID of a YouTube video that you want to begin your crawl in. All
subsequent videos are chosen based on the suggested videos of the specified
video. I conducted 3 separate crawls each beginning in a video of either
Democratic, Centrist or Republican bias. My crawler includes code to save
the progress of the crawl in case that the quota limit imposed by the YouTube
Data API is reached mid-crawl causing the crawl to terminate prematurely.

python crawler.py <crawl_name> <video_id> <num_suggested> <iter_num_max>
outputs (quota limit reached):
<crawl_name>\_queue.pickle
<crawl_name>\_queue\_backup.pickle
<crawl_name>\_video\_data.json
<crawl_name>\_video\_data\_backup.json

outputs (crawl complete):
<crawl_name>\_video\_data\_complete.json
<crawl_name>\_video\_data\_complete\_backup.json   

## combineCrawls.py
This program combines all separate crawl data output by crawler.py into a single
.json file. It also combines all text fields of the YouTube video data into a
single field for each video in preparation for the bag of words conversion.

python combineCrawls.py <combine_name> <train_or_test> \**files
outputs: <combine_name>\_data\_complete\_pre.csv
<combine_name>\_video\_data\_complete\_pre.json

## prune.py
This program prunes a .json file containing crawl data of all video data recorded in a specific iteration. Note: this file does not have to be used, but it can be used in the case that you want to for example reduce a crawl of 7 iterations to 6 instead.

python prune.py <input_file_name> <output_file_name> <num_to_remove>
outputs: <output_file_name>.json

## wordCounterVectorize.py
This program takes as input a combined crawl data file and converts each video to a bag of words vector. This file is used both for test and training data.

python wordCountVectorizer.py <crawl_file_name> <output_file_name> <min_df> <vocab>
outputs: <output_file_name>\_<min_df>.py
vocab\_<output_file_name>\_<min_df>.py

## durationConvertToTime.py
This program converts the video duration field of each video entry from a string
of the form 'PT#H#M#S' to the video duration in minutes.

python durationConvertToTime.py <file_name>
outputs: <file_name>\_data\_complete\_pre.csv
<file_name>\_video\_data\_complete\_pre.json

## BiasClassifier.ipynb
Contains all of the code related to constructing my political bias classifier
using Sci-Kit Learn. Run this code before proceeding.

## predictLabels.py
This file uses the constructed bias classifier to predict the labels of each
video for the given input file.

python predictLabels.py <bow_file> <combined_file_name> <output_name>
outputs: <output_name>\_predicted.json
<output_name>\_predicted.csv

## NetworkGraphs-ntnc.ipynb
Contains all of the network analysis conducted on the videos with predicted
labels using NetworkX.
