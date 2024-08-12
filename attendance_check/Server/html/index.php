<?php

$path = "/home/g02_1/pdf";
$htmlPath = '/home/g02_1/html';
 
$list = array();
$htmlList = array();

//  ディレクトリに読み取り権限があるか確認
if( is_readable($path) ) {

	// ディレクトリ内のファイルを取得
	$files = scandir($path);

    $htmlFiles = scandir($htmlPath);

	foreach( $files as $file_name ) {

		// 「.」「..」以外のファイルを出力
		if( !preg_match( '/^(\.|\.\.)$/', $file_name) ) {
			// echo $file_name . ', ';
            array_push($list,$file_name);
		}
	}
    
	foreach( $htmlFiles as $file_name ) {

		// 「.」「..」以外のファイルを出力
		if( !preg_match( '/^(\.|\.\.)$/', $file_name) ) {
			// echo $file_name . ', ';
            array_push($htmlList,$file_name);
		}
	}
    // var_dump($list);
} else {
	echo 'ディレクトリの読み込み権限がありません。';
}
?>

<!DOCTYPE html>
<html lang="jp">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>G2-出席確認</title>
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <script src="js/bootstrap.min.js"></script>
</head>
<body>
    <div class="container">
        <h1 class="text-center">出席確認</h1>
    </div>
    <hr>
    <div class="container">
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">日付</th>
                    <th scope="col">出席リスト(.html)</th>
                    <th scope="col">出席リスト(.pdf)</th>
                    <th scope="col">座席表(.pdf)</th>
                <tr>
                    <tbody>
                <?php for($i = 0; $i < count($list); $i++){
                    echo "<tr>";
                    echo "<th>".$list[$i]."</th>\n";
                    $d = "html/".$htmlList[$i];
                    echo "<td><a href=".$d.">出席リスト</a></td>\n";
                    $dl = "pdf/".$list[$i];
                    echo "<td><a href=".$dl.">出席リスト</a></td>\n";
                    // echo "<td><a href=".$dl.">座席表</a></td>\n";
                    echo "<td>座席表</td>\n";
                    echo "</tr>";
                }?>
                    </tbody>
</thead>
    </table>
</div>
</body>
</html>