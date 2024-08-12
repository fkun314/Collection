<?php
require('./tfpdf/tfpdf.php');
$getid = $_GET['id'];
// echo $getid;
//データベースへ接続
$dsn = "mysql:dbname=mochi314_element;host=localhost;charset=utf8mb4";
$username = "mochi314_mochi";
$password = "Askr0625";
$options = [];
$pdo = new PDO($dsn, $username, $password, $options);
$stmt = $pdo->query("SELECT * FROM elementanswerlist WHERE Id='" . $getid . "'");
$pdo = null;
// var_dump($stmt);
$long_ans = "";
$long_left = "";
$long_right = "";
$type_id = 0;
foreach ($stmt as $row) :
    $long_left = $row[2];
    $long_right = $row[3];
    $long_ans = $row[4];
    $type_id = $row[5];
endforeach;
if ($type_id == 2012) {
    $ex_right = explode(",", $long_right);
    $ex_left = explode(",", $long_left);
    for ($i = 0; $i < 20; $i++) {
        $j1 = $ex_left[$i] + $ex_right[$i];
        $j0 = $ex_left[$i] * $ex_right[$i];
        if ($j1 >= 0) {
            $j1 = "+" . $j1;
        }
        if ($j0 >= 0) {
            $j0 = "+" . $j0;
        }
        $ex_ans[$i] = "x²" . $j1 . "x" . $j0;
        if ($ex_left[$i] >= 0) {
            $ex_left[$i] = "+" . $ex_left[$i];
        }
        if ($ex_right[$i] >= 0) {
            $ex_right[$i] = "+" . $ex_right[$i];
        }
        // "(x".$lef.")(x".$rig.")" <=siki[$i]
    }
} else if ($type_id == 2013) {
    $ex_right = explode(",", $long_right);
    $ex_left = explode(",", $long_left);
    for ($i = 0; $i < 20; $i++) {
        $ex_ans[$i] = "x= " . ($ex_left[$i]) . ",x= " . ($ex_right[$i]);
    }
} else if ($type_id == 1012) {
    $ex_right = explode(",", $long_right);
    $ex_left = explode(",", $long_left);
    for ($i = 0; $i < 10; $i++) {
        $j1 = $ex_left[$i] + $ex_right[$i];
        $j0 = $ex_left[$i] * $ex_right[$i];
        if ($j1 >= 0) {
            $j1 = "+" . $j1;
        }
        if ($j0 >= 0) {
            $j0 = "+" . $j0;
        }
        $ex_ans[$i] = "x²" . $j1 . "x" . $j0;
        if ($ex_left[$i] >= 0) {
            $ex_left[$i] = "+" . $ex_left[$i];
        }
        if ($ex_right[$i] >= 0) {
            $ex_right[$i] = "+" . $ex_right[$i];
        }
        // "(x".$lef.")(x".$rig.")" <=siki[$i]
    }
} else if ($type_id == 1013) {
    $ex_right = explode(",", $long_right);
    $ex_left = explode(",", $long_left);
    for ($i = 0; $i < 10; $i++) {
        $ex_ans[$i] = "x= " . ($ex_left[$i]) . ",x= " . ($ex_right[$i]);
    }
} else if ($type_id == 5012) {
    $ex_right = explode(",", $long_right);
    $ex_left = explode(",", $long_left);
    for ($i = 0; $i < 50; $i++) {
        $j1 = $ex_left[$i] + $ex_right[$i];
        $j0 = $ex_left[$i] * $ex_right[$i];
        if ($j1 >= 0) {
            $j1 = "+" . $j1;
        }
        if ($j0 >= 0) {
            $j0 = "+" . $j0;
        }
        $ex_ans[$i] = "x²" . $j1 . "x" . $j0;
        if ($ex_left[$i] >= 0) {
            $ex_left[$i] = "+" . $ex_left[$i];
        }
        if ($ex_right[$i] >= 0) {
            $ex_right[$i] = "+" . $ex_right[$i];
        }
        // "(x".$lef.")(x".$rig.")" <=siki[$i]
    }
} else if ($type_id == 5013) {
    $ex_right = explode(",", $long_right);
    $ex_left = explode(",", $long_left);
    for ($i = 0; $i < 50; $i++) {
        $ex_ans[$i] = "x= " . ($ex_left[$i]) . ",x= " . ($ex_right[$i]);
    }
} else {
    $ex_ans = explode(",", $long_ans);
    $ex_left = explode(",", $long_left);
    $ex_right = explode(",", $long_right);
}

