import os
import json
from langchain_tavily import TavilySearch
from langchain_google_community import GooglePlacesTool, GooglePlacesAPIWrapper 
import requests
import os

class GeoapifyPlaceSearchTool:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEOAPIFY_API_KEY")
        self.base_url = "https://api.geoapify.com/v2/places"

    def _search(self, place, category):
        url = f"https://api.geoapify.com/v2/places"
        params = {
            "categories": category,
            "filter": f"place:{place}",
            "bias": f"proximity:0,0",  # fallback if location not geocoded
            "limit": 5,
            "apiKey": self.api_key
        }

        # Geoapify requires lat/lng — so you might need geocoding first.
        # Here's a helper for geocoding:
        lat, lon = self._geocode_place(place)
        if lat and lon:
            params["bias"] = f"proximity:{lon},{lat}"

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return [f"{item['properties']['name']} ({item['properties']['categories'][0]})"
                    for item in data.get("features", [])]
        else:
            return f"Error fetching data from Geoapify: {response.text}"

    def _geocode_place(self, place_name):
        url = "https://api.geoapify.com/v1/geocode/search"
        params = {
            "text": place_name,
            "limit": 1,
            "apiKey": self.api_key
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            results = response.json().get("features", [])
            if results:
                coords = results[0]["geometry"]["coordinates"]
                return coords[1], coords[0]  # lat, lon
        return None, None

    def search_attractions(self, place):
        return self._search(place, "tourism.sights")

    def search_restaurants(self, place):
        return self._search(place, "catering.restaurant")

    def search_transportation(self, place):
        return self._search(place, "transport.public")

    def search_activity(self, place):
        return self._search(place, "entertainment")  # or other category


# class GooglePlaceSearchTool:
#     def __init__(self, api_key: str):
#         self.places_wrapper = GooglePlacesAPIWrapper(gplaces_api_key=api_key)
#         self.places_tool = GooglePlacesTool(api_wrapper=self.places_wrapper)
    
#     def google_search_attractions(self, place: str) -> dict:
#         """
#         Searches for attractions in the specified place using GooglePlaces API.
#         """
#         return self.places_tool.run(f"top attractive places in and around {place}")
    
#     def google_search_restaurants(self, place: str) -> dict:
#         """
#         Searches for available restaurants in the specified place using GooglePlaces API.
#         """
#         return self.places_tool.run(f"what are the top 10 restaurants and eateries in and around {place}?")
    
#     def google_search_activity(self, place: str) -> dict:
#         """
#         Searches for popular activities in the specified place using GooglePlaces API.
#         """
#         return self.places_tool.run(f"Activities in and around {place}")

#     def google_search_transportation(self, place: str) -> dict:
#         """
#         Searches for available modes of transportation in the specified place using GooglePlaces API.
#         """
#         return self.places_tool.run(f"What are the different modes of transportations available in {place}")

class TavilyPlaceSearchTool:
    def __init__(self):
        pass

    def tavily_search_attractions(self, place: str) -> dict:
        """
        Searches for attractions in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"top attractive places in and around {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result
    
    def tavily_search_restaurants(self, place: str) -> dict:
        """
        Searches for available restaurants in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"what are the top 10 restaurants and eateries in and around {place}."})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result
    
    def tavily_search_activity(self, place: str) -> dict:
        """
        Searches for popular activities in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"activities in and around {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result

    def tavily_search_transportation(self, place: str) -> dict:
        """
        Searches for available modes of transportation in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"What are the different modes of transportations available in {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result
    