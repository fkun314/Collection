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
    <title>教科編集</title>
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
                <h2>教科編集</h2>
                <p class="lead">教科の編集・持ち物の登録ができます。</p>
            </div>
            <div class="row">
                <div class="col-6 col-md-4"></div>
                <div class="col-6 col-md-4">
                    <form action="bringRegister.php" method="POST" novalidate>
                        <div class="row g-3">
                            <div class="col-12">
                                <label for="firstName" class="form-label">名称（表示名）：</label>
                                <br>
                                <a href="subjectRegister.php">新規作成</a>
                                <select name="subjectID">
                                    <option hidden>選択してください</option>
                                    <?php
                                    $recordSet = mysqli_query($db, "select * from subjectTable where subjectClassID = {$classID}");

                                    while ($data = mysqli_fetch_assoc($recordSet)) {
                                        printf('<option value="%d">%s</option>', $data['subjectID'], $data['subjectName']);
                                    }
                                    ?>
                                </select>
                            </div>

                            <div class="col-12">
                                <label class="form-label">持ち物</label>
                                <input type="text" name="bring" class="form-control">
                                <input type="text" name="gradeID" hidden value="<?php echo $_SESSION['gradeid'];  ?>">
                                <hr class="my-4">
                                <p class="text-center">既に登録済みの持ち物</p>
                                <div id="kison">


                                </div>


                                <button class="w-100 btn btn-primary btn-lg col-sm-6 d-block mx-auto mt-4" type="submit">保存</button>
                    </form>
                </div>
                <div class="col-6 col-md-4"></div>
            </div>
        </main>
    </div>
    <script>
        $(function() {
            var kisonList = new Array();
            <?php
            printf("var classID = {$classID};");
            printf("var subjectID = $('option:selected').val();");
            $recordSet = mysqli_query($db, "select * from bringTable where classID = {$classID}");

            if (!$recordSet) {
                printf('');
            } else {
                while ($data = mysqli_fetch_assoc($recordSet)) {
                    printf("kisonList.push('%d');", $classID);
                    printf("kisonList.push('%d');", $data['subjectID']);
                    printf("kisonList.push('%s');", "<li>{$data['bringName']}</li>");
                }
            }
            ?>
            $('select').change(function() {
                $('#kison').html("");
                var subjectID = $('option:selected').val();
                for (var i = 0; i < kisonList.length; i += 3) {
                    if (kisonList[i] == classID) {
                        if (kisonList[i + 1] == subjectID) {
                            $('#kison').append(kisonList[i + 2]);
                        }
                    }
                }
            });
        });
    </script>
</body>

</html>