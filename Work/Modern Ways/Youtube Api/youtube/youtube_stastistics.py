import requests
import json


class YTstats:

    def __init__(self, api_key, video_id):
        self.api_key = api_key
        self.video_id = video_id
        self.video_statistics = None
    
    def get_video_statistics(self):
        url = f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={self.video_id}&key={self.api_key}'
        print(url)
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data["items"][0]["statistics"]
        except:
            data = None 

        self.video_statistics = data
        return data

    def dump(self):
        if self.video_statistics is None:
            return

        video_title = "video"
        video_title = video_title.replace(" ", "_").lower()
        file_name = video_title + ".json"
        with open(file_name, "w") as f:
            json.dump(self.video_statistics, f, indent=4)
        
        print('file dumped')

