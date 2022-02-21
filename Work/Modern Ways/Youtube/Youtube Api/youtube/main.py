from youtube_stastistics import YTstats

API_KEY = "AIzaSyDxi_HowF_0WKoWQsFNAiSLwgMb5gWCEDk"
video_id = "oQyaI7Bt1Ig"

yt = YTstats(API_KEY, video_id)
#yt.get_video_statistics()
#yt.dump()

data = yt.get_video_statistics()
print(data)