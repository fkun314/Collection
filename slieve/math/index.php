<?php
// include "./TCPDF/tcpdf.php";
  
// $tcpdf = new TCPDF();
// $tcpdf->AddPage();
  
// $tcpdf->SetFont("kozgopromedium", "", 10);
  
// $html = <<< EOF
// <style>
// h1 {
//     font-size: 20px; // 文字の大きさ
//     text-align: center; // テキストを真ん中に寄せる
// }
// p {
//     font-size: 12px; // 文字の大きさ
//     color: #000000; // 文字の色
//     text-align: left; // テキストを左に寄せる
//     line-height:24px;
// }
 
// .tbl{
//     border:solid 1px #ccc;
//     width:100%;
// }
// .tbl th{
//     border:solid 1px #ccc;
//     padding:20px;
//     text-align:center;
// }
// .tbl td{
//     border:solid 1px #ccc;
//     padding:20px;
//     text-align:center;
// }
// li{
//     listy-style:none;
// }
// .num{
//     width:30px;
// }
// h3{
//     border-bottom:solid 1px #ccc;
// }
// h2{
//     font-size:12px;
// }
// </style>
// <div class="wrapper">
// <h1>御見積書</h1>
//     <p></p><p></p>
// <table>
// <tr><td>
// <p>お客様名<br>ご住所<br>有効期限&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;年&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;月&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;日</p>
 
// <p>※下記の通り御見積り申し上げます。</p>
// </td>
// <td class="box2">
//     <p>年&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;月&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;日</p>
//     <div class="company">
//     <h2>株式会社ファイブスターコーポレーション</h2>
//     <p>〒900-0021 沖縄県那覇市泉崎１丁目１３−７<br>
//     TEL 098-988-0892<br>
//     FAX 098-988-0893</p>
//     </div>
// </td></tr>
// </table>
//     <h3>御見積金額　￥</h3>
//     <p><br></p>
// <table class="tbl">
//     <tr><th class="num">No.</th><th>品名</th><th>数量</th><th>単位</th><th>単価</th><th>金額</th><th>備考</th></tr>
//     <tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
//     <tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
//     <tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
//     <tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
//     <tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
//     <tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
//     <tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
//     <tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
//     <tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
//     <tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
// </table>
// </div>
// EOF;
 
// $tcpdf->writeHTML($html);
// $tcpdf->Output('samurai.pdf', 'I');


?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>足し算１</title>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>

</head>
<body>
    <h3>つぎのもんだいをこたえましょう。</h3>
    <div class="p1">

    </div>
    <script>
        var count = 0;
        var allleft = [];
        var allright = [];
        $(function(){
            for(var i = 1; i <= 10; i++){
                $('.p1').append(i+'、　'+add_1to10() + '=<br>');
            }
            $('.p1').append('<button>問題一覧へ</button>');
            $('.p1').append('<button onclick="Reload()">新しい問題へ</button>');
            $('.p1').append('<button onclick="Anser()">答えを見る</button>');
        });

        function add_1to10(){
            // var left = 0;
            var left = Math.floor( Math.random() * 11 );
            allleft.push(left);
            var right = Math.floor( Math.random() * 11 );
            allright.push(right);
            var output = "";
            output += left + "+" + right;
            return output;
        }

        function Anser(){
            count++;
            $('.p1').html("");
            if(count%2 == 1){
                for(var i = 1; i <= 10; i++){
                $('.p1').append(i+'、　'+allleft[i-1] + "+"+allright[i-1] + '=<span style=color:red;>' + (allleft[i-1]+allright[i-1])+'</span><br>');
            }
            $('.p1').append('<button>問題一覧へ</button>');
            $('.p1').append('<button onclick="Reload()">新しい問題へ</button>');
            $('.p1').append('<button onclick="Anser()">答えを見る</button>');
            }else{
            $('.p1').html("");
                for(var i = 1; i <= 10; i++){
                $('.p1').append(i+'、　'+allleft[i-1] + "+"+allright[i-1] + '=' + '<br>');
            }
            $('.p1').append('<button>問題一覧へ</button>');
            $('.p1').append('<button onclick="Reload()">新しい問題へ</button>');
            $('.p1').append('<button onclick="Anser()">答えを見る</button>');
            }
        }

        function Reload(){
            location.reload();
        }
    </script>
</body>
</html>