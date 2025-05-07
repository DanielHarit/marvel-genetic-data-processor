import requests

# Get the presigned URL
response = requests.post("http://localhost:8000/api/v1/generate-upload-url")
data = response.json()

# Upload the file
with open("./data/superhero_genetic_data.zip", "rb") as f:
    upload_response = requests.put(
        data["upload_url"],
        data=f,
        headers={"Content-Type": "application/zip"}
    )

print(upload_response)