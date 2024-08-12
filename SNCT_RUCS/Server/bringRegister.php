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

$subjectID = $_POST['subjectID'];
$bring = $_POST['bring'];
$kisonClassID = array();
$kisonSubjectID = array();
$kisonName = array();
$recordSet = mysqli_query($db, "select * from bringTable where classID = {$classID}");
if ($recordSet) {
    while ($data = mysqli_fetch_assoc($recordSet)) {
        array_push($kisonName, $data['bringName']);
        if ($data['bringName'] == $bring) {
            if ($data['subjectID'] == $subjectID) {
                $text_alert = "<script type='text/javascript'>alert('既に登録されています');</script>";
                echo $text_alert;
                echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/subjectEdit.php';</script>";
            }
        }
    }
}

$returnName = array_search($kisonName, $bring);
$query = "insert into bringTable (subjectID, classID, bringName) values ('{$subjectID}','{$classID}','{$bring}')";
$result = mysqli_query($db, $query);

if ($result == FALSE) {
    $text_alert = "<script type='text/javascript'>alert('データベースに追加できませんでした');</script>";
    echo $text_alert;
    echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/index.php';</script>";
    return false;
}

$text_alert = "<script type='text/javascript'>alert('{$bring}を追加しました');</script>";
echo $text_alert;
echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/subjectEdit.php';</script>";
