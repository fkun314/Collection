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
    $text_alert = "<script type='text/javascript'>alert('ログインしてくださいた');</script>";
    echo $text_alert;
    echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/index.php';</script>";
    return false;
}

$presetID = $_POST['presetID'];

$query = "replace into mainPreset values ($classID, $presetID)";

$result = mysqli_query($db, $query);

if ($result == FALSE) {
    $text_alert = "<script type='text/javascript'>alert('データベースに追加できませんでした');</script>";
    echo $text_alert;
    echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/index.php';</script>";
    return false;
}
$text_alert = "<script type='text/javascript'>alert('メインの時間割を変更しました');</script>";
echo $text_alert;
echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/index.php';</script>";
return false;