switch ($type_id) {
    case '5001':
    case '5002':
    case '5008':
    case '5009':
        for ($i = 0; $i < 50; $i++) {
            $siki[$i] = $ex_left[$i] . "+" . $ex_right[$i] . "=" . $ex_ans[$i];
        }
        break;
    case '5003':
    case '5004':
    case '5010':
    case '5011':
        for ($i = 0; $i < 50; $i++) {
            $siki[$i] = $ex_left[$i] . "-" . $ex_right[$i] . "=" . $ex_ans[$i];
        }
        break;
    case '5005':
        for ($i = 0; $i < 50; $i++) {
            $siki[$i] = $ex_left[$i] . "×" . $ex_right[$i] . "=" . $ex_ans[$i];
        }
        break;
    case '5006':
    case '5007':
        for ($i = 0; $i < 50; $i++) {
            $siki[$i] = $ex_left[$i] . "÷" . $ex_right[$i] . "=" . $ex_ans[$i];
        }
        break;
    case '2001':
    case '2002':
    case '2008':
    case '2009':
        for ($i = 0; $i < 20; $i++) {
            $siki[$i] = $ex_left[$i] . "+" . $ex_right[$i] . "=" . $ex_ans[$i];
        }
        break;
    case '2003':
    case '2004':
    case '2010':
    case '2011':
        for ($i = 0; $i < 20; $i++) {
            $siki[$i] = $ex_left[$i] . "-" . $ex_right[$i] . "=" . $ex_ans[$i];
        }
        break;
    case '2005':
        for ($i = 0; $i < 20; $i++) {
            $siki[$i] = $ex_left[$i] . "×" . $ex_right[$i] . "=" . $ex_ans[$i];
        }
        break;
    case '2006':
    case '2007':
        for ($i = 0; $i < 20; $i++) {
            $siki[$i] = $ex_left[$i] . "÷" . $ex_right[$i] . "=" . $ex_ans[$i];
        }
        break;
    case '1001':
    case '1002':
    case '1008':
    case '1009':
        for ($i = 0; $i < 10; $i++) {
            $siki[$i] = $ex_left[$i] . "+" . $ex_right[$i] . "=" . $ex_ans[$i];
        }
        break;
    case '1003':
    case '1004':
    case '1010':
    case '1011':
        for ($i = 0; $i < 10; $i++) {
            $siki[$i] = $ex_left[$i] . "-" . $ex_right[$i] . "=" . $ex_ans[$i];
        }
        break;
    case '1005':
        for ($i = 0; $i < 10; $i++) {
            $siki[$i] = $ex_left[$i] . "×" . $ex_right[$i] . "=" . $ex_ans[$i];
        }
        break;
    case '1006':
    case '1007':
        for ($i = 0; $i < 10; $i++) {
            $siki[$i] = $ex_left[$i] . "÷" . $ex_right[$i] . "=" . $ex_ans[$i];
        }
        break;
    case '1012':
        for ($i = 0; $i < 10; $i++) {
            $siki[$i] = "(x" . $ex_left[$i] . ")(x" . $ex_right[$i] . ")";
        }
        break;
    case '1013':
        for ($i = 0; $i < 10; $i++) {
            $j1 = $ex_left[$i] + $ex_right[$i];
            $j0 = $ex_left[$i] * $ex_right[$i];
            if ($j1 >= 0) {
                $j1 = "+" . $j1;
            }
            if ($j0 >= 0) {
                $j0 = "+" . $j0;
            }
            if ($j1 != 0) {
                $siki[$i] = "x²" . $j1 . "x" . $j0;
            } else {
                $siki[$i] = "x²" . $j0;
            }
        }
        break;
    case '2012':
        for ($i = 0; $i < 20; $i++) {
            $siki[$i] = "(x" . $ex_left[$i] . ")(x" . $ex_right[$i] . ")";
        }
        break;
    case '2013':
        for ($i = 0; $i < 20; $i++) {
            $j1 = $ex_left[$i] + $ex_right[$i];
            $j0 = $ex_left[$i] * $ex_right[$i];
            if ($j1 >= 0) {
                $j1 = "+" . $j1;
            }
            if ($j0 >= 0) {
                $j0 = "+" . $j0;
            }
            if ($j1 != 0) {
                $siki[$i] = "x²" . $j1 . "x" . $j0;
            } else {
                $siki[$i] = "x²" . $j0;
            }
        }
        break;
    case '5012':
        for ($i = 0; $i < 50; $i++) {
            $siki[$i] = "(x" . $ex_left[$i] . ")(x" . $ex_right[$i] . ")";
        }
        break;
    case '5013':
        for ($i = 0; $i < 50; $i++) {
            $j1 = $ex_left[$i] + $ex_right[$i];
            $j0 = $ex_left[$i] * $ex_right[$i];
            if ($j1 >= 0) {
                $j1 = "+" . $j1;
            }
            if ($j0 >= 0) {
                $j0 = "+" . $j0;
            }
            if ($j1 != 0) {
                $siki[$i] = "x²" . $j1 . "x" . $j0;
            } else {
                $siki[$i] = "x²" . $j0;
            }
        }
        break;
    default:
        # code...
        break;
}


