export function fetch_dow_song(music_list) {
    return new Promise((resolve, reject) => {
        fetch(`/music/download?song_info=${encodeURIComponent(JSON.stringify(music_list))}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    fetch_dow_all_songs(music_list.artist_url, music_list.artist);
                    resolve(true); // 回傳成功
                } else {
                    resolve(false); // 回傳失敗
                }
            })
            .catch(error => {
                reject(error); // 回傳錯誤
            });
    });
}

export function fetch_dow_all_songs(artist_url, artist) {
    return new Promise((resolve, reject) => {
        fetch(`/music/download_songs?artist_url=${artist_url}&artist=${artist}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('dow all songs on db');
                    resolve(data.result);
                } else {
                    reject(new Error('Failed to download all songs.'));
                }
            })
            .catch(error => {
                reject(error);
            });
    });
}

