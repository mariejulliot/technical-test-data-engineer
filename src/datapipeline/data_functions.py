import requests
import pandas as pd
from IPython.display import display
from datetime import date
import os

# Call the api
def call_api(api_url, route) :
    print("Get " + route)
    try:
        response = requests.get(api_url + route)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve data " + route + ":" + str(e))
    except Exception as e:
        print("Unexpected error while fetching from " + route + ":" + str(e))


# Transform the api response to a dataFrame
def transform_to_df(data) :
    df = pd.DataFrame(data)
    if isinstance(data, dict) and bool(data):
        df = pd.DataFrame(data["items"])
    else :
        print("Datas cannot be parsed or are empty")
    return df

# SHOULD HAVE BEEN DONE IN A REAL CASE
# SAVE DATAFRAME INTO THE DATABASE USING THE TABLE NAME
def save_to_database(df, table_name, path) :
    # add today's date to datas, can be used to partition
    today = date.today()
    dates = str(today).split("-")
    df["year"] = dates[0]
    df["month"] = dates[1]
    df["day"] = dates[2]
    # We save it as a file instead
    if not df.empty :
        file_path = path + table_name + '.csv'
        # if the file already exists
        if os.path.exists(file_path) :
            # we save it in append mode with no header
            df.to_csv(file_path, mode='a', header=False, index=False)
        else :
            df.to_csv(file_path, index=False)

# Used for testing purpose
def display_df(df):
    with pd.option_context('display.max_columns', None):
        display(df)