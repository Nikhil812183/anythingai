import os
import requests
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Setup voice engine
engine = pyttsx3.init()

# API constants
API_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}
MODEL = "llama3-70b-8192"

# Voice input function
def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."
    except sr.RequestError as e:
        return f"Error with Google Speech API: {e}"

# Chatbot response
def chat_with_bot(user_input):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful chatbot."},
            {"role": "user", "content": user_input}
        ]
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        return reply
    else:
        return f"Error: {response.status_code} - {response.text}"

# Speak output
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Main loop
if __name__ == "__main__":
    print("🤖 Voice Chatbot is ready! Say 'exit' to stop.")
    while True:
        user_input = get_voice_input()
        if "exit" in user_input.lower():
            break
        response = chat_with_bot(user_input)
        print("Bot:", response)
        speak(response)

