from googleapiclient.discovery import build

api_key = "AIzaSyA3oohdkwOh9sxB7u5gkybRL6Thpcksg98"

youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.search().list(
        part="snippet",
        location="40.042126, 30.650741",
        locationRadius="400km",
        order="viewCount",
        relevanceLanguage="TR",
        type="video",
        videoCaption="closedCaption",
        videoEmbeddable="true",
        videoLicense="any",
        videoSyndicated="true",
        videoType="any"
    )
response = request.execute()

print(response)