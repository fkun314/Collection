<?php
$classID = $_GET['classID'];

$db = mysqli_connect('localhost', '2021', '2021', 'rucs');
if ($db == FALSE) {
    exit('データベースに接続できませんでした。');
}

if (isset($classID)) {
    $recordSet = mysqli_query($db, "select * from subjectTable where subjectClassID = {$classID}");
} else {
    $recordSet = mysqli_query($db, 'select * from subjectTable');
}


$output = array();
$i = 0;

while ($data = mysqli_fetch_assoc($recordSet)) {
    $i++;
    $output += array($i => array("classID" => $data['subjectClassID'], "subjectID" => $data['subjectID'], "name" => $data['subjectName'], 'subjectColor' => $data['subjectColor']));
}

$outoutJson = json_encode($output, JSON_UNESCAPED_UNICODE);

echo $outoutJson;
