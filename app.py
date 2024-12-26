import os
import requests
import streamlit as st
import pycurl
from io import BytesIO
import json

# Set up Streamlit app page
st.set_page_config(page_title="AI Submission Insights", page_icon="📊")
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyBue4xizhbGN-j_FYUGPuUYGk1pLPyCa8U"

# Upload Folder Setup
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf'}

# Placeholder for Gemini API key and endpoint (replace with actual)

# Streamlit UI components
st.title("AI-Generated Submission Insights")
st.write("""
    Upload your submission file (in .txt or .pdf format) to get automated insights, feedback, and scores.
""")

# File uploader widget
uploaded_file = st.file_uploader("Choose a file to upload", type=["txt", "pdf"])

# Function to process file and interact with Gemini API
def process_file(file):
    # Save the uploaded file to the local folder
    file_path = os.path.join(UPLOAD_FOLDER, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())

    # Read the content of the file (assuming text-based files like txt or pdf)
    file_content = ""
    if file.name.endswith(".txt"):
        with open(file_path, 'r') as f:
            file_content = f.read()
    elif file.name.endswith(".pdf"):
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        file_content = "".join([page.extract_text() for page in reader.pages])

    # Call Gemini API to get insights (feedback, scoring, and summarization)
    response = get_insights_from_gemini(file_content)
    return response

def extract_text(data):
    if isinstance(data, str):
        data = json.loads(data)  # Parse JSON string if necessary
    text = ""
    candidates = data.get("candidates", [])
    for candidate in candidates:
        content = candidate.get("content", {})
        parts = content.get("parts", [])
        for part in parts:
            text += part.get("text", "") + "\n"
    return text
# Function to interact with Gemini API (for feedback, scoring, and summarization)
def get_insights_from_gemini(text):
    # Request payload
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": ""}
                ]
            }
        ]
    }
    payload["contents"][0]["parts"][0]["text"] = text

    # Convert payload to JSON string
    json_payload = json.dumps(payload)

    # Create a buffer to store the response
    response_buffer = BytesIO()

    # Initialize cURL
    curl = pycurl.Curl()

    # Set cURL options
    curl.setopt(curl.URL, url)  # API URL
    curl.setopt(curl.POST, 1)  # Set request method to POST
    curl.setopt(curl.POSTFIELDS, json_payload)  # JSON data
    curl.setopt(curl.HTTPHEADER, ['Content-Type: application/json'])  # Headers
    curl.setopt(curl.WRITEDATA, response_buffer)  # Buffer for response

    # Execute the request
    try:
        curl.perform()
        status_code = curl.getinfo(curl.RESPONSE_CODE)  # Get HTTP response code
        print(f"HTTP Status Code: {status_code}")
    except pycurl.error as e:
        print(f"PycURL Error: {e}")
    finally:
        curl.close()  # Cleanup

    # Decode and print the response
    response_data = response_buffer.getvalue().decode('utf-8')
    print("Response Data:")
    return extract_text(response_data)

# Display results if file is uploaded and processed
if uploaded_file:
    st.write("Processing your file...")
    insights = process_file(uploaded_file)
    print (insights)

    if insights:
        st.subheader("Feedback Suggestions")
        st.write(insights)
        exit(0)
        """st.subheader("Key Project Features Summary")
        st.write(insights.get("summary", "No summary generated"))

        st.subheader("Problem Statement Adherence")
        st.write(insights.get("problem_adherence", "No analysis generated"))

        st.subheader("Scoring")
        st.write(f"**Innovation:** {insights.get('innovation', 'No score')}")
        st.write(f"**Feasibility:** {insights.get('feasibility', 'No score')}")
        st.write(f"**Impact:** {insights.get('impact', 'No score')}")
    else:
        st.write("Failed to generate insights.")"""
