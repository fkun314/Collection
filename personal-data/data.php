<?php
// $date = "2020/3/14,15:00,36.5,2020/3/14,18:00,36.1,2020/3/16,15:00,36.3,2020/4/5,15:35,37.1";
if (isset($_GET['id'])) {
    $getid = $_GET['id'];
}
$result = file_get_contents('https://script.google.com/macros/s/AKfycbzz3Y7annmsZfS1a3SUWCuCObGczNQIak6iKkFSGRxNMZNfHhrx/exec?id=' . $getid);
$date = $result;
$date_cut = preg_split('/[,]+/', $date, -1, PREG_SPLIT_NO_EMPTY);
print_r($array_keyword);

?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personal_Data</title>
    <!-- BootstrapのCSS読み込み -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <!-- jQuery読み込み -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <!-- BootstrapのJS読み込み -->
    <script src="js/bootstrap.min.js"></script>
    <style>
        body {
            max-width: 700px;
            margin: auto;
        }
    </style>
</head>

<body>
    <div class="header">
        <nav class="navbar navbar-light bg-light justify-content-center">
            <a class="navbar-brand" href="#">
                <img src="./photo/favicon.ico" width="30" height="30" class="d-inline-block align-top" alt="">
                体温記録帳
            </a>
        </nav>
    </div>
    <div class="hyoji">

    </div>

    <script>
        //var date = [[],[],[]];

        var token = 0;
        <?php
        if(!$result){echo('token = 0;');}else{echo('token = 1;');}
            $count = 0;
            $date_length = count($date_cut);
            echo ('var date = [];for (var i = 0; i < ' . (($date_length) / 3) . ' ; i++) {date[i] = [];}');
            echo ("var date_length = " . $date_length . ";");
            echo ("var date_length_3 = " . ($date_length / 3) . ";");
            $push . "].push(";
            for ($i = 0; $i < $date_length; $i += 3) {
                echo ('date[' . ($count) . "].push('" . $date_cut[$i] . "');");
                echo ('date[' . ($count) . "].push('" . $date_cut[$i + 1] . "');");
                echo ('date[' . ($count) . "].push('" . $date_cut[$i + 2] . "');");
                $count++;
            }
        ?>
        console.log(date);
        $(function() {
            if(token){
            var tbody = '<div class="mx-4"><table class="table table-striped"><thead><tr><th><div class="text-center">日付</div></th><th><div class="text-center">時刻</div></th><th><div class="text-center">体温（℃）</div></th></tr></thead><tbody>';
            for (var j = 0; j < date_length_3; j++) {
                if (date[j][2] < 37.0) {
                    tbody += ('<tr><td><div class="text-center">' + date[j][0] + '</div></td><td><div class="text-center">' + date[j][1] + '</div></td><td><div class="text-center">' + date[j][2] + '</div></td></tr>');
                } else {
                    tbody += ('<tr><td style="color:red"><div class="text-center">' + date[j][0] + '</div></td><td style="color:red"><div class="text-center">' + date[j][1] + '</div></td><td style="color:red"><div class="text-center">' + date[j][2] + '</div></td></tr>');
                }
            }
            tbody += "</tbody></table></div>";
            $('.hyoji').append(tbody);
            }
            else{
                $('.hyoji').append('不正なアクセスです。データベースの閲覧は１つのURLで１回しかできません。<br>LINEで「データベース」と入力し、新しいURLから再度アクセスをお願いします。');
            }
            // $('.hyoji').append("<tbody><tr><td>1</td><td>エンジニア1</td><td>PHP</td></tr></tbody></table></div>");
            // $('.hyoji').append('');
            // console.log(tbody);
            // $('.hyoji').append('<tbody>'+tbody + '</tbody></table></div>');
        })
    </script>
</body>

</html>