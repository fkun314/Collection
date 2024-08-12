<?php
require_once('config.php');
//データベースへ接続、テーブルがない場合は作成
try {
  $pdo = new PDO(DSN, DB_USER, DB_PASS);
  $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
  $pdo->exec("create table if not exists userDeta(
      id int not null auto_increment primary key,
      gradeId char(2),
      email varchar(255) unique,
      password varchar(255) ,
      created timestamp not null default current_timestamp
    )");
} catch (Exception $e) {
  echo $e->getMessage() . PHP_EOL;
}
//POSTのValidate。
if (!$email = filter_var($_POST['email'], FILTER_VALIDATE_EMAIL)) {
  $text_alert = "<script type='text/javascript'>alert('入力された値が不正です');</script>";
  echo $text_alert;
  echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/register.php';</script>";
  return false;
}
//パスワードの正規表現
if (preg_match('/\A(?=.*?[a-z])(?=.*?\d)[a-z\d]{8,100}+\z/i', $_POST['password'])) {
  $password = password_hash($_POST['password'], PASSWORD_DEFAULT);
} else {
  $text_alert = "<script type='text/javascript'>alert('パスワードは半角英数字をそれぞれ1文字以上含んだ8文字以上で設定してください');</script>";
  echo $text_alert;
  echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/register.php';</script>";
  return false;
}
//登録処理
try {
  $gradeId = $_POST['grade'] . $_POST['class'];
  $stmt = $pdo->prepare("insert into userDeta(gradeId, email, password) value(?, ?, ?)");
  $stmt->execute([$gradeId, $email, $password]);

  function h($s)
  {
    return htmlspecialchars($s, ENT_QUOTES, 'utf-8');
  }

  $db = mysqli_connect('localhost', '2021', '2021', "rucs");
  if ($db == FALSE) {
    exit('データベースに接続できませんでした。');
  }
  mysqli_set_charset($db, 'utf8');

  $subjectName = $_POST['subjectName'];
  $subjectColor = $_POST['color'];

  $query = "insert into subjectTable (subjectClassID, subjectName, subjectColor) values ({$gradeId},'なし','#ffffff')";

  $result = mysqli_query($db, $query);

  $text_alert = "<script type='text/javascript'>alert('登録完了しました');</script>";
  echo $text_alert;
  echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/index.php';</script>";
  return false;
} catch (\Exception $e) {
  $text_alert = "<script type='text/javascript'>alert('すでに登録されています');</script>";
  echo $text_alert;
  echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/register.php';</script>";
  return false;
}
