import requests
from urllib.parse import quote_plus

def get_movie_details(title, api_key):
    try:
        encoded_title = quote_plus(title)
        url = f"http://www.omdbapi.com/?t={encoded_title}&plot=full&apikey={api_key}"
        res = requests.get(url, timeout=10).json()

        # ✅ DEBUG: Print raw API response
        print(f"OMDB request for '{title}' → Response: {res}")

        if res.get("Response") == "True":
            plot = res.get("Plot", "N/A")
            poster = res.get("Poster", "N/A")
            return plot, poster
        else:
            print(f"OMDb API Error for '{title}': {res.get('Error')}")
            return "N/A", "N/A"
    except Exception as e:
        print(f"Exception during OMDB fetch for '{title}': {e}")
        return "N/A", "N/A"