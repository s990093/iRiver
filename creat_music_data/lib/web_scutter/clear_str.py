import re


def clear_str(title, artist):
    artist = re.compile(re.escape(artist), flags=re.IGNORECASE)
    artist = delete_tag(artist)
    if artist:
        title = re.sub(r'\s+', '', title)   #刪除格
    # 英文
    title = delete_tag(title)
    # 中文
    title = re.sub(r'主題|歌|《純粹中翻》|中日詞|電影', '', title, flags=re.IGNORECASE) # 刪除 official, music, video (忽略大小寫)
    title = re.sub(f'{artist}', '', title, flags=re.IGNORECASE) # 替換 artist 名稱
    title = re.sub(r'\s*-\s*', '', title) # 刪除 title 和 artist 名稱之間的 -
    title = re.sub(r'[=.#、：\/\[\]－—―–()\|\｜@「」]', '', title) # 刪除特殊符號
    title = re.sub(r'\(.*?mv.*?\)|\[.*?官方.*?\]|（.*?Cover.*?）|\[.*?中.*?\]||\「.*?中.*?\」|\(.*?from.*?\)', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\(\s*\)|（\s*）', '', title) # 刪除括號內部只有空格的情況
    title = re.sub(r'\【\s*\】|（\s*）', '', title) # 刪除【】括號內部只有空格的情況
    title = re.sub(r'＜.*?＞', '', title)
    title = re.sub(r'\【中\】', '', title)
    title = re.sub(r'\【動態\】', '', title)
    title = re.sub(r'\b\d{4}\b|\b\d{1,2}/\d{1,2}\b', '', title).strip() # 刪除年份和日期
    title = re.sub(r'\d{5,}', '', title) #配5個或更多的連續數字
    title = title.strip()  # 刪除前後空格
    return title


def  delete_tag(name):
    return re.sub(r'official|music|video|Audio|demo|Acoustic|version|MV|HD|Remix|live|4k|cover|OP|OfficialYouTubeChannel', '', name, flags=re.IGNORECASE) # 刪除 official, music, video (忽略大小寫
