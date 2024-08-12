## 使用技術一覧
<p style="display: inline">
   <img src="https://img.shields.io/badge/-Python-3776AB.svg?logo=python&style=plastic">
   <img src="https://img.shields.io/badge/-Html5-E34F26.svg?logo=html5&style=plastic">
   <img src="https://img.shields.io/badge/-Css3-1572B6.svg?logo=css3&style=plastic">
   <img src="https://img.shields.io/badge/-Javascript-F7DF1E.svg?logo=javascript&style=plastic">
   <img src="https://img.shields.io/badge/-Php-777BB4.svg?logo=php&style=plastic">
</p>


## サーバー側の設定
### 必要ライブラリ
1. apache
2. php
3. samba
### ディレクトリ構造

```
/home/attendance_check/
├html/  …※１
├pdf/    …※２
/var/www/html/
├ index.php
├html/   作成したhtmlファイル保存場所   ……※１
├pdf/     作成したpdfファイル保存場所    ……※２
├css/     Bootstrap関連
└js/      Bootstrap関連
※１、※２はg02_1ディレクトリからhtmlディレクトリへシンボリックリンクを作成する必要がある。
```

### 必要設定
1. 	apache (/etc/apache2/apache2.conf)
DocmentRootを/var/www/html/に変更
2. 	php
特になし
3. 	samba (/etc/samba/smb.conf)
以下の設定を記述（必要に応じて変更する）
```bash
[pdf]
#共有フォルダ指定
   path = /home/g02_1/pdf
#書き込みOK
   writable = yes
#ゲストユーザーOK
   guest ok = yes
#全てゲストとして扱う
   guest only = yes
#フルアクセスでファイル作成
   create mode = 0777
#フルアクセスでフォルダ作成
   directory mode =0777

[html]
   path = /home/g02_1/html
   writable = yes
   guest ok = yes
   guest only = yes
   create mode = 0777
   directory mode = 0777

```


## クライアント側の設定

### 必要ライブラリ
1. 	PyQt5
2. 	time
3. 	datetime
4. 	NFCPy   ……※３
5. 	playsound
6. 	openpyxl
7. 	threading
8. 	designQT   （PyQt Designerで作ったファイル）
9. 	goto-statement
10. 	pdfkit   ……※４
11. 	platform
12. 	SMBConnection
※３   Zadigを使ってUSBドライバをWinUSBに上書きする。その後libusbのMS64dlllibusb-1.0.dllとMS32dlllibusb-1.0.dllをダウンロード
※４　クライアント側にwkhtmlopdfをインストール

### ディレクトリ構造
任意のディレクトリ内で
```
G02.bat (Windowsのみ実行可能)   ……※５
G02/
├_gui.py
├designQT.py
├Ticket_Gate-Beep01-02(Tone1).mp3
├Ticket_Gate-Beep01-03(Tone1).mp3
├Ticket_Gate-Beep01-07(Tone3).mp3
   ├html/    作成したhtmlファイル保存場所
   ├css/      Bootstrap関連
   ├js/       Bootstrap関連
   └pdf/     作成したpdfファイル保存場所

※５　適切なディレクトリパス、環境設定を記述する必要がある。
今回の場合は、G02ディレクトリまでのパスを「C:\Users\kaz\Desktop\」、環境設定Anacondaパスを「C:/Users/kaz/Anaconda3/Scripts/」、仮想環境名を「G02」とした。

```

### 学生の登録
Book1.xlsxの名簿シートに学籍番号、クラス、出席番号、氏名を事前に記述しておく必要がある。ここに記述されていない人を実行するとソフトが応答しなくなるので注意。
### その他の設定
(1)	wkhtmltopdfのインストールパスを記述
_gui.pyの22行目を適切なパスに変更する
(2)	SMB接続設定
_gui.pyの165行目からのSMBConnectionでサーバーのSMBディレクトリ名を記述
_gui.pyの173行目の接続先をサーバーのIPアドレスを記述
（プログラムを実行した際に”echo success”と表示されれば正常に接続している）


## 使用方法
### プログラムの立ち上げ方法
(1)	サーバーと同じLAN内に接続
(2)	PaSoRiとバーコードリーダーを端末に接続
(3)	G02ディレクトリから_gui.pyを起動
### 出席（学生証登録済の場合）
(1)	学生証をNFCリーダーに置く
(2)	学生の出席の登録が完了
### 出席（学生証未登録の場合）
(1)	学生証をNFCリーダーに置く
(2)	画面に「登録が必要です。バーコードを読み取ってください。」と表示される
(3)	バーコードリーダーを使い、学生証のバーコードを読み取る
(4)	学生の出席の登録が完了
### 出席確認結果の出力
(1)	教員用の終了用キーを使い、プログラムを出力させる。
(2)	ブラウザでhttp://サーバーのIPアドレス（今回の場合はhttp://10.65.134.149）にアクセスする。
(3)	それぞれの授業の出席リストhtml版とpdf版を選択することで出席リストを閲覧することが可能


## 使用機器（例）
ノートPC
HP ProBook 430 G2　　（Windows 10）
サーバー
Mac mini　　（Debian 10.10）
NFCリーダー
PaSoRi
バーコードリーダー
BUSICOM BC-BR900L-W

## 備考
個人情報を含んでいるファイルはアップロードされていません