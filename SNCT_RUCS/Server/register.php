<!DOCTYPE html>
<html lang="ja">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>新規登録</title>
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
                <h1 class="mb-4 text-center">新規登録</h1>
                <form action="signUp.php" method="post">
                    <div class="row">
                        <div class="col">
                            <select name="grade" id="inputState" class="form-control">
                                <option value="1">１年</option>
                                <option value="2">２年</option>
                                <option value="3">３年</option>
                                <option value="4">４年</option>
                                <option value="5">５年</option>
                                <option value="6">６年</option>
                            </select>
                        </div>
                        <div class="col">
                            <select name="class" id="inputState" class="form-control">
                                <option value="1">１組</option>
                                <option value="2">２組</option>
                                <option value="3">３組</option>
                                <option value="4">４組</option>
                                <option value="5">５組</option>
                                <option value="6">６組</option>
                            </select>
                        </div>
                    </div>
                    <br>
                    <label for="inputEmail" class="visually-hidden">Email address</label>
                    <input type="email" name="email" class="form-control" placeholder="Email address" required autofocus>
                    <label for="inputPassword" class="visually-hidden">Password</label>
                    <input type="password" name="password" class="form-control" placeholder="Password" required>
                    <button class="w-100 btn btn-lg btn-primary mt-3" type="submit">Register</button>
                    <p>※パスワードは半角英数字をそれぞれ１文字以上含んだ、８文字以上で設定してください。</p>
                </form>

            </div>
            <div class="col-6 col-md-4"></div>
        </div>
    </div>
</body>

</html>