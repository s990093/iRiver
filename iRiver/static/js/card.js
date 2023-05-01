const cards = document.querySelectorAll(".myCard");

// 检查是否为触摸设备
const isTouchDevice = window.matchMedia("(hover: none)").matches;

// 绑定点击事件
cards.forEach((card) => {
    if (isTouchDevice) {
        // 触摸设备，绑定 touchstart 事件
        card.addEventListener("touchstart", () => {
            card.classList.toggle("flipped");
        });
    } else {
        // 非触摸设备，绑定 click 事件
        card.addEventListener("click", () => {
            card.classList.toggle("flipped");
        });
    }
});