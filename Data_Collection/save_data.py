import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import datetime


def write_data(time='NA', tweets='NA', uv='NA', cc='NA'):

    file_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(file_dir, 'data_new.csv')

    df = pd.read_csv(data_path, index_col='DateTime', parse_dates=['DateTime'])
    df2 = pd.DataFrame({'MentalHealthTweets': tweets, 'UV': uv, 'CloudCover': cc}, index=[time],
                       columns=['MentalHealthTweets', 'UV', 'CloudCover'])
    df = df.append(df2, ignore_index=False)
    df.index.names = ['DateTime']
    df.to_csv(data_path)


def backup_data(time='NA'):

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    file_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(file_dir, 'data_new.csv')

    df = pd.read_csv(data_path, index_col='DateTime', parse_dates=['DateTime'])

    time = time.replace(':', '-')
    filename = 'data_' + time.replace(' ', '_') + '.csv'

    file1 = drive.CreateFile({'title': filename, 'mimeType': 'text/csv',
                              "parents": [{"kind": "drive#fileLink", "id": '1Jhm8v0F9sI6xPon3NCtqfEzwyBrDfW5_'}]})
    file1.SetContentString(df.to_csv())
    file1.Upload()


def save_error():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    file1 = drive.CreateFile({'title': '420 Error', 'mimeType': 'text/csv',
                              "parents": [{"kind": "drive#fileLink", "id": '1w0v6wKYIQg18iF8TT3vm_7WXvH13kxGY'}]})
    file1.SetContentString('420 error raised - rate limit exceeded at ' + str(datetime.datetime.now()))
    file1.Upload()

