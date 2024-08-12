<?php
function h($s)
{
  return htmlspecialchars($s, ENT_QUOTES, 'utf-8');
}

$db = mysqli_connect('localhost', '2021', '2021', "rucs");
if ($db == FALSE) {
  $text_alert = "<script type='text/javascript'>alert('データベースに接続できませんでした');</script>";
  echo $text_alert;
  echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/index.php';</script>";
  return false;
}
mysqli_set_charset($db, 'utf8');
session_start();
$classID = $_SESSION['gradeid'];
date_default_timezone_set('Asia/Tokyo');

if (isset($_GET['ym'])) {
  $ym = $_GET['ym'];
} else {
  $ym = date('Y-m');
}

$timestamp = strtotime($ym . '-01');
if ($timestamp === false) {
  $ym = date('Y-m');
  $timestamp = strtotime($ym . '-01');
}

$today = date('Y-m-j');
$todayN = date('N') - 1;
//月曜日に予定が入っているかの前段階
$startMonday = date("Y-m-d", strtotime("-{$todayN} day"));
$html_title = date('Y年n月', $timestamp);
$prev = date('Y-m', mktime(0, 0, 0, date('m', $timestamp) - 1, 1, date('Y', $timestamp)));
$next = date('Y-m', mktime(0, 0, 0, date('m', $timestamp) + 1, 1, date('Y', $timestamp)));
$day_count = date('t', $timestamp);
$youbi = date('w', mktime(0, 0, 0, date('m', $timestamp), 1, date('Y', $timestamp)));
$weeks = [];
$week = '';
$week .= str_repeat('<td></td>', $youbi);
$subjectNumber = array();
$subjectNamae = array();

$recordSet = mysqli_query($db, "select * from subjectTable where subjectClassID = {$classID}");
while ($data = mysqli_fetch_assoc($recordSet)) {
  array_push($subjectNumber, $data['subjectID']);
  array_push($subjectNamae, $data['subjectName']);
}

if (isset($_POST['Monday'])) {
  $m = $_POST['Monday'];
  $md = $_POST["{$m}"];
  $startWeek = date('Y-m-d', strtotime($m));
  $db = mysqli_connect('localhost', '2021', '2021', "rucs");
  if ($db == FALSE) {
    exit('データベースに接続できませんでした。');
  }
  mysqli_set_charset($db, 'utf8');
  $query = "insert into weeks (classID, monday, presetNumber) values ({$classID},'{$m}','{$md}')";
  $result = mysqli_query($db, $query);
  if ($result == FALSE) {
    exit("追加できませんでした。");
  }
  $preset = array();
  $recordSet = mysqli_query($db, "select * from presetData where classID = {$classID} and presetNumber = {$md}");
  $recordData = mysqli_fetch_assoc($recordSet);
  $preset = [
    $recordData['preset11'], $recordData['preset12'], $recordData['preset13'], $recordData['preset14'], $recordData['preset15'], $recordData['preset16'], $recordData['preset21'], $recordData['preset22'], $recordData['preset23'], $recordData['preset24'], $recordData['preset25'], $recordData['preset26'], $recordData['preset31'], $recordData['preset32'], $recordData['preset33'], $recordData['preset34'], $recordData['preset35'], $recordData['preset36'], $recordData['preset41'], $recordData['preset42'], $recordData['preset43'], $recordData['preset44'], $recordData['preset45'], $recordData['preset46'], $recordData['preset51'], $recordData['preset52'], $recordData['preset53'], $recordData['preset54'], $recordData['preset55'], $recordData['preset56']
  ];
  $time = 1;
  $dayOfweek = 1;
  $m2 = str_replace("-", "", $m) + 0.1;
  $m3 = $m . " 00:00:00";
  $m3 = date('Y-m-d H:m:s', strtotime($m3));
  $sql = "";
  for ($dayOfweek = 0; $dayOfweek < 5; $dayOfweek++) {
    for ($time = 1; $time < 7; $time++) {
      $m2 = str_replace("-", "", $startWeek) + ($time / 10);
      $sql .= "('{$m2}'" . "," . "'{$startWeek}'" . "," . "'{$dayOfweek}'" . "," . "'{$classID}'" . "," . "'{$time}'" . "," . "'{$preset[6 * ($dayOfweek) +$time - 1]}'),";
    }
    $startWeek = date('Y-m-d', strtotime("+1 day" . $startWeek));
  }
  $sql = substr($sql, 0, -1);
  $query = "REPLACE INTO Calendar VALUES {$sql};";
  $result = mysqli_query($db, $query);
  $startWeek = date('Y-m-d', strtotime($m));
  $sql = "";
  for ($dayOfweek = 0; $dayOfweek < 5; $dayOfweek++) {
    for ($time = 1; $time < 7; $time++) {
      $m2 = str_replace("-", "", $startWeek) + ($time / 10);
      $recordSet = mysqli_query($db, "select * from bringTable where classID = {$classID} and subjectID = {$preset[6 * ($dayOfweek) +$time - 1]}");
      while ($data = mysqli_fetch_assoc($recordSet)) {
        $bring = $data['bringName'];
        $sql .= "('{$m2}'" . "," . "'{$classID}'" . "," . "'{$preset[6 * ($dayOfweek) +$time - 1]}'" . "," . "'{$bring}'),";
      }
    }
    $startWeek = date('Y-m-d', strtotime("+1 day" . $startWeek));
  }
  $sql = substr($sql, 0, -1);
  $query = "REPLACE INTO bringCalendar VALUES {$sql};";
  $result = mysqli_query($db, $query);

  if ($result == FALSE) {
    exit("追加できませんでした。");
  }
}

