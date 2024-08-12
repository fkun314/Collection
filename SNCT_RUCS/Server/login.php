<?php

require_once('config.php');
session_start();
if (!filter_var($_POST['email'], FILTER_VALIDATE_EMAIL)) {
  $text_alert = "<script type='text/javascript'>alert('入力された値が不正です');</script>";
  echo $text_alert;
  echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/index.php';</script>";
  return false;
}
try {
  $pdo = new PDO(DSN, DB_USER, DB_PASS);
  $stmt = $pdo->prepare('select * from userDeta where email = ?');
  $stmt->execute([$_POST['email']]);
  $row = $stmt->fetch(PDO::FETCH_ASSOC);
} catch (\Exception $e) {
  echo $e->getMessage() . PHP_EOL;
}
//emailがDB内に存在しているか確認
if (!isset($row['email'])) {
  $text_alert = "<script type='text/javascript'>alert('メールアドレス又はパスワードが間違っています');</script>";
  echo $text_alert;
  echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/index.php';</script>";
  return false;
}
//パスワード確認後sessionにメールアドレスを渡す
if (password_verify($_POST['password'], $row['password'])) {
  session_regenerate_id(true);
  $_SESSION['EMAIL'] = $row['email'];
  $_SESSION['gradeid'] = $row['gradeId'];

  echo "Redirecting TOP Page...";
  header('Location: https://fulab.tk/rucs/index.php');
} else {
  $text_alert = "<script type='text/javascript'>alert('メールアドレス又はパスワードが間違っています');</script>";
  echo $text_alert;
  echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/index.php';</script>";
  return false;
}
