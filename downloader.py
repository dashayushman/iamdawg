import json
from pathlib import Path
import os
import requests
from pypexels import PyPexels

from azure.storage.blob import BlobClient



api_key = '563492ad6f91700001000001aeb006d415ed4a22bda755bf22efc602'

# instantiate PyPexels object
py_pexels = PyPexels(api_key=api_key)


def download_image(url, root_dir, filename):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
    response = requests.get(url, stream=True, headers=headers)
    filename = f"{filename}.jpg"
    filepath = Path(root_dir) / filename

    with open(filepath, 'wb') as file:
        for chunk in response.iter_content(10000):
            file.write(chunk)
    try:
        with open(filepath, "rb") as data:
            blob = BlobClient.from_connection_string(
                conn_str="DefaultEndpointsProtocol=https;AccountName=nsindgovtdiag;AccountKey=CVHI0omjl5e2vx7/Nw0b0z8/LEt1W6YLCbyGCZ632zqARMZvWlzx/MdXMSZpbg16xkrrEAEDGyQii4yqxK295w==;EndpointSuffix=core.windows.net",
                container_name="highondogs",
                blob_name=filename)
            blob.upload_blob(data)
    except:
        pass
    #os.remove(filepath)


search_results = py_pexels.search(query='funny dogs', per_page=10)


for _ in range(1):
    for photo in search_results.entries:
        print(photo.id, photo.photographer, photo.url)
        image_url = f"https://www.pexels.com/photo/{photo.id}/download"
        dest_dir = "./data"
        download_image(image_url, dest_dir, str(photo.id))
        metadata_file = f"./metadata/{photo.id}.json"
        with open(metadata_file, "w") as file:
            json.dump({"download_url": image_url, "id": photo.id, "photo_url": photo.url,
                       "photographer": photo.photographer}, file)
    if not search_results.has_next:
        break
    search_results = search_results.get_next_page()