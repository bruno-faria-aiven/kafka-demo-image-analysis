import streamlit as st
from kafka import KafkaConsumer
from PIL import Image
import io
import base64
import requests
import json
import time
from dashboards import dashboard
import config

HOST = config.KAFKA_HOST
SSL_PORT = config.KAFKA_SSL_PORT
certs_path = config.KAFKA_CERTS_PATH

consumer = KafkaConsumer(
    'image-topic',
    auto_offset_reset="latest",
    bootstrap_servers=f"{HOST}:{SSL_PORT}",
    enable_auto_commit=False,
    security_protocol="SSL",
    ssl_cafile=f"{certs_path}/ca.pem",
    ssl_certfile=f"{certs_path}/service.cert",
    ssl_keyfile=f"{certs_path}/service.key",
)

# OpenAI API Configuration
api_url = "https://api.openai.com/v1/chat/completions"
api_key = config.OPENAI_KEY
headers = {
    "Authorization": f"Bearer {api_key}",  # Replace with your OpenAI API key
    "Content-Type": "application/json"
}

# Function to analyze images with OpenAI
def analyze_image(image_bytes):
    # Encode image in Base64
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe the characteristics of this image (ex: is it a person, what are they wearing, etc)"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    }
                ]
            }
        ]
    }

    # Send the request to OpenAI
    res = requests.post(api_url, headers=headers, data=json.dumps(payload))

    # Return the response content
    return res.json()

# Streamlit UI setup
dashboard("consumer")

# Initialize session state variables for controlling the loop
if 'consuming' not in st.session_state:
    st.session_state.consuming = False

# Start or stop consuming images
if st.button('Start Consuming Images'):
    st.session_state.consuming = True

if st.button('Stop Consuming Images'):
    st.session_state.consuming = False

# Kafka consumer loop in Streamlit
while st.session_state.consuming:
    st.write("Consuming images from Kafka: ")

    for message in consumer:
        img_bytes = message.value
        response = analyze_image(img_bytes)
        # print("OpenAI Image Analysis Response:", response)

        # Display the image
        img = Image.open(io.BytesIO(img_bytes))
        st.image(img, caption='Consumed Image from Kafka', width=350)

        # Display the analysis result
        if 'choices' in response:
            description = response['choices'][0]['message']['content']
            st.write(f"Image Description: {description}")
            st.divider()
        else:
            st.write("Failed to get description from OpenAI API.")

        # Break if consuming is stopped
        if not st.session_state.consuming:
            break

        # Sleep for a short duration to prevent overwhelming the server
        time.sleep(1)

    # End loop if stopped
    if not st.session_state.consuming:
        break
