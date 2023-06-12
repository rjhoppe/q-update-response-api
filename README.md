# Qualtrics Update Response API Using Data from Google Sheets

## Table of contents
* [Introduction](#introduction)
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## Introduction

This Python script was built to pull embedded data values associated with a individual Qualtrics survey response from a
user owned Google Sheet and then feed it into the Qualtrics Update Survey Response public API. The use case for this would 
be a need to perform a mass embedded data update to a large number of survey responses where the embedded data values were either not stored with the original response or it was stored incorrectly.

## General info
This project is simple Lorem ipsum dolor generator.
	
## Technologies
Project is created with:
* Qualtrics platform
* Qualtrics public APIs
* Google Sheet API
* asyncio, requests, aiohttp Python libraries
	
## Setup
To run this program, setup a local virtual environment and install the required dependencies byu running this command:

$ pip install -r requirements.txt

After installing the required dependencies, create / login to a Google Cloud account. Once you have logged in to your account
create a new project for this program and create a new OAuth token with the necessary Google Sheets permissions (requires read and write permissions) 

The first 10 minutes of this video shows you how to do that: https://www.youtube.com/watch?v=3wC-SCdJK2c&t=1232s

After you have generated your OAuth credentials you should have a "credentials.json" file. Place this file in the program directory.

Now, proceed to run the quickstart.py file provided by this Google Developers page: https://developers.google.com/drive/api/quickstart/python

After running the quickstart.py file in your local directory, you should now have a "token.json" file. This gives your program the permissions required to run this script. 

You may now proceed to configuring the main.py file for your use case. Replace all the placeholder values in the ApiUser class as well as all of the placeholder values in the sheets_scrap function. You will need a Qualtrics API user token of your own in order to run this program.

Throughout this program, there are a number of print statements that serve as guardrails to ensure the data being processed is correct. You can delete these if you like or keep them as is. 