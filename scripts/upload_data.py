import requests

# Get the token
response = requests.post("http://localhost:8000/api/v1/login",
                        data={"username": "user@example.com", "password": "user123"})
print(response.json())
token = response.json()["access_token"]
print(token)

# Get the presigned URL
response = requests.post("http://localhost:8000/api/v1/generate-upload-url",
                         headers={"Authorization": f"Bearer {token}"})
data = response.json()

# Upload the file
with open("./data/superhero_genetic_data.zip", "rb") as f:
    upload_response = requests.put(
        data["upload_url"],
        data=f,
        headers={"Content-Type": "application/zip"}
    )

print(upload_response)