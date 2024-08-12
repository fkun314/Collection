<?php
$classID = $_GET['classID'];

$db = mysqli_connect('localhost', '2021', '2021', 'rucs');
if ($db == FALSE) {
    exit('データベースに接続できませんでした。');
}

if (isset($classID)) {
    $recordSet = mysqli_query($db, "select * from bringTable where classID = {$classID} order by subjectID");
} else {
    $recordSet = mysqli_query($db, 'select * from bringTable');
}


$output = array();
$subject = array();
$color = array();

if (isset($classID)) {
    $recordSetSubject = mysqli_query($db, "select * from subjectTable where subjectClassID = {$classID}");
} else {
    $recordSetSubject = mysqli_query($db, 'select * from subjectTable');
}


$i = 0;

while ($data = mysqli_fetch_assoc($recordSetSubject)) {
    $i++;
    $subject += array($i => array($data['subjectClassID'] . $data['subjectID'] => $data['subjectName']));
    $color += array($i => array($data['subjectClassID'] . $data['subjectID'] => $data['subjectColor']));
}

$j = 0;
while ($data = mysqli_fetch_assoc($recordSet)) {
    $j++;
    $results = array_column($subject, $data['classID'] . $data['subjectID']);
    $results_color = array_column($color, $data['classID'] . $data['subjectID']);
    $output += array($j => array("classID" => $data['classID'], "subjectID" => $data['subjectID'], "color" => $results_color[0], "bringID" => $data['bringID'], "subjectName" => $results[0], "name" => $data['bringName']));
}

$outoutJson = json_encode($output, JSON_UNESCAPED_UNICODE);

echo $outoutJson;
