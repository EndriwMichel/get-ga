"""
Main file to execute the program, but, what exatcly this program execute ?
- Read urls from json pre-configured with GDS (Google Data Studio) 
- Generate a GA token
- Make a request with the urls list
- Return a object with the information and extract de same value of GDS report
- Open a connection with SQL Server
- Insert the information into SQL Server "Datawarehouse"
"""

import os
import json
import requests
from src.insert_ga import Connect
from src.logger_ga import writeLog
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
load_dotenv()

# ----- Declare de env variables ----- 
# ----- Env variables to access Analytics Api and jsonFile -----

SCOPE = os.environ.get("SCOPE")
KEY_FILEPATH = os.environ.get("JSON_FILE_KEY")
URLS = os.environ.get("URLS")
PROC_INSERT_GA = os.environ.get("PROC_INSERT_GA")


def get_access_token(scope = SCOPE, key_filepath = KEY_FILEPATH):
    try:
        return ServiceAccountCredentials.from_json_keyfile_name(
        key_filepath, scope).get_access_token().access_token
    except Exception as e:
        writeLog(e).write_log()

def get_urls_from_file(file_path = URLS):
    try:
        with open(file_path) as json_urls:
            urls = json.load(json_urls)
            urls['urls']
            return urls

    except Exception as e:
        writeLog(e).write_log()

    finally:
        json_urls.close()

def make_request_ga(urls, token):
        request_result = None

        try:  
            for name in urls['urls']:
                for key, url in urls['urls'][name].items():
                    request_result = requests.get(url + token)
                    result_json = request_result.json()
                    urls['urls'][name][key] = result_json['rows'][0][0]            

            return urls

        except Exception as e:
            writeLog(e).write_log()


def main():
    token = get_access_token()
    url_list = get_urls_from_file()

    object_from_request = make_request_ga(url_list, token)
    
    Connect().executeProc(PROC_INSERT_GA, object_from_request)

if __name__ == "__main__":
    main()
