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

?>

<!DOCTYPE html>
<html lang="jp">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>教科登録</title>
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
        <main>
            <div class="py-5 text-center">
                <img class="d-block mx-auto mb-4" src="./img/logo.png" alt="" height="60">
                <h2>教科登録</h2>
                <p class="lead">教科の登録ができます。</p>
            </div>
            <div class="row">
                <div class="col-6 col-md-2"></div>
                <div class="col-6 col-md-8">
                    <form action="subjectregist.php" method="POST" novalidate>
                        <div class="row g-3">
                            <div class="col-sm-8">
                                <label class="form-label">教科名</label>
                                <input type="text" class="form-control" name="subjectName" required>
                            </div>

                            <div class="col-sm-4">
                                <label class="form-label">色</label>
                                <input type="color" class="form-control form-control-color" name="color" required>
                            </div>
                        </div>

                        <hr class="my-4">

                        <p>※教科名はタブレットにそのまま反映されるため注意してください。</p>
                        <p>※生徒のアプリでも同じ色が使用されます。アプリ内で見やすいようにイメージカラーは明るめがおすすめです。</p>
                        </p>

                        <hr class="my-4">


                        <button class="w-100 btn btn-primary btn-lg col-sm-6 d-block mx-auto" type="submit">登録</button>
                    </form>
                </div>
                <div class="col-6 col-md-2"></div>
            </div>
        </main>
    </div>
</body>

</html>