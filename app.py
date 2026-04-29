import gradio as gr
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

def chat_with_grok(user_message, history):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    messages = []

    messages.append({
        "role": "system",
        "content": "You are a helpful assistant only for education. If you get any questions related to education then repond with the best answer. If you get any questions related to other topics then respond with 'I am sorry, I am only designed to assist with educational questions.'"
    })


    print("Chat history:", history)

    for h in history:
        role = h["role"]
        text = h["content"][0]["text"]

        messages.append({
            "role": role,
            "content": text
        })

    messages.append({"role": "user", "content": user_message})

    data = {
        "model": "openai/gpt-oss-120b",
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    # print("API Response:", result)  # Debugging line to check the API response

    if "choices" in result:
        return result['choices'][0]['message']['content']
    else:
        return f"Error from API: {result}"

    # return result['choices'][0]['message']['content']

with gr.ChatInterface(chat_with_grok) as demo:
    demo.launch()