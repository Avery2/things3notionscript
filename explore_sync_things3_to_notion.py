import requests

url = "https://api.notion.com/v1/databases/a1fd716f1a6b4ae6b5fcd8e6817f9af3"

headers = {
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "content-type": "application/json",
    "authorization": "Bearer secret_WtaDbd5hEzeF8A4eppjHHCfJsuuK4gEqITpu0ikcXgM"
}

response = requests.patch(url, headers=headers)

print(response.text)
