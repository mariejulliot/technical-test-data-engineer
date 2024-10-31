from src.datapipeline.data_functions import call_api, transform_to_df, save_to_database
import pandas as pd
import os

api_url = "http://127.0.0.1:8000/"

########################################################
#                    Test call_api                     #
########################################################
# Testing call_api for tracks
def test_call_api_for_tracks():
    res = call_api(api_url, "tracks")
    assert isinstance(res, dict)

# Testing call_api for users
def test_call_api_for_users():
    res = call_api(api_url, "users")
    assert isinstance(res, dict)

# Testing call_api for listen_history
def test_call_api_for_listen_history():
    res = call_api(api_url, "listen_history")
    assert isinstance(res, dict)

# Testing call_api for a bad request
def test_call_api_for_bad_request():
    res = call_api(api_url, "test")
    assert not isinstance(res, dict)

########################################################
#                Test transform_to_df                  #
########################################################
#Testing transform to df for tracks
def test_transform_to_df_for_tracks():
    data = call_api(api_url, "tracks")
    res = transform_to_df(data)
    assert isinstance(res, pd.DataFrame)
    expected_names = ['id', 'name', 'artist', 'songwriters', 'duration', 'genres', 'album', 'created_at', 'updated_at']
    column_names = res.columns.tolist()
    assert column_names == expected_names

#Testing transform to df for users
def test_transform_to_df_for_users():
    data = call_api(api_url, "users")
    res = transform_to_df(data)
    assert isinstance(res, pd.DataFrame)
    expected_names = ['id', 'first_name', 'last_name', 'email', 'gender', 'favorite_genres', 'created_at', 'updated_at']
    column_names = res.columns.tolist()
    assert column_names == expected_names

#Testing transform to df for listen_history
def test_transform_to_df_for_listen_history():
    data = call_api(api_url, "listen_history")
    res = transform_to_df(data)
    assert isinstance(res, pd.DataFrame)
    expected_names = ['user_id', 'items', 'created_at', 'updated_at']
    column_names = res.columns.tolist()
    assert column_names == expected_names

#Testing transform to df for bad request
def test_transform_to_df_for_bad_request():
    data = call_api(api_url, "test")
    res = transform_to_df(data)
    assert isinstance(res, pd.DataFrame)
    expected_names = []
    column_names = res.columns.tolist()
    assert column_names == expected_names

########################################################
#                Test save_to_database                 #
########################################################
#Testing save to database for listen_history
def test_save_to_database_for_listen_history():
    data = call_api(api_url, "listen_history")
    df = transform_to_df(data)
    path = '../results_test/'
    file_path = path + "listen_history.csv"
    if os.path.exists(file_path):
        os.remove(file_path)
    save_to_database(df, "listen_history", path)
    # Check that the file has been created again
    assert os.path.exists(file_path), f"Le fichier {file_path} n'existe pas."

#Testing save to database for a bad request
def test_save_to_database_for_bad_request():
    data = call_api(api_url, "test")
    df = transform_to_df(data)
    path = '../results_test/'
    file_path = path + "test.csv"
    if os.path.exists(file_path):
        os.remove(file_path)
    save_to_database(df, "test", path)
    # Check that the file has not been created
    assert not os.path.exists(file_path), f"Le fichier {file_path} n'existe pas."
