import requests

def fetch_data(url):
  response = requests.get(url)
  if response.status_code == 200:
    return response.json()
  else:
    return "Failed to fetch data"

if __name__ == "__main__":
  url = "https://jsonplaceholder.typicode.com/posts/1"
  data = fetch_data(url)
  print(data)