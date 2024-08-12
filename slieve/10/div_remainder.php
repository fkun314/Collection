<?php
$left = [];
$right = [];
$leftlist = "";
$rightlist = "";
$anserlist ="";

$count = 0;
//割り切れない割り算316問
for ($i = 1; $i <= 81; $i++) {
    for ($j = 1; $j <= 9; $j++) {
        if ($i % $j != 0 && $i / $j < 10 && $i / $j >= 1) {
            $left[$count] = $i;
            $right[$count] = $j;
            $ans[$count] = intdiv($i,$j);
            $amr[$count] = $i % $j;
            $count++;
        }
    }
}

$count -= 1;
$lenght = $count;
for ($i = 0; $i < 1000; $i++) {
    $shuff = random_int(0, $lenght);
    do {
        $shuff2 = random_int(5, $lenght);
    } while ($shuff2 == $shuff);
    $k_left = $left[$shuff];
    $k_right = $right[$shuff];
    $k_ans = $ans[$shuff];
    //下一行は割り算あまりありのみ
    $k_amr = $amr[$shuff];
    $left[$shuff] = $left[$shuff2];
    $right[$shuff] = $right[$shuff2];
    $ans[$shuff] = $ans[$shuff2];
    //下一行は割り算あまりありのみ
    $amr[$shuff] = $amr[$shuff2];
    $left[$shuff2] = $k_left;
    $right[$shuff2] = $k_right;
    $ans[$shuff2] = $k_ans;
    //下一行は割り算あまりありのみ
    $amr[$shuff2] = $k_amr;
}

for ($i = 0; $i < 10; $i++) {
    $siki[$i] = $left[$i] . "÷" . $right[$i] . "=";
    $ans = intdiv($left[$i],$right[$i]);
    $amr = $left[$i]%$right[$i];
    $per = $ans.'あまり'.$amr.',';
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
$pdf->SetFontSize(20); //フォントサイズ変更。
$pdf->Cell(90, 20, '次の問題に答えましょう');
$pdf->Ln(20);
$pdf->SetFontSize(30); //フォントサイズ変更。
for ($i = 0; $i < 10; $i += 1) {
    $pdf->Cell(90, 30, "(". ($i + 1) . ")  " .$siki[$i]);
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

// INSERT
$sql = "INSERT INTO elementanswerlist(
	Date, Id, leftnumber, rightnumber, Answer, type_id
) VALUES (
	'$date', '$Id' , '$leftlist','$rightlist','$anserlist','1007'
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