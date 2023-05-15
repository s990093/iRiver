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

/**
 *
 * @class Fetch class for performing HTTP requests.
 */
export class Fetch {
    constructor() {
        this.session = this._get_cookie();
        this.cookie = this._get_cookie();
    }

    /**
     * @method GET_template - 发送 GET 请求并带有参
     * @param {string} target - params = {
                                param1: 'value1',
                                param2: 'value2',
                                param3: 'value3'
                                };
     * 
     * @param {Object} params - 参数对象
     * @returns {Promise<Response>} - 返回包含响应数据的 Promise 对象
     */
    async GET_template(target, params) {
        const url = new URL(target);
        const searchParams = new URLSearchParams(params);

        url.search = searchParams.toString();

        const data = await fetch(url);
        return data;
    }

    _get_seesion() {
        return "test";
    }
    _get_cookie() {
        return "test";
    }

    get_playlist() {
        var playlist = ["專輯1", "專輯2"];
        return playlist;
    }
}