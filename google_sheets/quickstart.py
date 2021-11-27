from __future__ import print_function
#import os.path
from googleapiclient.discovery import build
#from google_auth_oauthlib.flow import InstalledAppFlow
#from google.auth.transport.requests import Request
#from google.oauth2.credentials import Credentials

from google.oauth2 import service_account

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# The ID and range of a sample spreadsheet.

SPREADSHEET_ID = '1VbtCJdf9368QqmLCDJKakyP-pYRlPD2KTZ-F4E7omFk'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'



service = build('sheets', 'v4', credentials=credentials)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                            range="Sheet1!a1:g13").execute()
values = result.get('values', [])
print(values)
anydata = [["1/1/2020", 4000],
           ["2/2/2020", 4000],
           ]
request = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                              range="Sheet1!a1",
                              valueInputOption="USER_ENTERED",
                              body={"values": anydata}
                              )
request.execute()