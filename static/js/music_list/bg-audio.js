export class bgAudio {
	constructor(isTets = false) {
		this.isTets = isTets;
	}

	updateMediaSessionMetadata(music_list) {
		this.currentSong = music_list;
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

			if (this.isTets) {
				console.log(navigator.mediaSession.metadata);
			}
		}
	}

}