$pdf = new tFPDF();
$pdf->SetMargins(20, 11); //左マージン、トップマージン、（右マージンは左に同じ）
$pdf->AddPage();
$pdf->AddFont('ShipporiMincho', '', 'ShipporiMincho-TTF-Regular.ttf', true);
$pdf->SetFont('ShipporiMincho', '', 40);
if (!$siki[0]) {
    $pdf->SetFontSize(20); //フォントサイズ変更。
    $pdf->Cell(60, 20, '入力されたIDの問題はまだ発行されていません');
} else {
    $pdf->SetFontSize(20); //フォントサイズ変更。
    $pdf->Cell(140, 10, '答え');
    $pdf->SetFontSize(14); //フォントサイズ変更。
    $pdf->Cell(10, 10, 'Id → ' . $getid);
    $pdf->Ln(10);
    switch ($type_id) {
        case '5001':
        case '5002':
        case '5003':
        case '5004':
        case '5005':
        case '5006':

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
            break;
        case '5008':
        case '5010':
            $pdf->SetFontSize(17); //フォントサイズ変更。
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
            break;
        case '5009':
        case '5011':
            $pdf->SetFontSize(14); //フォントサイズ変更。
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
            break;
        case '5007':
            $pdf->SetFontSize(16); //フォントサイズ変更。
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
            break;
        case '5012':
        case '5013':
            for ($i = 0; $i < (count($ex_left) - 1); $i += 3) {
                $pdf->SetFontSize(14);
                $pdf->Cell(60, 20, "(" . ($i + 1) . ")  " . $siki[$i]);
                $pdf->Cell(60, 20, "(" . ($i + 2) .  ")  " . $siki[$i + 1]);
                if(($i + 3) != 51){
                    $pdf->Cell(0, 20, "(" . ($i + 3) .  ")  " . $siki[$i + 2]);
                }
                $pdf->Ln(7);
                $pdf->SetFontSize(12);
                $pdf->Cell(60, 20, "          " . $ex_ans[$i]);
                $pdf->Cell(60, 20, "          " . $ex_ans[$i + 1]);
                if(($i + 3) != 51){
                    $pdf->Cell(0, 20, "          " . $ex_ans[$i + 2]);
                }
                $pdf->Ln(7);
            }
            break;
        case '2001':
        case '2002':
        case '2003':
        case '2004':
        case '2005':
        case '2007':
        case '2006':
        case '2007':
        case '2008':
        case '2009':
        case '2010':
        case '2011':
            $pdf->SetFontSize(25); //フォントサイズ変更。
            for ($i = 0; $i < (count($ex_left) - 1); $i += 2) {
                $pdf->Cell(90, 30, "(" . ($i + 1) . ")  " . $siki[$i]);
                $pdf->Cell(0, 30, "(" . ($i + 2) .  ")  " . $siki[$i + 1]);
                $pdf->Ln(23);
            }
            break;
        case '2012':
        case '2013':
            for ($i = 0; $i < (count($ex_left) - 1); $i += 2) {
                $pdf->SetFontSize(22);
                $pdf->Cell(90, 30, "(" . ($i + 1) . ")  " . $siki[$i]);
                $pdf->Cell(0, 30, "(" . ($i + 2) .  ")  " . $siki[$i + 1]);
                $pdf->Ln(11);
                $pdf->SetFontSize(20);
                $pdf->Cell(90, 30, "          " . $ex_ans[$i]);
                $pdf->Cell(0, 30, "          " . $ex_ans[$i + 1]);
                $pdf->Ln(12);
            }
            break;
        case '1001':
        case '1002':
        case '1003':
        case '1004':
        case '1005':
        case '1006':
        case '1007':
            $pdf->SetFontSize(30); //フォントサイズ変更。
            for ($i = 0; $i < (count($ex_left) - 1); $i += 1) {
                $pdf->Cell(90, 30, "(" . ($i + 1) . ")  " . $siki[$i]);
                $pdf->Ln(23);
            }
            break;
        case '1008':
        case '1009':
        case '1010':
        case '1011':
            $pdf->SetFontSize(25); //フォントサイズ変更。
            for ($i = 0; $i < (count($ex_left) - 1); $i += 1) {
                $pdf->Cell(90, 30, "(" . ($i + 1) . ")  " . $siki[$i]);
                $pdf->Ln(23);
            }
            break;
        case '1012':
        case '1013':
            for ($i = 0; $i < (count($ex_left) - 1); $i += 1) {
                $pdf->SetFontSize(22);
                $pdf->Cell(90, 30, "(" . ($i + 1) . ")  " . $siki[$i]);
                $pdf->Ln(11);
                $pdf->SetFontSize(20);
                $pdf->Cell(90, 30, "          " . $ex_ans[$i]);
                $pdf->Ln(12);
            }
            break;
    }
}
$pdf->Output();
