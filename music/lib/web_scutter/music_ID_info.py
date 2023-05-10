from pytube import YouTube


def get_music_ID_info(music_ID):
    url = f"https://www.youtube.com/watch?v={music_ID}"
    yt = YouTube(url)
    keywords = None
    description = None
    views = 0
    rating = None
    publish_time = 0
    chinese_lyrics = None
    english_lyrics = None

    try:
        keywords = yt.keywords

        description = yt.description

        views = yt.views

        publish_time = yt.publish_date.year

        rating = yt.rating

        chinese_captions = yt.captions.get_by_language_code('zh-Hans')
        if chinese_captions:
            chinese_lyrics = chinese_captions.generate_srt_captions()

        english_captions = yt.captions.get_by_language_code('en')
        if english_captions:
            english_lyrics = english_captions.generate_srt_captions()

    except Exception as e:
        print(f"on web_scutter get_mysic_ID_datail {e}")

    # Create a dictionary with the extracted data
    video_info = {
        'keywords': keywords,
        'description': description,
        'publish_time': publish_time,
        'views': views,
        'rating': rating,
        'ch_lyrics': chinese_lyrics,
        'en_lyrics': english_lyrics
    }

    return video_info
