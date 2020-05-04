from __future__ import print_function
import os
import csv
import glob
import scipy
import sklearn
import numpy as np
import hmmlearn.hmm
import sklearn.cluster
import pickle as cpickle
import matplotlib.pyplot as plt
from scipy.spatial import distance
import sklearn.discriminant_analysis
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import MidTermFeatures as mtf
from pyAudioAnalysis import ShortTermFeatures as stf
from pyAudioAnalysis import audioSegmentation
import pyAudioAnalysis
import sounddevice as sd
from scipy.io.wavfile import write
from pyAudioAnalysis import audioTrainTest as aT
import boto3
import time

fs = 44100  # Sample rate
seconds = 30  # Duration of recording It likes long recordings better for speaker diarization

result = "whatever you want, I don't know yet"

aT.feature_extraction_train_regression("data/speechEmotion/", 1, 1, aT.shortTermWindow, aT.shortTermStep, "svm", "data/svmSpeechEmotion", False)

def GenrePicker(valence, arousal, people):
	print(valence, arousal, people)
	if people <= 3:
		if valence > 0.25:  #Very Happy
			if arousal > 0.25:  #very Excited
				return("Pop")
			elif arousal > -0.25: #neutral Exitement
				return("Hip-Hop")
			else:
				return ("Lofi Beats") #Low Energy
		elif valence > -0.25: #Neutral Happy
			if arousal > 0.25:
				return("Hip-Hop")
			elif arousal > -0.25:
				return ("Jazz")
			else:
				return("Classical")
		else:
			if arousal > 0.25: #Negative Happy
				return("Soft Rock")
			elif arousal > -0.25:
				return("Classical")
			else:
				return("Lofi Beats")
	elif people <= 6:
		if valence > 0.25:
			if arousal > 0.25:
				return("Dance")
			elif arousal > -0.25:
				return("Hip-Hop")
			else:
				return ("Soul")
		elif valence > -0.25:
			if arousal > 0.25:
				return("Hip-Hop")
			elif arousal > -0.25:
				return ("Jazz")
			else:
				return("Classical")
		else:
			if arousal > 0.25:
				return("Rock")
			elif arousal > -0.25:
				return("Country")
			else:
				return("Blues")
	else:
		if valence > 0.25:
			if arousal > 0.25:
				return("Electronic Dance Music")
			elif arousal > -0.25:
				return("Dance")
			else:
				return ("Hip-Hop")
		elif valence > -0.25:
			if arousal > 0.25:
				return("Hip-Hop")
			elif arousal > -0.25:
				return ("R&B")
			else:
				return("Soul")
		else:
			if arousal > 0.25:
				return("Hard Rock")
			elif arousal > -0.25:
				return("Country")
			else:
				return("Jazz")

access_key = "AKIA6OD36MM4U2WBKOVQ"
access_secret = "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"
region ="us-east-2"
queue_url = "https://sqs.us-east-2.amazonaws.com/992397386553/READ_THE_ROOM"

def pop_message(client, url):
    response = client.receive_message(QueueUrl = url, MaxNumberOfMessages = 10)

    #last message posted becomes messages
    message = response['Messages'][0]['Body']
    receipt = response['Messages'][0]['ReceiptHandle']
    client.delete_message(QueueUrl = url, ReceiptHandle = receipt)
    return message

def post_message(client, message_body, url):
	response = client.send_message(QueueUrl = url, MessageBody= message_body)
    
    
client = boto3.client('sqs', aws_access_key_id = access_key, aws_secret_access_key = access_secret, region_name = region)

waittime = 20
client.set_queue_attributes(QueueUrl = queue_url, Attributes = {'ReceiveMessageWaitTimeSeconds': str(waittime)})

time_start = time.process_time()
while (time.process_time() - time_start < 60):
        print("Checking...")
        try:
                message = pop_message(client, queue_url)
                print(message)
                if message == "Listening":
                	myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1) #num channels             
                	sd.wait()  # Wait until recording is finished
                	write('output.wav', fs, myrecording)  # Save as WAV file 
                	mood = aT.file_regression("output.wav", ["data/svmSpeechEmotion_valence", "data/svmSpeechEmotion_valenceMEANS", "data/svmSpeechEmotion_arousal", "data/svmSpeechEmotion_arousalMEANS"], "svm")
                	people = audioSegmentation.speaker_diarization("output.wav", 0, mid_window=2.0, mid_step=0.2, short_window=0.05, lda_dim=35, plot_res=False)
                	result = GenrePicker(mood[0][0], mood[0][1], people)
                	print(result)
                elif message == "Responding":
                	print(result)
                	post_message(client, result, queue_url)
        except:
                pass
