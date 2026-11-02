import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def generate_event_description(
    title: str,
    category: str,
    audience: str,
    location: str,
    event_date: str
):
    prompt = f"""
    Create a professional and engaging event description.

    Event Title: {title}
    Category: {category}
    Target Audience: {audience}
    Event Location: {location}
    Event Date: {event_date}

    Keep the description concise and suitable for an event management platform.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )
        return response.text
    except Exception as e:
        print("Gemini API Error:", e)
        return None