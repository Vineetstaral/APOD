import streamlit as st
from llama_index.llms.groq import Groq
from dotenv import load_dotenv
import os
import requests

# Load the environment variables from .env file
load_dotenv()

# Fetch the API key from the environment variable
api_key = os.getenv("GROQ_API_KEY")

# Initialize the Groq model
llm = Groq(model="llama3-70b-8192", api_key=api_key)

# NASA APOD API endpoint
NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"

def get_apod():
    """
    Fetch the Astronomy Picture of the Day (APOD) from NASA API.
    """
    try:
        params = {
            "api_key": "DEMO_KEY"  # Use NASA's demo key (no API key required)
        }
        response = requests.get(NASA_APOD_URL, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        apod_data = response.json()
        return {
            "title": apod_data["title"],
            "explanation": apod_data["explanation"],
            "url": apod_data["url"]
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"NASA API error: {e}"}
    except KeyError:
        return {"error": "Invalid response from NASA API"}

# Streamlit app
st.title("🌌 NASA Astronomy Picture of the Day 🚀")

if st.button("Fetch APOD"):
    apod = get_apod()
    if "error" in apod:
        st.error(apod["error"])
    else:
        st.write(f"### {apod['title']}")
        st.image(apod["url"], caption=apod["title"])
        st.write(apod["explanation"])

# Add a footer
st.markdown("---")
st.markdown("Made by [Your Name]")
