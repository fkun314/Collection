<?php
$left = [];
$right = [];
$leftlist = "";
$rightlist = "";
$anserlist = "";
$max = 10;
$le = [];
$ri = [];
for ($i = 0; $i < 10; $i++) {
    do{
    $le[$i] = random_int(-10,10);
    }while($le[$i]==0);
    do{
    do{
        $ri[$i] = random_int(-10,10);
    }while($le[$i] == $ri[$i]);
}while($ri[$i] == 0);
    $per = '' . ',';
    $leftlist .= $le[$i] . ',';
    $rightlist .= $ri[$i] . ',';
    $anserlist .= $per;
}
require('../tfpdf/tfpdf.php');
$pdf = new tFPDF;
$pdf->SetMargins(20, 11); //左マージン、トップマージン、（右マージンは左に同じ）
$pdf->AddPage();
$pdf->AddFont('ShipporiMincho', '', 'ShipporiMincho-TTF-Regular.ttf', true);
$pdf->SetFont('ShipporiMincho', '', 40);
$pdf->SetFontSize(20); //フォントサイズ変更。
$pdf->Cell(90, 20, '次の式を展開してください');
$pdf->Ln(20);
$pdf->SetFontSize(22); //フォントサイズ変更。
for ($i = 0; $i < 10; $i += 1) {
    if($le[$i] >= 0){$lef = "+".$le[$i];}else{$lef = $le[$i];}
    if($ri[$i] >= 0){$rig = "+".$ri[$i];}else{$rig = $ri[$i];}
    $pdf->Cell(90, 30, "(". ($i + 1) . ")  " ."(x".$lef.")(x".$rig.")");
    $pdf->Ln(23);
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
// $Id = $allid[count($allid)-1] + 1;

// INSERT
$sql = "INSERT INTO elementanswerlist(
	Date, Id, leftnumber, rightnumber, Answer, type_id
) VALUES (
	'$date', '$Id' , '$leftlist','$rightlist','$anserlist','1012'
)";
$res = $mysqli->query($sql);

$mysqli->close();
$pdf->Ln(8);
$pdf->SetFontSize(9); //フォントサイズ変更。
$pdf->Image('img/answer.jpg', 190, 275, 12, 12);
$pdf->Cell(0, 1,'                                                                                                           答えは下記のリンクまたはQRコードをご利用ください ID→ '.$Id);
$pdf->Ln(5);
$link = 'https://mochi314.cloudfree.jp/answer.php?id='.strval($Id);
$pdf->Cell(0, 1,'                                                                                                                              '."$link");
$pdf->Output();