# https://developers.google.com/sheets/api/quickstart/python
# sudo pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# sudo pip3 install gsheets
# Create project, add drive API, and add sheets API
# set up permissions as "Editor"
# Add "yourself" as a user of the api while it is in test mode
# Go to https://console.cloud.google.com/apis/credentials?project=raspibackboiler
# Under the OAuth2 client ID's and download the "client ID", not the service-account object you made.
# drop the client_secret.json file into this folder, run the app and authorize it first time
# do not check the json or the token into git!

import pygsheets
import numpy as np


MAX_SHEET_ROWS = 1000
INCREMENT_SHEET_ROWS = 200
WORKSHEET_NAME = 'Raspi-backboiler'


def is_heading(line):
    return line.split(',') and line.split(',')[0].lower() == 'time'


def main():
    """
    Simple program to copy the data in a CSV file into a google cloud document.
    Example to solve the issues of pushing data into a more persistent store
    somehow.
    :return:
    """
    gc = pygsheets.authorize()

    # Open spreadsheet and then worksheet
    try:
        sh = gc.open(WORKSHEET_NAME)
    except Exception as e:
        print(e)
        sh = gc.create(WORKSHEET_NAME)
    wks = sh.sheet1
    # todo: append sheets to instead of creating a new document
    #       make this add 1 new tab/sheet for each day of the month by numbering the sheets

    with open('../sensors.csv') as f:
        headings = False
        # find, and write the CSV header first
        while not headings:
            l = f.readline().rstrip()
            if is_heading(l):
                print("headings:")
                print(l)
                wks.update_values('A1', [l.split(',')])
                headings = True
        l = f.readline().rstrip()
        row = 2  # excell cell numbers
        update = []
        while len(l.split(',')[0]):
            if not is_heading(l):
                update.append(l.split(','))
            l = f.readline().rstrip()
            if len(update) > INCREMENT_SHEET_ROWS:
                range = f"A{row}"
                print(f"DATA({row}): {l}...")
                if INCREMENT_SHEET_ROWS + row >= MAX_SHEET_ROWS:
                    print(f"grow to {INCREMENT_SHEET_ROWS + row}")
                    wks.resize(rows=INCREMENT_SHEET_ROWS + row)
                wks.update_values(range, update)
                row += len(update)
                update = []
        # final rows
        if len(update):
            range = f"A{row}"
            print(f"DATA({row}): {l}")
            if INCREMENT_SHEET_ROWS + row >= MAX_SHEET_ROWS:
                print(f"grow to {INCREMENT_SHEET_ROWS + row}")
                wks.resize(rows=INCREMENT_SHEET_ROWS + row)
            wks.update_values(range, update)

if __name__ == '__main__':
    main()
