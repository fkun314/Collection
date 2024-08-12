<?php
require_once('./config.php');

if (!session_id()) {
    session_start();
}

$code = $_GET['code'];
//echo '$code= ' . $code . '<br /><br />';

$state = $_GET['state'];
// echo '$state= ' . $state . '<br /><br />';

$session_state = $_SESSION['_line_state'];
unset($_SESSION['_line_state']);
if ($session_state !== $state) {
    echo 'アクセスエラー';
    exit;
}

//**************
// 各種値の設定
//**************
$base_url = "https://api.line.me/oauth2/v2.1/token";
$client_id = CLIENT_ID;
$client_secret = CLIENT_SECRET;
$redirect_uri = REDIRECT_URI;

$url = "https://api.line.me/oauth2/v2.1/token";

//----------------------------------------
// POSTパラメータの作成
//----------------------------------------
$query = "";
$query .= "grant_type=" . urlencode("authorization_code") . "&";
$query .= "code=" . urlencode($code) . "&";
$query .= "redirect_uri=" . urlencode($redirect_uri) . "&";
$query .= "client_id=" . urlencode($client_id) . "&";
$query .= "client_secret=" . urlencode($client_secret) . "&";

//--------------------
// HTTPヘッダーの設定
//--------------------
$header = array(
    "Content-Type: application/x-www-form-urlencoded",
    "Content-Length: " . strlen($query),
);

//--------------------------------
// コンテキスト（各種情報）の設定
//--------------------------------
$context = array(
    "http" => array(
        "method"        => "POST",
        "header"        => implode("\r\n", $header),
        "content"       => $query,
        "ignore_errors" => true,
    ),
);

//---------------------
// id token を取得する
//---------------------
$res_json = file_get_contents($url, false, stream_context_create($context));

//----------------------------------
// 取得するデータを展開して表示する
//----------------------------------

// 取得したjsonデータをオブジェクト化
$res = json_decode($res_json);
// echo '$res= ';
// print_r($res); // LINEから取得したデータの表示
// echo '<br /><br />';

// エラーを取得
if (isset($res->error)) {
    echo 'ログインエラーが発生しました。<br />';
    echo "error: " . $res->error . '<br />';
    echo $res->error_description;
    exit;
}

//id_token(JWT)を分解
$val = explode(".", $res->id_token);
// echo '$val= ';
// print_r($val);
// echo '<br /><br />';

//2番目がデータ部分(PAYLOAD)なのでbase64でデコード
$data_json = base64_decode($val[1]);
// echo '$data_json= ';
// print_r($data_json);
// echo '<br /><br />';

//bsae64でデコードしたjsonをオブジェクト化
$data = json_decode($data_json);
// echo '$data= ';
// print_r($data);
// echo '<br /><br />';

//取得したデータを表示
//print("[sub]:[" . $data->sub . "][対象ユーザーの識別子]<br />\n");

$url = 'https://script.google.com/macros/s/AKfycbzz3Y7annmsZfS1a3SUWCuCObGczNQIak6iKkFSGRxNMZNfHhrx/exec';

if (!($data->sub)) {

    $data = array(
        'id' => $data->sub,
    );

    $context = array(
        'http' => array(
            'method'  => 'POST',
            'header'  => implode("\r\n", array('Content-Type: application/x-www-form-urlencoded',)),
            'content' => http_build_query($data)
        )
    );

    $html = file_get_contents($url, false, stream_context_create($context));
    $date_cut = preg_split('/[,]+/', $html, -1, PREG_SPLIT_NO_EMPTY);
}

//var_dump($http_response_header);
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personal_Date</title>
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
        <?php
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
            // $('.hyoji').append("<tbody><tr><td>1</td><td>エンジニア1</td><td>PHP</td></tr></tbody></table></div>");
            // $('.hyoji').append('');
            // console.log(tbody);
            // $('.hyoji').append('<tbody>'+tbody + '</tbody></table></div>');
        })
    </script>
</body>

</html>