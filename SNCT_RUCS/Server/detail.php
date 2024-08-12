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

$subjectNumber = array();
$subjectNamae = array();

//教科名取得
$recordSet = mysqli_query($db, "select * from subjectTable where subjectClassID = {$classID}");
while ($data = mysqli_fetch_assoc($recordSet)) {
    array_push($subjectNumber, $data['subjectID']);
    array_push($subjectNamae, $data['subjectName']);
}

if (isset($_GET['ym'])) {
    $ym = $_GET['ym'];
    $subjectID = $_GET['subject'];
    $ym = strtr((string)$ym, '_', '.');
    $recordSet = mysqli_query($db, "select * from Calendar where classID = {$classID} AND originalNumber = '{$ym}'");
    if (isset($_GET['type'])) {
        $type = $_GET['type'];
        if ($type == 1) {
            $recordSet = mysqli_query($db, "delete from bringCalendar where classID = {$classID} AND date = {$ym} AND bringName = '{$_GET['bringName']}'");
        } else if ($type == 2) {
            $recordSet = mysqli_query($db, "delete from bringCalendar where classID = {$classID} AND date = {$ym}");
            $recordSet_Get = mysqli_query($db, "select * from bringTable where classID = {$classID} AND subjectID = {$_GET['subjectID']}");
            if (!$recordSet) {
                printf('');
            } else {
                while ($data = mysqli_fetch_assoc($recordSet_Get)) {
                    $bringName = $data['bringName'];
                    $recordSet = mysqli_query($db, "insert into bringCalendar values('{$ym}',{$classID},{$_GET['subjectID']},'{$data['bringName']}')");
                }
            }
            $recordSet = mysqli_query($db, "update Calendar set subjectID = {$_GET['subjectID']} where classID = {$classID} AND originalNumber = '{$ym}'");
            sleep(0.5);
            $text_alert = "<script type='text/javascript'>alert('教科を変更しました');</script>";
            echo $text_alert;
            echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/index.php';</script>";
        } else if ($type == 3) {
            $recordSet = mysqli_query($db, "insert into bringCalendar values({$ym},{$classID},{$_GET['subjectID']},'{$_GET['bring']}')");
            sleep(0.5);
            $text_alert = "<script type='text/javascript'>alert('持ち物を登録しました');</script>";
            echo $text_alert;
            $time = substr($_GET['ym'], -1);
            echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/detail.php?ym={$_GET['ym']}&subject={$time}';</script>";
        }
    }
}

?>

<!DOCTYPE html>
<html lang="jp">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RUCS</title>
    <script type="text/javascript" src="jquery-3.5.1.min.js"></script>
    <script type="text/javascript" src="jquery.tablesorter.min.js"></script>
    <link href="./bootstrap/css/bootstrap.min.css" rel="stylesheet" />
    <script src="./bootstrap/js/bootstrap.min.js"></script>
    <link rel="icon" href="./favicon.ico" />
</head>

<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid"> <a class="navbar-brand" href="index.php">RUCS</a>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item"> <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true"><?php echo (intdiv(h($_SESSION['gradeid']), 10)); ?>年<?php echo (h($_SESSION['gradeid']) % 10); ?>組 </a> </li>
                </ul>
            </div> <a href="logout.php" class="ms-auto link-light" hreflang="ar">ログアウト</a>
        </div>
    </nav>

    <div class="container">
        <h1><?php
            $recordSet = mysqli_query($db, "select * from subjectTable where subjectClassID = {$classID} and subjectID = {$subjectID}");
            $d = mysqli_fetch_array($recordSet);
            echo $d['subjectName'];
            ?></h1>
        <div class="row">
            <div class="col-6">
                <form action="detail.php">
                    <h2>持ち物登録</h2>
                    <form action="detail.php" method="GET">
                        <input type="hidden" name="ym" value="<?php echo strtr((string)$ym, '.', '_'); ?>">
                        <input type="hidden" name="subjectID" value="<?php echo $subjectID; ?>">
                        <input type="hidden" name="type" value="3">
                        <select name="bring">
                            <?php
                            $recordSet = mysqli_query($db, "select * from bringTable where classID = {$classID} order by subjectID");
                            while ($data = mysqli_fetch_assoc($recordSet)) {
                                $p = array_search($data['subjectID'], $subjectNumber);
                                $Title = $subjectNamae[$p];
                                printf('<option value="' . $data['bringName'] . '">' . $Title . ' : ' . $data['bringName'] . '</option>');
                            }
                            ?>
                        </select>
                        <button class="btn btn-primary" type="submit">追加</button>
                    </form>
                    <p>※新規持ち物登録は<a href="subjectEdit.php">こちら</a>より行ってください。</p>

                    <form action="detail.php">
                        <h2>教科変更：</h2>
                        <input type="hidden" name="ym" value="<?php echo strtr((string)$ym, '.', '_'); ?>">
                        <input type="hidden" name="subject" value="<?php echo $subjectID; ?>">
                        <input type="hidden" name="type" value="2">
                        <select name="subjectID">
                            <?php
                            $recordSet = mysqli_query($db, "select * from subjectTable where subjectClassID = {$classID}");

                            while ($data = mysqli_fetch_assoc($recordSet)) {
                                if ($data['subjectID'] == $subjectID) {
                                    printf('<option value="%d" selected>%s</option>', $data['subjectID'], $data['subjectName']);
                                } else {
                                    printf('<option value="%d">%s</option>', $data['subjectID'], $data['subjectName']);
                                }
                            }
                            ?>
                        </select>
                        <button class="btn btn-primary" type="submit">保存</button>
                    </form>
                    <p>※新規教科登録は<a href="subjectRegister.php">こちら</a>より行ってください。</p>
            </div>
            <div class="col-6">
                <div class="card">
                    <div class="card-header">
                        <h4 class="card-title">日付：<?php echo substr($ym, 0, 4) . "年" . substr($ym, 4, 2) . "月" . substr($ym, 6, 2) . "日"; ?></h4>
                        <h4 class="card-title">コマ数：<?php echo substr($ym, 9); ?>校時</h4>
                    </div>
                    <div class="card-body">
                        <h4 for="firstName" class="form-label">教科：
                            <?php
                            $recordSet = mysqli_query($db, "select * from subjectTable where subjectClassID = {$classID} and subjectID = {$subjectID}");
                            $d = mysqli_fetch_array($recordSet);
                            echo $d['subjectName'];
                            ?>
                        </h4>
                        <p class="m-0">
                        <h5 for="firstName" class="form-label">持ち物：</h5>
                        </p>
                        <ul class="list-group">
                            <?php
                            $recordSet = mysqli_query($db, "select * from bringCalendar where classID = {$classID} and date = {$ym}");
                            while ($data = mysqli_fetch_assoc($recordSet)) {
                                printf('<li class="list-group-item">%s　　　<a href="detail.php?ym=' . $ym . '&subject=' . $subjectID . '&type=1&bringName=' . $data['bringName'] . '">削除</a></li>', $data['bringName']);
                            }
                            ?>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>

</html>