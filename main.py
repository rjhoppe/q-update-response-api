from __future__ import print_function
import requests
import asyncio
import aiohttp
import os
import sys
import time

# Import all necessary google api libraries
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Create API user class
class ApiUser:
    def __init__(self, username, api_token, data_center, survey_id, brand_name):
        self.username = username
        self.api_token = api_token
        self.data_center = data_center
        self.survey_id = survey_id
        self.brand_name = brand_name

# Replace user class placeholder values
User = ApiUser("user", "api_token", "data_center", "survey_id", "brand_name")

# Survey connection and schema check
def get_sample_response():

    try:    
        # Replace with a survey response id from the production project
        sample_response_id = "R_xxxxxxxxxxx"

        url = f"https://{User.data_center}.qualtrics.com/API/v3/surveys/{User.survey_id}/responses/{sample_response_id}"

        headers = {
            "Content-Type": "application/json",
            "X-API-TOKEN": f"{User.api_token}"
        }

        response = requests.request("GET", url, headers=headers)

        print(response.status_code)
        print(response.text)
    
    # Exception to end program if http error encountered
    except HttpError:
        print(HttpError)
        sys.exit()
    
    # User inputs "Y" to validate that sample response and associated schema looks correct - can be removed
    print("Does this data look correct to you? Y/N")
    check1 = input()
    if check1.upper() != "Y":
        print("Exiting program")
        sys.exit() 

get_sample_response()

# Pulled from Google Python quickstart.py file
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Output of this function will be the response_data dict
def sheets_scrap() -> dict:

    response_data = {}
    creds = None
    # quickstart.py notes: The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    #quickstart.py notes: If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    # Row value
    index = 2
    # Need to count the number of Google Sheet APIs in a row - Google throttles requests at 60 per user account
    g_api_count = 0
    # Update below depending on length of spreadsheet, 1000 is the placeholder value for number of rows
    while index < 1000:
        
        try:
            # Pulled from the quickstart.py file
            SAMPLE_SPREADSHEET_ID = 'google_spreadsheet_id'
            SAMPLE_RANGE_NAME = f'Sheet1!A{index}:B{index}'
            
            service = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME).execute()
            values = result.get('values', [])

            # Adds row values as a key-value dictionary pair to the response_data dict 
            for row in values:
                print('%s, %s' % (row[0], row[1]))
                response_data.update({row[0]: row[1]})

            if not values:
                print('No data found.')
                return

        except HttpError as err:
            print(err)

        index += 1
        g_api_count += 1
        
        # This manually stops the program and waits for 60 seconds, so the API minute limit of 60 per minute refreshes
        # After 60 seconds, the API count is set back to 0
        if g_api_count > 59:
            print("Refreshing Google API count...")
            time.sleep(60)
            print("Number of response collected:")
            print(len(response_data))
            g_api_count = 0

    # System outputs the response_data and awaits user validation
    print(response_data)
    print("Does this data look correct to you? Y/N")
    check2 = input()
    if check2.upper() != "Y":
        print("Exiting program")
        sys.exit()       
    return response_data

response_data = sheets_scrap()

# Update Response Qualtrics API
# This function iterates through the response ids and plugs in any associated embedded values 
# that you would like updated on the individual response and passes those into the request 
async def update_dates(response_data):
    async_count = 0
    print(response_data.keys())
    headers = {
        "Content-Type": "application/json",
        "X-API-TOKEN": f"{User.api_token}"
    }

    print(response_data.keys())

    timeout = aiohttp.ClientTimeout(total=500)
    async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
        for key, value in response_data.items():
            url = f"https://{User.data_center}.qualtrics.com/API/v3/responses/{key}"
            payload = {
                "surveyId": f"{User.survey_id}",
                "resetRecordedDate": False,
                "embeddedData": {
                    "CourseEndDate": f"{value}"
                    # Add any additional embedded data values here
                }
            }
            async with session.put(url, json=payload) as resp:
                async_count +=1
                # This will print the response status code for each request - can be removed
                print(resp.status)
            if async_count > 2500:
                print("Refreshing Q API count...")
                time.sleep(60)
                async_count = 0
    
        print("Job Done")

asyncio.run(update_dates(response_data))




