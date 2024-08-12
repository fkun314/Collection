<?php
// require_once('./config.php');

// if (!session_id()) {
//     session_start();
// }

// $base_url = "https://access.line.me/oauth2/v2.1/authorize";
// $client_id = CLIENT_ID;
// $redirect_uri = REDIRECT_URI;

// $_SESSION['_line_state'] = sha1(time());

// $query = "";
// $query .= "response_type=" . urlencode("code") . "&";
// $query .= "client_id=" . urlencode($client_id) . "&";
// $query .= "redirect_uri=" . urlencode($redirect_uri) . "&";
// $query .= "state=" . urlencode($_SESSION['_line_state']) . "&";
// $query .= "scope=" . urlencode("openid") . "&";

// $url = $base_url . '?' . $query;
?>
<!-- <!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=10.0, user-scalable=yes">
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
</head>

<body> -->
    <!-- <div class="container" style="margin: 10px 0;">
        <div class="panel panel-default">
            <div class="panel-heading">
                LINEログインv2.1テスト
            </div>
            <div class="panel-body">
                <p>ログインしてください。</p>
                <a href="<?php echo $url; ?>">
                    <button>Login</button>
                </a>
            </div>
        </div>
    </div> -->
<!-- </body>

</html> -->

<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional//EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'>
<html xmlns='http://www.w3.org/1999/xhtml' lang='ja' xml:lang='ja'>
<head>
<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>
<title>LINE Login v2 Sample</title>
</head>
<body>
<?php

require_once __DIR__ . '/vendor/autoload.php';

$session_factory = new \Aura\Session\SessionFactory;
$session = $session_factory->newInstance($_COOKIE);
$segment = $session->getSegment('Vendor\Package\ClassName');

$csrf_value = $session->getCsrfToken()->getValue();

$callback = urlencode('https://' . $_SERVER['HTTP_HOST']  . '/line_callback.php');
$url = 'https://access.line.me/dialog/oauth/weblogin?response_type=code&client_id=' . getenv('LOGIN_CHANNEL_ID') . '&redirect_uri=' . $callback . '&state=' . $csrf_value;
echo '<a href=' . $url . '><button class="contact">LINE Login v2 Sample</button></a>';

?>
</body>
</html>