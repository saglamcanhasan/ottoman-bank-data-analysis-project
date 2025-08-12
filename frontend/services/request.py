import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("URL_BACKEND")
port = int(os.getenv("PORT_BACKEND"))

def request(figure_id: str, **filter_parameters):
    print(figure_id, filter_parameters)
    response = requests.post(f"http://{url}:{port}/api/{figure_id}", json=filter_parameters)

    # return data if the request was successful
    if response.status_code == 200:
        response = response.json()
        if response["type"] == "dataframe":
            return pd.DataFrame(response["data"])
        return response["data"]
    else:
        print(response.json())