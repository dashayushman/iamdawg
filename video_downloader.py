import json
import time
from pathlib import Path
import os
import requests
from pypexels import PyPexels

from azure.storage.blob import BlobClient



import requests
from tqdm import tqdm

baseurl = "https://api.pexels.com/videos/search?query="

payload = {}
headers = {
  'Authorization': '563492ad6f91700001000001aeb006d415ed4a22bda755bf22efc602',
}


def get_pexels_results(query, page_number, num_res_per_page):
    url = f"{baseurl}{query}&per_page={num_res_per_page}&page={page_number}"
    response = requests.request("GET", url, headers=headers, data = payload)
    json_response = json.loads(response.text)
    return json_response



def download_image(url, root_dir, filename):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
    response = requests.get(url, stream=True, headers=headers)
    filename = f"{filename}.mp4"
    filepath = Path(root_dir) / filename

    with open(filepath, 'wb') as file:
        for chunk in tqdm(response.iter_content(10000)):
            file.write(chunk)


SEARCH_QUERY = "dogs"
NUM_PAGES = 20
ITEMS_PER_PAGE = 10

for i in range(NUM_PAGES):
    search_results = get_pexels_results(SEARCH_QUERY, i + 1, ITEMS_PER_PAGE)
    #print(search_results)
    for video in search_results["videos"]:
        dest_dir = "./video_data"
        video_filename = os.path.join(dest_dir, f"{video['id']}.mp4")
        if os.path.exists(video_filename):
            print("skipping as it exists")
            continue
        print(video["id"], video["user"]["name"], video["url"])
        image_url = f"https://www.pexels.com/video/{video['id']}/download"
        download_image(image_url, dest_dir, str(video["id"]))
        metadata_file = f"./video_metadata/{video['id']}.json"
        with open(metadata_file, "w") as file:
            json.dump({"download_url": image_url, "id": video['id'], "video_url": video["url"],
                       "videographer": video["url"]}, file)
        time.sleep(20)
