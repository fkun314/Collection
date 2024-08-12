<?php
session_start();
$output = '';
if (isset($_SESSION["EMAIL"])) {
  $output = 'Logoutしました';
} else {
  $output = 'SessionがTimeoutしました';
}
//セッション変数クリア
$_SESSION = array();
//セッションクッキー削除
if (ini_get("session.use_cookies")) {
    $params = session_get_cookie_params();
    setcookie(session_name(), '', time() - 42000,
        $params["path"], $params["domain"],
        $params["secure"], $params["httponly"]
    );
}
//セッションクリア
@session_destroy();

$text_alert = "<script type='text/javascript'>alert('{$output}');</script>";
echo $text_alert;
echo "<script type='text/javascript'>location.href = 'https://fulab.tk/rucs/index.php';</script>";