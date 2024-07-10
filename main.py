# import json
# from yt_dlp import YoutubeDL

# ydl_opts = {}
# video_url = "https://www.youtube.com/watch?v=kNU2WCHVVBk"

# with YoutubeDL(ydl_opts) as ydl:
#     info = ydl.extract_info(video_url, download=False)
#     formats = info.get('formats', [])
#     res = []
#     for f in formats:
#         if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
#             res.append({
#                 'url': f.get('url'),
#                 'ext': f.get('ext'),
#                 'vcodec': f.get('vcodec'),
#                 'acodec': f.get('acodec'),
#             })
#     print(json.dumps(res, indent=4))

from fastapi import FastAPI

import uvicorn

from api.router import router

app = FastAPI()

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
