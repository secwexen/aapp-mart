document.addEventListener("DOMContentLoaded", function () {

    const canvas = document.getElementById("matrixCanvas");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    function resize() {
        canvas.width = canvas.clientWidth;
        canvas.height = canvas.clientHeight;
    }

    resize();
    window.addEventListener("resize", resize);

    const nodes = [];
    const nodeCount = 30;
    const maxDistance = 150;

    for (let i = 0; i < nodeCount; i++) {
        nodes.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.3,
            vy: (Math.random() - 0.5) * 0.3
        });
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        for (let i = 0; i < nodes.length; i++) {
            for (let j = i + 1; j < nodes.length; j++) {

                const dx = nodes[i].x - nodes[j].x;
                const dy = nodes[i].y - nodes[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < maxDistance) {
                    ctx.strokeStyle = "rgba(0, 188, 212, " + (1 - dist / maxDistance) * 0.12 + ")";
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.moveTo(nodes[i].x, nodes[i].y);
                    ctx.lineTo(nodes[j].x, nodes[j].y);
                    ctx.stroke();
                }
            }
        }

        for (let node of nodes) {

            ctx.fillStyle = "rgba(0,188,212,0.5)";
            ctx.beginPath();
            ctx.arc(node.x, node.y, 2, 0, Math.PI * 2);
            ctx.fill();

            node.x += node.vx;
            node.y += node.vy;

            if (node.x <= 0 || node.x >= canvas.width) node.vx *= -1;
            if (node.y <= 0 || node.y >= canvas.height) node.vy *= -1;
        }

        requestAnimationFrame(draw);
    }

    draw();
});
