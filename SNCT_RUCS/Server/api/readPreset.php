<?php
$classID = $_GET['classID'];

$db = mysqli_connect('localhost', '2021', '2021', 'rucs');
if ($db == FALSE) {
    exit('データベースに接続できませんでした。');
}

$output = array();
$subject = array();
$preset = array();
$presetList = array();
$subjectColor = array();
$subjectNumber = array();
$subjectNamae = array();

$recordSet = mysqli_query($db, "select * from subjectTable where subjectClassID = {$classID}");
while ($data = mysqli_fetch_assoc($recordSet)) {
    array_push($subjectNumber, $data['subjectID']);
    array_push($subjectNamae, $data['subjectName']);
    array_push($subjectColor, $data['subjectColor']);
}

$recordPresetNumber = mysqli_query($db, "select * from mainPreset where classID = {$classID}");
$recordData = mysqli_fetch_assoc($recordPresetNumber);
$presetNumber = $recordData['presetNumber'];

$recordSet = mysqli_query($db, "select * from presetData where presetNumber = {$presetNumber}");
$recordData = mysqli_fetch_assoc($recordSet);
$presetList = [
$recordData['preset11'], $recordData['preset12'], $recordData['preset13'], $recordData['preset14'], $recordData['preset15'], $recordData['preset16'], $recordData['preset21'], $recordData['preset22'], $recordData['preset23'], $recordData['preset24'], $recordData['preset25'], $recordData['preset26'], $recordData['preset31'], $recordData['preset32'], $recordData['preset33'], $recordData['preset34'], $recordData['preset35'], $recordData['preset36'], $recordData['preset41'], $recordData['preset42'], $recordData['preset43'], $recordData['preset44'], $recordData['preset45'], $recordData['preset46'], $recordData['preset51'], $recordData['preset52'], $recordData['preset53'], $recordData['preset54'], $recordData['preset55'], $recordData['preset56']
];

$output += array("class" => $classID);
$output += array("preserID" => $presetNumber);

for ($k = 1; $k <= 30; $k++) {
    $subTitle = "";
    $Title = "";
    if($presetList[$k-1] != ""){
        $subTitle = $presetList[$k-1];
        $p = array_search($subTitle, $subjectNumber);
        $Title = $subjectNamae[$p];
        $color = $subjectColor[$p];
    }
    else{
        $color = "#FFFFFF";
    }
    $preset += array($k => array("subject" =>$Title,"color" => $color));
}

$output += array("preset" => $preset);

$outoutJson = json_encode($output, JSON_UNESCAPED_UNICODE);

echo $outoutJson;
