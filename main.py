import streamlit as st
from llama_index.llms.groq import Groq
from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta

# Load the environment variables from .env file
load_dotenv()

# Fetch the API key from the environment variable
api_key = os.getenv("GROQ_API_KEY")

# Initialize the Groq model
llm = Groq(model="llama3-70b-8192", api_key=api_key)

# NASA APOD API endpoint
NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"

def get_apod(date=None):
    """
    Fetch the Astronomy Picture of the Day (APOD) from NASA API for a specific date.
    If no date is provided, fetch today's APOD.
    """
    try:
        params = {
            "api_key": "DEMO_KEY",  # Use NASA's demo key (no API key required)
            "date": date  # Optional: Fetch APOD for a specific date
        }
        response = requests.get(NASA_APOD_URL, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        apod_data = response.json()
        return {
            "title": apod_data["title"],
            "explanation": apod_data["explanation"],
            "url": apod_data["url"],
            "date": apod_data["date"]
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"NASA API error: {e}"}
    except KeyError:
        return {"error": "Invalid response from NASA API"}

# Streamlit app
st.title("🌌 NASA Astronomy Picture of the Day 🚀")

# Date picker in the main interface
selected_date = st.date_input(
    "Select a date",
    value=datetime.today(),  # Default to today's date
    max_value=datetime.today(),  # Cannot select future dates
    min_value=datetime(1995, 6, 16)  # APOD started on June 16, 1995
)

# Fetch APOD for the selected date
if st.button("Fetch APOD"):
    apod = get_apod(selected_date.strftime("%Y-%m-%d"))  # Convert date to string format
    if "error" in apod:
        st.error(apod["error"])
    else:
        st.write(f"### {apod['title']} ({apod['date']})")
        st.image(apod["url"], caption=apod["title"])
        st.write(apod["explanation"])

# Add a footer
st.markdown("---")
st.markdown("AI can make mistakes.")
