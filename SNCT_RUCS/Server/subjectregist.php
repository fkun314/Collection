<?php
function h($s)
{
    return htmlspecialchars($s, ENT_QUOTES, 'utf-8');
}
$db = mysqli_connect('localhost', '2021', '2021', 'rucs');
if ($db == FALSE) {
    $text_alert = "<script type='text/javascript'>alert('データベースに接続できませんでした');</script>";
    echo $text_alert;
    echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/index.php';</script>";
    return false;
}
session_start();
$classID = $_SESSION['gradeid'];

if (!$classID) {
    $text_alert = "<script type='text/javascript'>alert('ログインしてください');</script>";
    echo $text_alert;
    echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/index.php';</script>";
    return false;
}

$subjectName = $_POST['subjectName'];
$subjectColor = $_POST['color'];

if (mb_strlen($subjectName) == 0) {
    $text_alert = "<script type='text/javascript'>alert('教科名を空にすることはできません');</script>";
    echo $text_alert;
    echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/index.php';</script>";
    return false;
}
$query = "insert into subjectTable (subjectClassID, subjectName, subjectColor) values ({$classID},'{$subjectName}','{$subjectColor}')";




$result = mysqli_query($db, $query);

if ($result == FALSE) {
    $text_alert = "<script type='text/javascript'>alert('データベースに追加できませんでした');</script>";
    echo $text_alert;
    echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/index.php';</script>";
    return false;
}
echo '<!DOCTYPE html><html lang="jp"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>RUCS</title></head> <link href="./bootstrap/css/bootstrap.min.css" rel="stylesheet" /> <script src="./bootstrap/js/bootstrap.min.js"></script><link rel="icon" href="./favicon.ico" /><style>.container {sans-serif;margin-top: 80px;}a {text-decoration: none;}th {height: 30px;text-align: center;}td {height: 100px;}.today {background: orange !important;}th:nth-of-type(1), td:nth-of-type(1) {color: red;}th:nth-of-type(7), td:nth-of-type(7) {color: blue;}</style></head><body><nav class="navbar navbar-expand-lg navbar-light bg-light"> <div class="container-fluid"> <a class="navbar-brand" href="index.php">RUCS</a> <div class="collapse navbar-collapse" id="navbarSupportedContent"> <ul class="navbar-nav me-auto mb-2 mb-lg-0"> <li class="nav-item"> <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">' . intdiv(h($_SESSION['gradeid']), 10) . "年" . h($_SESSION['gradeid']) % 10 . '組</a> </li> </ul> </div> <a href="logout.php" class="ms-auto link-light" hreflang="ar">ログアウト</a> </div> </nav>';

$text_alert = "<script type='text/javascript'>alert('{$subjectName}を追加しました');</script>";
echo $text_alert;
echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/subjectEdit.php';</script>";
