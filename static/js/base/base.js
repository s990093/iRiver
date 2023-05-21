import { KeybroadCollenter } from "./keybroad.js";

// 必載入必要js檔案
class Base {
    constructor() {
        this.keybroadCollenter = new KeybroadCollenter();
    }
}


const base = new Base();