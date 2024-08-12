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
    <title>プリセット</title>
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
        <div class="py-5 text-center">
            <img class="d-block mx-auto mb-4" src="./img/logo.png" alt="" height="60">
            <h2>プリセット登録</h2>
            <p class="lead">プリセット登録できます</p>
        </div>
        <div class="row">
            <div class="col-md-11 col-lg-12">
            <form action="setpreset.php" method="POST">
                <div class="text-center">
                    <label for="firstName" class="form-label">プリセット名</label>
                    <input name="nm" type="text">
                </div>
                <hr class="my-4">
                <table class="table">
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">月</th>
                            <th scope="col">火</th>
                            <th scope="col">水</th>
                            <th scope="col">木</th>
                            <th scope="col">金</th>
                        </tr>
                    </thead>
                    <tbody>

                        <?php
                        for ($j = 1; $j < 7; $j++) {
                            echo ("<tr>");
                            echo ("<td>" . $j . "</td>");
                            for ($i = 1; $i < 6; $i++) {
                                $recordSet = mysqli_query($db, "select * from subjectTable where subjectClassID = {$classID}");
                                $name = (string)$i . (string)$j;
                                echo ("<td>");
                                echo ("<select name=" . $name . " class='form-select'>");
                                echo ("<option hidden>選択してください</option>");
                                while ($data = mysqli_fetch_assoc($recordSet)) {
                                    printf('<option value="%d">%s</option>', $data['subjectID'], $data['subjectName']);
                                }
                                echo ("</td>");
                            }
                            echo ("</tr>");
                        }
                        ?>
                    </tbody>
                </table>
                <hr>
                <div class="text-center">
                <p>※教科を入れる必要がない場合は「なし」を選択してください</p>
                </div>
                <button class="w-100 btn btn-primary btn-lg col-sm-6 d-block mx-auto mt-4" type="submit">登録</button>
            </form>
            </div>
        </div>
    </div>
</body>

</html>