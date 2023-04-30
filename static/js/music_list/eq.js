export class Eq {
    constructor(audioElement, isTest = false) {
        this.isTest = isTest;
        this.audioElement = audioElement;
        this.context = new AudioContext();
        this.sourceNode = this.context.createMediaElementSource(this.audioElement);
        this.filterNode = this.context.createBiquadFilter();
        this.pannerNode = this.context.createPanner();

        this.sourceNode.connect(this.filterNode);
        this.filterNode.connect(this.pannerNode);
        this.pannerNode.connect(this.context.destination);



        this.setLowStereo = this.setLowStereo.bind(this);



        // // 创建压缩器
        // this.compressor = this.context.createDynamicsCompressor();
        // this.filterNode.connect(this.compressor);
        // this.compressor.connect(this.pannerNode);

        // // 创建失真器
        // this.distortion = this.context.createWaveShaper();
        // this.distortion.curve = this.makeDistortionCurve(400); // 使用自定义曲线函数
        // this.pannerNode.connect(this.distortion);
        // this.distortion.connect(this.context.destination);
        this._register();
    }

    _register() {
        this.setHighGain(0);
        this.setMidGain(0);
        this.setLowGain(0);
        this.setSuperBass(0);


        // 多聲道
        // this.setLowStereo(0, 0);
    }

    setHighGain(value) {
        this.filterNode.type = 'highshelf';
        this.filterNode.frequency.value = 2000;
        this.filterNode.gain.value = value || 0; // 默认值为0
    }

    setMidGain(value) {
        this.filterNode.type = 'peaking';
        this.filterNode.frequency.value = 1000;
        this.filterNode.Q.value = 1;
        this.filterNode.gain.value = value || 0; // 默认值为0
    }

    setLowGain(value) {
        this.filterNode.type = 'lowshelf';
        this.filterNode.frequency.value = 300;
        this.filterNode.gain.value = value || 0; // 默认值为0
    }

    setSuperBass(value) {
        this.filterNode.type = 'lowshelf';
        this.filterNode.frequency.value = 100;
        this.filterNode.gain.value = value || 0; // 默认值为0
    }

    // 多聲道測試
    setLowStereo(value, angle = 30) {
        // 創建節點
        const splitter = this.context.createChannelSplitter(4);
        const lowNodes = Array.from({ length: 4 }, () => {
            const lowNode = this.context.createBiquadFilter();
            lowNode.type = 'lowshelf';
            lowNode.frequency.value = 200;
            lowNode.gain.value = value;
            return lowNode;
        });

        const merger = this.context.createChannelMerger(4);

        // 將節點連接起來
        lowNodes.forEach((lowNode, index) => {
            splitter.connect(lowNode, index);
            lowNode.connect(merger, 0, index);
        });

        // 將合併節點連接到音頻源節點
        this.sourceNode.disconnect();
        this.sourceNode.connect(splitter);
        merger.connect(this.context.destination);
    }


    //風格
    setGenre(genre) {
        switch (genre) {
            case 'pop':
                this.audioElement.style.filter = 'brightness(1.2) saturate(1.2)';
                break;
            case 'rock':
                this.audioElement.style.filter = 'contrast(1.2) saturate(0.8)';
                break;
            case 'jazz':
                this.audioElement.style.filter = 'hue-rotate(90deg) brightness(0.8)';
                break;
            case 'classical':
                this.audioElement.style.filter = 'sepia(0.5) brightness(1.2)';
                break;
            case 'electronic':
                this.audioElement.style.filter = 'invert(1) hue-rotate(180deg)';
                break;
            case 'hip-hop':
                this.audioElement.style.filter = 'grayscale(1) contrast(1.5)';
                break;
            default:
                this.audioElement.style.filter = 'none';
        }
    }

    // 樂器靠前
    setInstrumentPosition(x, y, z) {
        switch (instrument) {
            case 'guitar':
                this.pannerNode.positionX.setValueAtTime(x, this.audioContext.currentTime);
                this.pannerNode.positionY.setValueAtTime(y, this.audioContext.currentTime);
                this.pannerNode.positionZ.setValueAtTime(z, this.audioContext.currentTime);
                break;
            case 'bass':
                this.pannerNode.positionX.setValueAtTime(x, this.audioContext.currentTime);
                this.pannerNode.positionY.setValueAtTime(y, this.audioContext.currentTime);
                this.pannerNode.positionZ.setValueAtTime(-z, this.audioContext.currentTime);
                break;
            case 'drums':
                this.pannerNode.positionX.setValueAtTime(-x, this.audioContext.currentTime);
                this.pannerNode.positionY.setValueAtTime(y, this.audioContext.currentTime);
                this.pannerNode.positionZ.setValueAtTime(z, this.audioContext.currentTime);
                break;
            case 'vocals':
                this.pannerNode.positionX.setValueAtTime(-x, this.audioContext.currentTime);
                this.pannerNode.positionY.setValueAtTime(y, this.audioContext.currentTime);
                this.pannerNode.positionZ.setValueAtTime(z, this.audioContext.currentTime);
                break;
            default:
                this.pannerNode.positionX.setValueAtTime(0, this.audioContext.currentTime);
                this.pannerNode.positionY.setValueAtTime(0, this.audioContext.currentTime);
                this.pannerNode.positionZ.setValueAtTime(0, this.audioContext.currentTime);
        }
    }

    // 自定义失真曲线函数
    makeDistortionCurve(amount) {
        const k = typeof amount === 'number' ? amount : 50;
        const nSamples = 44100;
        const curve = new Float32Array(nSamples);
        const deg = Math.PI / 180;
        let x;

        for (let i = 0; i < nSamples; i++) {
            x = (i * 2) / nSamples - 1;
            curve[i] = ((3 + k) * x * 20 * deg) / (Math.PI + k * Math.abs(x));
        }

        return curve;
    }

    // 控制压缩器的参数
    setCompressorThreshold(value) {
        this.compressor.threshold.setValueAtTime(value, this.context.currentTime);
    }

    setCompressorRatio(value) {
        this.compressor.ratio.setValueAtTime(value, this.context.currentTime);
    }

    // 控制失真器的参数
    setDistortionAmount(value) {
        this.distortion.curve = makeDistortionCurve(value);
    }


}