$isset = 0;
$preset = array();
$realMonday = '';

for ($day = 1; $day <= $day_count; $day++, $youbi++, $isset--) {
  $date = $ym . '-' . $day;
  $preset = array();
  $recordSet = mysqli_query($db, "select * from presetData where classID = {$classID}");
  $recordData = mysqli_fetch_assoc($recordSet);
  $preset = [
    $recordData['preset11'], $recordData['preset12'], $recordData['preset13'], $recordData['preset14'], $recordData['preset15'], $recordData['preset16'], $recordData['preset21'], $recordData['preset22'], $recordData['preset23'], $recordData['preset24'], $recordData['preset25'], $recordData['preset26'], $recordData['preset31'], $recordData['preset32'], $recordData['preset33'], $recordData['preset34'], $recordData['preset35'], $recordData['preset36'], $recordData['preset41'], $recordData['preset42'], $recordData['preset43'], $recordData['preset44'], $recordData['preset45'], $recordData['preset46'], $recordData['preset51'], $recordData['preset52'], $recordData['preset53'], $recordData['preset54'], $recordData['preset55'], $recordData['preset56']
  ];
  if ($youbi % 7 == 1) {
    $realMonday = $date;
    $recordSet = mysqli_query($db, "select count(*) as count from weeks where classID = {$classID} AND monday = '{$date}'");
    $recordCount = mysqli_fetch_assoc($recordSet);
    if ($recordCount['count'] == 0) {
      $week .= '<td>' . $day . '<br>presetを設定してください';
      $recordSet = mysqli_query($db, "select * from presetData where classID = {$classID}");
      $week .= "<form action=index.php method=POST><select name={$date}>";
      while ($data = mysqli_fetch_assoc($recordSet)) {
        $week .= '<option value=' . $data['presetNumber'] . '>' . $data['presetName'] . '</option>';
      }
      $week .= "<input name='Monday' hidden value='{$date}'>";
      $week .= "<input type='submit' value='Set'>";
      $week .= '</form>';
    } else {
      if ($date == $today) {
        $week .= '<td class="today">' . $day;
      } else {
        $week .= '<td>' . $day;
      }
      $isset = 7;
      for ($k = 1; $k < 7; $k++) {
        $date = date('Y-m-d', strtotime($date));
        $searchDay = str_replace("-", "", $date) + ($k / 10);
        $recordSet2 = mysqli_query($db, "select * from Calendar where classID = {$classID} AND originalNumber = '{$searchDay}'");
        $recordData2 = mysqli_fetch_assoc($recordSet2);
        $subTitle = $recordData2['subjectID'];
        $p = array_search($subTitle, $subjectNumber);
        $Title = $subjectNamae[$p];
        $searchDay = strtr((string)$searchDay, '.', '_');
        $week .=  "<br>{$k}.<a href='detail.php?ym={$searchDay}&subject={$subTitle}'>{$Title}</a>";
      }
    }
  } else {
    if ($ym != substr($realMonday, 0, 7)) {
      $isset = 7;
    }
    if ($date == $today) {
      $week .= '<td class="today">' . $day;
    } else {
      $week .= '<td>' . $day;
    }
    for ($i = 1; $i < 7; $i++) {
      $date = date('Y-m-d', strtotime($date));
      $searchDay = str_replace("-", "", $date) + ($i / 10);
      $recordSet = mysqli_query($db, "select * from Calendar where classID = {$classID} AND originalNumber = '{$searchDay}'");
      $recordData = mysqli_fetch_assoc($recordSet);
      if ($recordData) {
        $subTitle = $recordData['subjectID'];
        $p = array_search($subTitle, $subjectNumber);
        $Title = $subjectNamae[$p];
        $searchDay = strtr((string)$searchDay, '.', '_');
        $week .=  "<br>{$i}.<a href='detail.php?ym={$searchDay}&subject={$subTitle}'>{$Title}</a>";
      }
    }
  }

  $week .= '</td>';
  // 週終わり、または、月終わりの場合
  if ($youbi % 7 == 6 || $day == $day_count) {
    if ($day == $day_count) {
      $week .= str_repeat('<td></td>', 6 - $youbi % 7);
    }
    $weeks[] = '<tr>' . $week . '</tr>';
    $week = '';
  }
}

