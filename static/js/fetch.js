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
    constructor() { }

    _get_seesion() {
        return "test";
    }

    _get_cookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    /**
    * @method GET - 发送 GET 请求并带有参
    * @param {string} target - params = {
                               param1: 'value1',
                               param2: 'value2',
                               param3: 'value3'
                               };
    * 
    * @param {Object} params - 参数对象
    * @returns {Promise<Response>} - 返回包含响应数据的 Promise 对象
    */
    async GET(target) {
        return new Promise((resolve, reject) => {
            fetch(target)
                .then(response => response.json())
                .then(data => {
                    resolve(data.isLogin);
                })
                .catch(error => {
                    reject(error);
                });
        });
    }

    async POST(target, params = null) {
        return new Promise(async (resolve, reject) => {
            try {
                const csrftoken = this._get_cookie('csrftoken');
                const response = await fetch(target, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify(params)
                });

                if (!response.ok) {
                    throw new Error('Failed with status code: ' + response.status);
                }
                const data = await response.json();
                resolve(data);
            } catch (error) {
                reject(false);
            }
        });
    }

}