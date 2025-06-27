import string
import json
import requests
import pandas as pd

def load_json_from_url(url):
    """Fetch JSON data from a given URL"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

# The extraction logic
def extract_recipes():
    """Extract recipes from TheMealDB API and return as list of dictionaries"""
    all_recipes = []
    
    for letter in string.ascii_lowercase:
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?f={letter}"
        data = load_json_from_url(url)
        if data and data.get('meals') is not None:
            all_recipes.extend(data['meals'])
    
    return all_recipes  # Return the raw recipe data

# Existing execution code
if __name__ == "__main__":
    all_recipes = extract_recipes()  
    
    # JSON to dataframe
    uncleaned_df = pd.DataFrame(all_recipes)
    
    # Error handling & success validation
    try:
        uncleaned_df = pd.DataFrame(all_recipes)
        if len(uncleaned_df) > 0:
            print(f"✅ {len(uncleaned_df)} recipes extracted successfully!")
        else:
            print("⚠️ No recipes were extracted - check API connection")
    except Exception as e:
        print(f"❌ Error during extraction: {str(e)}")
