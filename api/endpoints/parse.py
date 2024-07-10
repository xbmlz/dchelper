
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from yt_dlp import YoutubeDL
from utils.utils import extract_valid_urls


router = APIRouter()

class ParseRequest(BaseModel):
    text: str

@router.post("/parse")
async def parse(req: ParseRequest):
    print(req.text)

    if not req.text:
         raise HTTPException(status_code=400, detail="Text is empty")

    url = extract_valid_urls(req.text)
    if not url:
        raise HTTPException(status_code=400, detail="No valid URL found in text")
    
    ydl_opts = {
        'proxy': 'http://172.17.0.1:7890',
    }

    res = {}
    url_list = []
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        
        formats = info.get('formats', [])
        for f in formats:
            if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                url_list.append({
                    'url': f.get('url'),
                    'ext': f.get('ext'),
                    'vcodec': f.get('vcodec'),
                    'acodec': f.get('acodec'),
                    'format': f.get('format'),
                    'format_note': f.get('format_note'),
                    'ext': f.get('ext'),
                    'fps': f.get('fps'),
                    'resolution': f.get('resolution')
                })
        res = {
            'id': info.get('id'),
            'title': info.get('title'),
            'thumbnail': info.get('thumbnail'),
            'description': info.get('description'),
            'formats': url_list
        }
    
    return {"message": "success", "data": res}