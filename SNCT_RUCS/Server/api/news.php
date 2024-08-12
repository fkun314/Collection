<?php
$classID = $_GET['classID'];

function h($s)
{
    return htmlspecialchars($s, ENT_QUOTES, 'utf-8');
}
$db = mysqli_connect('localhost', '2021', '2021', 'rucs');
if ($db == FALSE) {
    exit('データベースに接続できませんでした。');
}

if(isset($classID)){
    $recordSet = mysqli_query($db, "select * from news where classID = {$classID}");
}else{
    exit("Required parameters are missing.");
}


$data = mysqli_fetch_assoc($recordSet);

$output = array();

if($data['date']){
    $output += array("classID" => $classID);
    $output += array("date" => $data['date']);
    $output += array("message" => $data['message']);
    $outoutJson = json_encode($output, JSON_UNESCAPED_UNICODE);

    echo $outoutJson;
}else{
    echo "Empty Data";
}
