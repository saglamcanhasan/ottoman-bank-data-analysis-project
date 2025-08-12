import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("URL_BACKEND")
port = int(os.getenv("PORT_BACKEND"))

def request(figure_id: str, **filter_parameters):
    server_url = f"http://{url}:{port}/api/{figure_id}"

    try:
        if figure_id == "filter-parameters":
            response = requests.get(server_url)
        else:
            response = requests.post(server_url, json=filter_parameters)

        # return data if the request was successful
        if response.status_code == 200:
                
            response = response.json()
            if isinstance(response["type"], list):
                return list(pd.DataFrame(data) if type == "dataframe" else data for type, data in zip(response["type"], response["data"]))
            elif response["type"] == "dataframe":
                return pd.DataFrame(response["data"])
            return response["data"]
        
        # return error message if the request failed
        elif response.status_code == 404:
            return response.json().get("error", "API not found")
        
        else:
            return None
        
    except Exception as exception:
        return None