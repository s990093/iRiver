/**
 * Perform the download of a song.
 * @param music_list - The music list containing song information.
 * @returns A Promise that resolves to a boolean value indicating the success of the download.
 */
export function fetch_dow_song(music_list: any): Promise<boolean> {
  console.log(typeof music_list);
  return new Promise<boolean>((resolve, reject) => {
    fetch(
      `/music/download?song_info=${encodeURIComponent(
        JSON.stringify(music_list)
      )}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          fetch_dow_all_songs(music_list.artist_url, music_list.artist);
          resolve(true); // 回傳成功
        } else {
          resolve(false); // 回傳失敗
        }
      })
      .catch((error) => {
        reject(error); // 回傳錯誤
      });
  });
}

export function fetch_dow_all_songs(
  artist_url: string,
  artist: string
): Promise<any> {
  return new Promise<any>((resolve, reject) => {
    fetch(`/music/download_songs?artist_url=${artist_url}&artist=${artist}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          console.log("dow all songs on db");
          resolve(data.result);
        } else {
          reject(new Error("Failed to download all songs."));
        }
      })
      .catch((error) => {
        reject(error);
      });
  });
}

export function fetch_is_song_exit(music_ID: string): Promise<boolean> {
  return new Promise<boolean>((resolve, reject) => {
    fetch(`/music/is_song_exit?music_ID=${music_ID}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          resolve(true);
        } else {
          resolve(false);
        }
      })
      .catch((error) => {
        reject(error);
      });
  });
}

/**
 *
 * @class Fetch class for performing HTTP requests.
 */
export class Fetch {
  constructor() {}

  get_session(music_ID: string): Promise<any> {
    return new Promise<any>((resolve, reject) => {
      resolve("session");
      // 执行异步操作的逻辑
    });
  }
  /**
   * Perform a GET request.
   * @param url The URL to send the request to.
   * @returns A Promise resolving to the response data.
   */
  get(url: string): Promise<any> {
    return new Promise<any>((resolve, reject) => {
      // 执行 GET 请求的逻辑
    });
  }

  /**
   * Perform a POST request.
   * @param url The URL to send the request to.
   * @param data The data to send in the request body.
   * @returns A Promise resolving to the response data.
   */
  post(url: string, data: any): Promise<any> {
    return new Promise<any>((resolve, reject) => {
      // 执行 POST 请求的逻辑
    });
  }
}
