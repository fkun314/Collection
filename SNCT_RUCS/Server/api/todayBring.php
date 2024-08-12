<?php
$classID = $_GET['classID'];

$db = mysqli_connect('localhost', '2021', '2021', 'rucs');
if ($db == FALSE) {
    exit('データベースに接続できませんでした。');
}

date_default_timezone_set('Asia/Tokyo');
$date = date('Y-m-d');

if (!isset($_GET['date'])) {
    if (date("Y-m-d", strtotime('+12 hour')) == date('Y-m-d')) {
        $date = date('Y-m-d');
    } else {
        $date = date("Y-m-d", strtotime('+12 hour'));
    }
} else {
    $date = $_GET['date'];
}



$output = array();
$subject = array();
$color = array();
$subjectNumber = array();
$subjectNamae = array();

$recordSet = mysqli_query($db, "select * from subjectTable where subjectClassID = {$classID}");
while ($data = mysqli_fetch_assoc($recordSet)) {
    array_push($subjectNumber, $data['subjectID']);
    array_push($subjectNamae, $data['subjectName']);
}

$output += array("date" => $date);
$output += array("class" => $classID);

for ($k = 1; $k < 7; $k++) {
    $subTitle = "";
    $Title = "";
    $searchDay = str_replace("-", "", $date) + ($k / 10);
    $recordSet2 = mysqli_query($db, "select * from Calendar where classID = {$classID} AND originalNumber = '{$searchDay}'");
    $recordData2 = mysqli_fetch_assoc($recordSet2);
    if ($recordData2['subjectID']) {
        $subTitle = $recordData2['subjectID'];
        $p = array_search($subTitle, $subjectNumber);
        $Title = $subjectNamae[$p];
    }
    $recordSet = mysqli_query($db, "select * from bringCalendar where classID = {$classID} AND Date = {$searchDay}");
    $i = 0;
    $bring = array();
    while ($data = mysqli_fetch_assoc($recordSet)) {
        $i++;
        if ($data['bringName']) {
            $bring += array($i => $data['bringName']);
        }
    }
    if($i == 0){
        $i = 1;
        $bring += array($i => "なし");
    }
    $output += array($k => array("title" => $Title, "bring" => $bring));
}

$outoutJson = json_encode($output, JSON_UNESCAPED_UNICODE);

echo $outoutJson;
