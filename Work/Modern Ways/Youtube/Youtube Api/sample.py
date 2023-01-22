# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "/media/kurubal/SSD/Data Scientist/Data Science/Natural-Language-Processing/Hand On/client_secret_1093989666214-j10lq5ma9g39tcovqpeadsovc2h924k2.apps.googleusercontent.com.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

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

if __name__ == "__main__":
    main()