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
$query = "INSERT INTO presetData(classID, presetName, preset11, preset12, preset13, preset14, preset15, preset16, preset21, preset22, preset23, preset24, preset25, preset26, preset31, preset32, preset33, preset34, preset35, preset36, preset41, preset42, preset43, preset44, preset45, preset46, preset51, preset52, preset53, preset54, preset55, preset56) VALUES ({$classID},'{$_POST['nm']}',{$_POST['11']},{$_POST['12']},{$_POST['13']},{$_POST['14']},{$_POST['15']},{$_POST['16']},{$_POST['21']},{$_POST['22']},{$_POST['23']},{$_POST['24']},{$_POST['25']},{$_POST['26']},{$_POST['31']},{$_POST['32']},{$_POST['33']},{$_POST['34']},{$_POST['35']},{$_POST['36']},{$_POST['41']},{$_POST['42']},{$_POST['43']},{$_POST['44']},{$_POST['45']},{$_POST['46']},{$_POST['51']},{$_POST['52']},{$_POST['53']},{$_POST['54']},{$_POST['55']},{$_POST['56']})";

$result = mysqli_query($db, $query);

if ($result == FALSE) {
    $text_alert = "<script type='text/javascript'>alert('データベースに追加できませんでした');</script>";
    echo $text_alert;
    echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/index.php';</script>";
    return false;
}
sleep(0.5);
$text_alert = "<script type='text/javascript'>alert('{$_POST['nm']}を変更しました');</script>";
echo $text_alert;
echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/index.php';</script>";
