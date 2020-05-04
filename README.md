# Read-the-Room
CPSC 490 JORDAN SMITH README

Requirements For Recreating My Work:
Amazon Developer Account
Amazon Web Service Account
Amazon Alexa Device
Laptop with Built-in MicroPhone

In order to run the system one must have set up the neccessary queue and run ReadtheRoom.py this will put the program in a loop that checks the queue for messages. Only then can you talk to alexa and recieve the expected responses.

Required Libraries:
pyAudioAnalysis -- It's important to substitute the AudioSegmentation.py file in pyaudioanalysis package with the version of the file I provided
-- It is also important to substitue midtermfeatures.py file because the time.time() functionality is outdated and I revised it
-- It is also important to specify the specific path to the training data correctly
Boto3
csv
glob
scipy
sklearn
numpy as np
hmmlearn
pickle
matplotlib
Sounddevice
Time
SimpleJSON
EyeD3
Pydub

documentation for pyAudioAnalysis can be found here: https://github.com/tyiannak/pyAudioAnalysis

Helpful for understanding AWS queue and Amazon Alexa Skill: http://www.cyber-omelette.com/2017/01/alexa-run-script.html

Note about Lambda_function.py and queue functionality:
This file is supposed to go where the AWS queue asks for function code.

Also the values for access_key, access_secret, region, and queue_url will all be different depending on the users own AWS queue creation

Creating the Alexa skill is straightforward, the most confusing part is specifying the queue as an endpoint, this can be done by finding the ARN adress within the AWS queue and specifying that adress inside of the new alexa skill.

Link to Demonstration Video: https://www.youtube.com/watch?v=CcCuK_IoyuQ





