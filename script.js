document.addEventListener("DOMContentLoaded", function () {

    const canvas = document.getElementById("matrixCanvas");
    const ctx = canvas.getContext("2d");

    function setupCanvas() {
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
    }

    setupCanvas();

    const letters = "0101AAPP-MART";
    const fontSize = 12;
    let columns = Math.floor(canvas.width / fontSize);
    let drops = new Array(columns).fill(1);

    function draw() {
        ctx.fillStyle = "rgba(15, 32, 39, 0.08)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#00bcd4";
        ctx.font = fontSize + "px monospace";

        for (let i = 0; i < drops.length; i++) {
            const text = letters[Math.floor(Math.random() * letters.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);

            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }

            drops[i]++;
        }
    }

    setInterval(draw, 35);

    window.addEventListener("resize", function () {
        setupCanvas();
        columns = Math.floor(canvas.width / fontSize);
        drops = new Array(columns).fill(1);
    });

});
