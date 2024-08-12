<?php
// 直接アクセスを拒否する
if (array_shift(get_included_files()) !== __FILE__) {
    define("CLIENT_ID", "1654046701");
    define("CLIENT_SECRET", "6de3470933756a676fc62101beeebca6");
    define("REDIRECT_URI", "https://personal-date.herokuapp.com/callback.php");
} else {
    echo 'Access Denied';
}
