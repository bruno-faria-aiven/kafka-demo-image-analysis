import streamlit as st
from kafka import KafkaProducer
from PIL import Image
import io
from dashboards import dashboard
import config

HOST = config.KAFKA_HOST
SSL_PORT = config.KAFKA_SSL_PORT
certs_path = config.KAFKA_CERTS_PATH

producer = KafkaProducer(
    bootstrap_servers=f"{HOST}:{SSL_PORT}",
    security_protocol="SSL",
    ssl_cafile=f"{certs_path}/ca.pem",
    ssl_certfile=f"{certs_path}/service.cert",
    ssl_keyfile=f"{certs_path}/service.key"
)

# Kafka topic
topic = 'image-topic'

# Streamlit UI setup
dashboard("producer")
# st.title("Kafka Image Producer")
st.write("Click the 'Browse files' button to select images you wish to analyze. Once selected, click the 'Produce to "
         "Kafka' button to produce them to a Kafka topic.")

st.info("Note: You can select multiple images at a time and also produce all images at once.")

# Upload multiple images through Streamlit
uploaded_files = st.file_uploader("Choose images:", type=["jpg", "jpeg", "png"], accept_multiple_files=True)


if uploaded_files:
    for uploaded_file in uploaded_files:
        # Display each uploaded image
        img = Image.open(uploaded_file)
        st.image(img, caption=f'Uploaded Image: {uploaded_file.name}', width=350)


        # Convert image to bytes
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='JPEG')
        img_bytes = img_byte_array.getvalue()

        # Kafka production
        if st.button(f"Produce {uploaded_file.name} to Kafka"):
            producer.send(topic, value=img_bytes)
            producer.flush()
            st.success(f"Image {uploaded_file.name} produced to Kafka successfully!")

        st.divider()

# Optional: Produce all images at once
if uploaded_files and st.button("Produce All Images to Kafka"):
    for uploaded_file in uploaded_files:
        img = Image.open(uploaded_file)
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='JPEG')
        img_bytes = img_byte_array.getvalue()
        producer.send(topic, value=img_bytes)
    producer.flush()
    st.success("All images produced to Kafka successfully!")