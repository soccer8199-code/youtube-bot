import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
import requests

# 1. 구글 웹앱 URL (아까 킵해두신 웹앱 주소를 다시 한번 정확히 넣어주세요)
GAS_URL = "https://script.google.com/macros/s/AKfycbzdXlhU7AUIuMrOGTnaGllnvwQUut0zh5Mmp4186BL_Pi9_voN5d316wUbrD1HaDT9j_Q/exec"

# 2. 감시할 채널들의 유튜브 핸들
# ❗ 각 채널마다 반드시 따옴표를 닫고 끝에 쉼표(,)를 찍어야 합니다.
CHANNELS = [
    "@orlandocampus",
    "@sosumonkey",
    "@위즈덤투스",
    "@supetv",
    "@moneymoneycomics"
]

for handle in CHANNELS:
    try:
        print(f"[{handle}] 최신 영상 확인 중...")
        
        ydl_opts = {
            'extract_flat': True,
            'playlist_items': '1',
            'quiet': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/{handle}/videos", download=False)
            
            if not info or 'entries' not in info or len(info['entries']) == 0:
                print("-> 영상을 찾을 수 없습니다.")
                continue
            
            video = info['entries'][0]
            video_id = video['id']
            title = video['title']
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            print(f"-> 찾음: {title}")

        # ❗ [핵심 해결] 최신 버전 문법으로 변경된 부분 (fetch 사용)
        try:
            ytt_api = YouTubeTranscriptApi()
            transcript_list = ytt_api.fetch(video_id, languages=['ko', 'en'])
            transcript = " ".join([i['text'] for i in transcript_list])
        except Exception as e:
            print(f"-> 자막 추출 에러: {e}")
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
