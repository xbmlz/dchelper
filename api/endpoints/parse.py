
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from yt_dlp import YoutubeDL
from utils.utils import extract_valid_urls


router = APIRouter()

MP_NOT_DOWNLOADABLE = ['youtube']

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
        'proxy': 'http://193.112.175.178:7890',
    }

    res = {}
    url_list = []
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        # 写入json文件
        with open('info.json', 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=4)
        
        formats = info.get('formats', [])
        for f in formats:
            if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                url_list.append(f)
        if not url_list:
            raise HTTPException(status_code=400, detail="No valid video format found")
        
        # TODO: add more info to response
        res = {
            'id': info.get('id'),
            'title': info.get('title'),
            'thumbnail': info.get('thumbnail'),
            'description': info.get('description'),
            'extractor': info.get('extractor'),
            'url': url_list[0].get('url'),
            'ext': url_list[0].get('ext'),
            'vcodec': url_list[0].get('vcodec'),
            'acodec': url_list[0].get('acodec'),
            'format': url_list[0].get('format'),
            'format_note': url_list[0].get('format_note'),
            'ext': url_list[0].get('ext'),
            'fps': url_list[0].get('fps'),
            'resolution': url_list[0].get('resolution'),
            'filesize_approx': url_list[0].get('filesize_approx'),
            'filesize': url_list[0].get('filesize'),
            'mp_downloadable': info.get('extractor') not in MP_NOT_DOWNLOADABLE
        }
    
    return {"message": "success", "data": res}