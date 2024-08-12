<?php
$left = [];
$right = [];
$leftlist = "";
$rightlist = "";
$anserlist ="";

$count = 0;
//九九81問
for ($i = 1; $i <= 9; $i++) {
    for ($j = 1; $j <= 9; $j++) {
        $left[$count] = $i;
        $right[$count] = $j;
        $ans[$count] = $i * $j;
        $count++;
    }
}

$count -= 1;
$lenght = $count;
for ($i = 0; $i < 1000; $i++) {
    $shuff = random_int(0, $lenght);
    do {
        $shuff2 = random_int(5, $lenght);
    } while ($shuff2 == $shuff);
    // var_dump($left);
    $k_left = $left[$shuff];
    $k_right = $right[$shuff];
    $k_ans = $ans[$shuff];
    $left[$shuff] = $left[$shuff2];
    // var_dump($left);
    $right[$shuff] = $right[$shuff2];
    $ans[$shuff] = $ans[$shuff2];
    $left[$shuff2] = $k_left;
    $right[$shuff2] = $k_right;
    $ans[$shuff2] = $k_ans;
    // var_dump($left);
}

for ($i = 0; $i < 50; $i++) {
    $siki[$i] = $left[$i] . "×" . $right[$i] . "=";
    $ans = $left[$i]*$right[$i];
    $per = $ans.',';
    $leftlist.= $left[$i].',';
    $rightlist.= $right[$i].',';
    $anserlist.=$per;
}
require('../tfpdf/tfpdf.php');
$pdf = new tFPDF;
$pdf->SetMargins(20, 11); //左マージン、トップマージン、（右マージンは左に同じ）
$pdf->AddPage();
$pdf->AddFont('ShipporiMincho', '', 'ShipporiMincho-TTF-Regular.ttf', true);
$pdf->SetFont('ShipporiMincho', '', 40);
// -$pdf->Cell(40,10,'Hello World!');
$pdf->SetFontSize(20); //フォントサイズ変更。
$pdf->Cell(90, 20, '次のもんだいに答えましょう');
$pdf->Ln(20);
$pdf->SetFontSize(20); //フォントサイズ変更。
// $siki 配列の長さを取得
$siki_length = count($siki);

for ($i = 0; $i < $siki_length; $i += 3) {
    $pdf->Cell(60, 20,"(". ($i + 1) . ")  " . $siki[$i]);
    $pdf->Cell(60, 20, "(". ($i + 2) .  ")  " . $siki[$i + 1]);
    
    // $i + 2 が配列の範囲内であるか確認
    if ($i + 2 < $siki_length) {
        $pdf->Cell(0, 20, "(". ($i + 3) . ")  " . $siki[$i + 2]);
    }
    
    $pdf->Ln(14);
}

include 'config.php';
$mysqli = new mysqli( $network, $name, $password, $dbname);

if( $mysqli->connect_errno ) {
	echo $mysqli->connect_errno . ' : ' . $mysqli->connect_error;
}

$mysqli->set_charset('utf8');

// 現在の日付を取得
$date = date('Y-m-d H:i:s');

// SELECT文を変数に格納
$sql = "SELECT * FROM elementanswerlist";
 
// SQLステートメントを実行し、結果を変数に格納
$stmt = $mysqli->query($sql);
 $allid = array();
 $i = 0;
// foreach文で配列の中身を一行ずつ出力
foreach ($stmt as $row) {
    $i++;
  array_push($allid,$row['Id']);
}
$Id = $i+1;

// INSERT
$sql = "INSERT INTO elementanswerlist(
	Date, Id, leftnumber, rightnumber, Answer, type_id
) VALUES (
	'$date', '$Id' , '$leftlist','$rightlist','$anserlist','5005'
)";
$res = $mysqli->query($sql);

$mysqli->close();
$pdf->Ln(2);
$pdf->SetFontSize(8); //フォントサイズ変更。
$pdf->Image('img/answer.jpg', 190, 275, 12, 12);
$pdf->Cell(0, 1,'                                                                                                                                 答えは下記のリンクまたはQRコードをご利用ください ID→ '.$Id);
$pdf->Ln(4);
$link = 'https://mochi314.cloudfree.jp/answer.php?id='.strval($Id);
$pdf->Cell(0, 1,'                                                                                                                                  '."$link");
$pdf->Output();