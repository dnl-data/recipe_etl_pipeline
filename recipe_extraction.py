import string
import json
import requests

import pandas as pd

def load_json_from_url(url):
    """Fetch JSON data from a given URL

    Args:
        url (str): The URL to fetch JSON data from. Must include protocol
                   (e.g., 'https://')

    Returns:
        dict/list/None: The parsed JSON data as Python objects (typically dict
                       or list) if successful. Returns None if any error occurs

    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

# Fetch recipes for each letter in the alphabet from the API

all_recipes = []

for letter in string.ascii_lowercase:
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?f={letter}"

    data = load_json_from_url(url)

    if data and data.get('meals') is not None:
        all_recipes.extend(data['meals'])


# JSON to dataframe

uncleaned_df = pd.DataFrame(all_recipes)

