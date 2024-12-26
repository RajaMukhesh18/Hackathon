import pycurl
from io import BytesIO
import json

# API URL
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyBue4xizhbGN-j_FYUGPuUYGk1pLPyCa8U"

# Request payload
payload = {
    "contents": [
        {
            "parts": [
                {"text": "Explain about AI"}
            ]
        }
    ]
}

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
print(response_data)
