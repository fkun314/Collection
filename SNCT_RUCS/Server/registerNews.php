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
$message = $_POST['message'];
$now = new DateTime();
$datetime = $now->format('Y-m-d H:i:s');

$query = "replace into news (classID, date, message) values ({$classID},'{$datetime}','{$message}')";

$result = mysqli_query($db, $query);

if ($result == FALSE) {
    $text_alert = "<script type='text/javascript'>alert('データベースに追加できませんでした');</script>";
    echo $text_alert;
    echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/index.php';</script>";
    return false;
}

sleep(0.5);
$text_alert = "<script type='text/javascript'>alert('お知らせを更新しました');</script>";
echo $text_alert;
echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/index.php';</script>";

?>