//ログイン済みの場合
if (isset($_SESSION['EMAIL'])) {
  echo '<!DOCTYPE html><html lang="jp"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>RUCS</title></head> <link href="./bootstrap/css/bootstrap.min.css" rel="stylesheet" /> <script src="./bootstrap/js/bootstrap.min.js"></script><link rel="icon" href="./favicon.ico" /><style>.container {sans-serif;margin-top: 80px;}a {text-decoration: none;}th {height: 30px;text-align: center;}td {height: 100px;}.today {background: orange !important;}th:nth-of-type(1), td:nth-of-type(1) {color: red;}th:nth-of-type(7), td:nth-of-type(7) {color: blue;}</style></head><body><nav class="navbar navbar-expand-lg navbar-light bg-light"> <div class="container-fluid"> <a class="navbar-brand" href="index.php">RUCS</a> <div class="collapse navbar-collapse" id="navbarSupportedContent"> <ul class="navbar-nav me-auto mb-2 mb-lg-0"> <li class="nav-item"> <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">' . intdiv(h($_SESSION['gradeid']), 10) . "年" . h($_SESSION['gradeid']) % 10 . '組</a> </li> </ul> </div> <a href="logout.php" class="ms-auto link-light" hreflang="ar">ログアウト</a> </div> </nav>';
  echo '<div class="container"><h3 class="mb-5"><a href="?ym=';
  echo $prev;
  echo '">&lt;</a>';
  echo $html_title;
  echo '<a href="?ym=';
  echo $next;
  echo '">&gt;</a></h3><div class="row"><div class="col-md-9"><table class="table table-bordered"><tr><th>日</th><th>月</th><th>火</th><th>水</th><th>木</th><th>金</th><th>土</th></tr>';
  foreach ($weeks as $week) {
    echo $week;
  }
  echo '</table></div><div class="col-md-3"><ul class="list-group"><li class="list-group-item"><a href="subjectEdit.php">教科登録・編集</a></li><li class="list-group-item"><a href="preset.php">プリセット登録</a></li><li class="list-group-item"><a href="addData.php">予定追加</a></li><li class="list-group-item"><a href="editNews.php">お知らせ編集</a></li><li class="list-group-item"><a href="others.php">その他</a></li></div></div></body>';
  echo "</html>";
  exit;
}

?>

<!DOCTYPE html>
<html lang="ja">

<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ログイン</title>
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
        </ul>
      </div>
    </div>
  </nav>
  <div class="container">
    <div class="row">
      <div class="col-6 col-md-4"></div>
      <div class="col-6 col-md-4">
        <h1 class="mb-4 text-center">ログイン</h1>
        <form action="login.php" method="post">
          <label for="inputEmail" class="visually-hidden">Email address</label>
          <input type="email" name="email" class="form-control" placeholder="Email address" required autofocus>
          <label for="inputPassword" class="visually-hidden">Password</label>
          <input type="password" name="password" class="form-control" placeholder="Password" required>
          <button class="w-100 btn btn-lg btn-primary mt-3" type="submit">Sign in</button>
        </form>
        <br>
        <p>新規登録は<a href="register.php">こちら</a>からできます</p>
      </div>
      <div class="col-6 col-md-4"></div>
    </div>
  </div>
</body>

</html>