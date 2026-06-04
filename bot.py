import scrapetube
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import json

# 1. 아까 복사해둔 구글 웹앱 URL을 여기에 붙여넣으세요! (따옴표 안에 넣으셔야 합니다)
GAS_URL = "https://script.google.com/macros/s/AKfycbzdXlhU7AUIuMrOGTnaGllnvwQUut0zh5Mmp4186BL_Pi9_voN5d316wUbrD1HaDT9j_Q/exec"

# 2. 감시할 채널들의 유튜브 핸들(@)을 적어주세요. (정확한 핸들을 쓰시면 됩니다)
CHANNELS = [
    "@orlandokim",    # 올랜도 킴 (예시)
    "@sosumonkey",    # 소수몽키
    "@WisdomTooth",   # 위즈덤투스
    "@supetv"         # 수페TV
]

for handle in CHANNELS:
    try:
        print(f"[{handle}] 채널 확인 중...")
        # 해당 채널의 가장 최근 영상 1개 가져오기
        videos = scrapetube.get_channel(channel_url=f"https://www.youtube.com/{handle}", limit=1)
        video = next(videos)
        
        video_id = video['videoId']
        title = video['title']['runs'][0]['text']
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        print(f"-> 최신 영상: {title}")

        # 파이썬 무적 라이브러리로 자막 추출 (API 키 불필요)
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
            transcript = " ".join([i['text'] for i in transcript_list])
        except Exception as e:
            print(f"-> 자막이 아직 없거나 추출할 수 없습니다: {e}")
            continue

        # 구글 시트로 쏴주기
        payload = {
            "channel": handle,
            "title": title,
            "url": url,
            "transcript": transcript
        }
        
        response = requests.post(GAS_URL, json=payload)
        
        if response.status_code == 200:
            print(f"-> 구글 시트로 전송 완료!")
        else:
            print(f"-> 전송 에러: {response.status_code}")

    except Exception as e:
        print(f"[{handle}] 채널 에러 발생: {e}")
