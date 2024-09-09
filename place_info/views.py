
from django.shortcuts import render
from django.http import JsonResponse
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests
from openai import OpenAI
import openai
client = OpenAI(api_key = 'your openai key')



def index(request):
    return render(request, 'place_info/index.html')
import wikipedia

def get_wikipedia_info(place_name):
    try:
        # Search for the place name on Wikipedia
        search_results = wikipedia.search(place_name)

        if not search_results:
            return "Wikipedia page not found for the provided place."

        # Use the first search result to get the page summary
        page_title = search_results[0]

        # Fetch the summary for the first relevant result
        summary = wikipedia.summary(page_title, sentences=5)

        return summary

    except wikipedia.exceptions.DisambiguationError as e:
        # Handle disambiguation errors (multiple results for the same name)
        return f"Multiple pages found for '{place_name}': {e.options}"

    except wikipedia.exceptions.PageError:
        # Handle page not found error
        return "Wikipedia page not found for the provided place."

    except Exception as e:
        # General exception handling
        print(f"Error fetching Wikipedia information: {e}")
        return "An error occurred while fetching Wikipedia information."


def get_location_info(request):
    place_name = request.GET.get('place_name')

    # Fetch information from Wikipedia
    wikipedia_summary = get_wikipedia_info(place_name)

    # Call the AI model to summarize if needed
    ai_summary = get_ai_summary(wikipedia_summary)

    # Prepare the response
    response = {
        'place_name': place_name,
        'summary': ai_summary if ai_summary else wikipedia_summary
    }

    return JsonResponse(response)



def get_ai_summary(summary):
    # Prepare the messages for the chat model
    messages = [
       {"role": "system", "content": "You are a knowledgeable historian and tour guide who provides engaging, concise, and easy-to-understand summaries of historical information. Your summaries should be suitable for a general audience, including tourists and history enthusiasts, and should highlight key events, important figures, cultural significance, and interesting facts. Aim to make the history come alive and spark curiosity."},

{"role": "user", "content": f"Please summarize the following historical information in a way that is informative, captivating, and accessible to a wide audience. Focus on the main events, notable personalities, and any unique or lesser-known facts that would be intriguing to someone visiting this location. Use a friendly and approachable tone:\n\n{summary}"}

    ]

    try:
        # Call the OpenAI API for chat completion
        ai_response = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-4.0" if using gpt-4o model
            messages=messages,
            max_tokens=1000
        )

        # Extract the assistant's response from the completion
        ai_summary = ai_response.choices[0].message.content
        return ai_summary

    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return "An error occurred while generating the summary."

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import UserProfile

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'place_info/register.html', {'form': form})
# Define the index view
def index(request):
    return render(request, 'place_info/index.html')

def login_view(request):
    return render(request, 'login.html')