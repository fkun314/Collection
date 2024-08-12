<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>かんじ１</title>
    <style>
        @page {
            size: A4 landscape
        }

        /* A4横 */
        body {
            width: 1100px;
            height: 750px;
            padding: 0px;
            margin: 0px;
            position: relative;
        }

        canvas {
            position: absolute;
            top: 50%;
            left: 50%;
            -webkit-transform: translateY(-50%) translateX(-50%);
            transform: translateY(-50%) translateX(-50%);
            padding: 20px;
        }
    </style>
</head>

<body onload="draw()">
    <div class="one-page">
        <canvas id="line" width="1000px" height="700px"></canvas>
        <canvas id="sub-line" width="1000px" height="700px"></canvas>
        <canvas id="kanji" width="1000px" height="700px"></canvas>
    </div>
    <script>
        function draw() {
            var canvas = document.getElementById('sub-line');
            if (canvas.getContext) {
                var ctx = canvas.getContext('2d');
                for (i = 0; i < 700; i += 75 / 2) {
                    if (i % 75 != 0) {
                        ctx.setLineDash([5, 5]);
                        ctx.beginPath();
                        ctx.moveTo(0, 250 + i); // 始点に移動
                        ctx.lineTo(150, 250 + i); // 終点
                        ctx.lineWidth = 1; // 線の太さ
                        ctx.stroke();
                    }
                }
                for (i = 0; i < 150; i += 75 / 2) {
                    if (i % 75 != 0) {
                        ctx.setLineDash([5, 5]);
                        ctx.beginPath();
                        ctx.moveTo(i, 250); // 始点に移動
                        ctx.lineTo(i, 700); // 終点
                        ctx.lineWidth = 1; // 線の太さ
                        ctx.stroke();
                    }
                }
                ctx.beginPath();
                ctx.moveTo(100,10);
                ctx.lineTo(100, 140);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(30,75);
                ctx.lineTo(170, 75);
                ctx.stroke();
            }
            var canvas = document.getElementById('line');
            if (canvas.getContext) {
                var ctx = canvas.getContext('2d');
                // ctx.fillRect(50,50,300,260);
                // ctx.clearRect(120,80,200,180);
                // ctx.strokeRect(180,20,180,180);
                    ctx.lineWidth = 2; // 線の太さ
                    ctx.strokeRect(30, 10, 140, 130);
                for (i = 0; i < 5; i++) {
                    ctx.strokeRect(i * 200, 0, 200, 150);
                    ctx.strokeRect(i * 200, 150, 200, 100);
                    ctx.strokeRect(i * 200, 250, 150, 450);
                    ctx.strokeRect((i * 200) + 150, 250, 50, 450);
                }
                ctx.beginPath();
                ctx.moveTo(75, 250); // 始点に移動
                ctx.lineTo(75, 700); // 終点
                ctx.stroke();
                for (i = 0; i < 700; i += 75) {
                    ctx.beginPath();
                    ctx.moveTo(0, 250 + i); // 始点に移動
                    ctx.lineTo(150, 250 + i); // 終点
                    ctx.stroke();
                }
            }
            var canvas = document.getElementById('kanji');
            if (canvas.getContext) {
                var ctx = canvas.getContext('2d');
                // ctx.fillRect(50,50,300,260);
                // ctx.clearRect(120,80,200,180);
                // ctx.strokeRect(180,20,180,180);
                var top = "一";
                tategaki(ctx, top, 40, 120, 120);
                var onsound = "音:イチ・イツ";
                ctx.font = "20px 'HG正楷書体-PRO'";
                ctx.fillText(onsound, 10, 180, 180);
                var kunsound = "訓:ひと・ひと(つ)";
                ctx.fillText(kunsound, 10, 210, 180);
                var ex = "一かい　一もじ　一ど";
                tategaki(ctx, ex, 160, 300, 30);
            }
        }

        var tategaki = function(context, text, x, y, ft) {
            var size = ft + "px 'HG正楷書体-PRO'";
            context.font = size;
            var textList = text.split('\n');
            var lineHeight = context.measureText("あ").width;
            textList.forEach(function(elm, i) {
                Array.prototype.forEach.call(elm, function(ch, j) {
                    context.fillText(ch, x - lineHeight * i, y + lineHeight * j);
                });
            });
        };
    </script>
</body>

</html>