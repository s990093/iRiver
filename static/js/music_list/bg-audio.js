export class bgAudio {
	constructor(music_list, currentIndex = 0) {
		this.musicList = music_list;
		this.currentIndex = currentIndex;

		this._register(this.currentIndex);
	}

	_register(currentIndex = 0) {
		// this.updateMediaSessionMetadata(currentIndex);
	}

	updateMediaSessionMetadata(currentIndex = 0) {
		this.currentIndex = currentIndex;
		this.currentSong = this.musicList[currentIndex];
		if ('mediaSession' in navigator) {
			const metadata = new MediaMetadata({
				title: this.currentSong.title,
				artist: this.currentSong.artist,
				album: this.currentSong.artist,

				artwork: [
					{
						src: '/media/' + this.currentSong.artist + '/img/' + this.currentSong.music_ID + '.jpg',
						sizes: '512x512',
						type: 'image/png'
					}
				]
			});

			// 刪除之前的 metadata
			// if (navigator.mediaSession.metadata) {
			// 	delete navigator.mediaSession.metadata;
			// }

			navigator.mediaSession.metadata = metadata;
			console.log(navigator.mediaSession.metadata);
		}
	}

}








