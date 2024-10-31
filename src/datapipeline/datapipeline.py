import schedule
import time
from data_functions import call_api, transform_to_df, display_df, save_to_database

# Fetch all different datas using data_functions functions
def fetch_data() :
    routes = ["users", "tracks", "listen_history"]
    api_url = "http://127.0.0.1:8000/"
    for route in routes :
        data = call_api(api_url, route)
        df = transform_to_df(data)
        display_df(df) # testing purpose
        save_to_database(df, route, '../../results/')

# Schedule to fetch the datas every day at 2am for example
#schedule.every().day.at("02:00").do(fetch_data)
# used for testing purpose only
schedule.every(1).minutes.do(fetch_data)

# Looping to keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)  # Attendre une minute avant de vérifier à nouveau




