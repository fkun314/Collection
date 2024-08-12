# 2024/08/09時点

## プログラムほか
- [CNNを用いた動画検索システム](./flask_2022/)

- [進化計算を用いたマスコン自動制御システム](./GA_train/)

- [RUCS＿小学生向け忘れ物削減システム](./SNCT_RUCS/)

- [LINE Bot向け Personal_data ページ](./personal-data/)

- [YouTubeLive チャット分析ツール](./youtube_chat_analyse_v2%20copy/)

- [Slieve. 小学生・中学生向け算数プリント作成ページ]()
## LINE Bot

- [中学生向け英単語クイズ](https://lin.ee/Pwu3mql)
<details>
    <summary>コードはこちら</summary>
    ```javascript


    //ユーザーから受け取ったメッセージをオウム返しするサンプルコード
    function doPost(e) {
      //LINE Messaging APIのチャネルアクセストークンを設定
      let token = "ht1HjnU2F/O2uAHgUyHWNfP2eIedj+jFg9XKFeUHG5KhDr718daWYkZ+4JAeTO03whndkFejNtd3Xxi6RjC2Ikd4zcV0AoGW5WhC94rFZCF4DhSSbqLCmDuOCe54Y5kxGF1MwO9I2jXL9pb8gVwVfQdB04t89/1O/w1cDnyilFU=";
      // WebHookで取得したJSONデータをオブジェクト化し、取得
      let eventData = JSON.parse(e.postData.contents).events[0];
      //取得したデータから、応答用のトークンを取得
      let replyToken = eventData.replyToken;
      //取得したデータから、メッセージ種別を取得
      let messageType = eventData.message.type;
      //取得したデータから、ユーザーが投稿したメッセージを取得
      var userMessage = eventData.message.text;

      var returnText = "";

      var user_id = eventData.source.userId;

      var setting = IDList(user_id)[0];

      if (setting == "change_grade") {
        if (userMessage.indexOf("１年生") != -1 || userMessage.indexOf("1年生") != -1) {
          changeGrade(user_id, 1);
          returnText += "1年生に変更しました\n"
          returnText += Question(user_id, "same");
        } else if (userMessage.indexOf("２年生") != -1 || userMessage.indexOf("2年生") != -1) {
          changeGrade(user_id, 2);
          returnText += "2年生に変更しました\n"
          returnText += Question(user_id, "same");
        }
        else if (userMessage.indexOf("３年生") != -1 || userMessage.indexOf("3年生") != -1) {
          changeGrade(user_id, 3);
          returnText += "3年生に変更しました\n"
          returnText += Question(user_id, "same");

        } else if (userMessage.indexOf("全部") != -1) {
          changeGrade(user_id, userMessage);
          returnText += "全学年に変更しました\n"
          returnText += Question(user_id, "same");
        }
        else {
          returnText += "学年を変更します。１年生、２年生、３年生、全部、のどれかを入力してください。";
        }
      } else if (setting == "change_type") {
        if (userMessage.indexOf("名詞") != -1 || userMessage.indexOf("代名詞") != -1 || userMessage.indexOf("動詞") != -1 || userMessage.indexOf("形容詞") != -1 || userMessage.indexOf("副詞") != -1 || userMessage.indexOf("前置詞") != -1 || userMessage.indexOf("フレーズ") != -1 || userMessage.indexOf("全部") != -1 || userMessage.indexOf("接続詞") != -1) {
          changeType(user_id, userMessage);
          returnText += userMessage+"に変更しました\n"
          returnText += Question(user_id, "same");
        }
        else {
          returnText += "品詞を変更します。名詞、代名詞、動詞、形容詞、副詞、接続詞、前置詞、フレーズ、全部、のどれかを入力してください。";
        }
      } else if (setting == "change_output") {
        if (userMessage.indexOf("正順") != -1 || userMessage.indexOf("逆順") != -1 || userMessage.indexOf("ランダム") != -1) {
          changeOutput(user_id, userMessage);
          returnText += userMessage+"に変更しました\n"
          returnText += Question(user_id, "same");
        } else {
          returnText += "出題順を変更します。正順、逆順、ランダム、のどれかを入力してください。";
        }
      }
      else {
        if (userMessage.indexOf("学年") != -1 ){
          if(userMessage.indexOf("変えたい") != -1 || userMessage.indexOf("変更") != -1) {
            returnText += "学年を変更します。１年生、２年生、３年生、全部、のどれかを入力してください。";
            changeSetting(user_id, "change_grade");
          } 
        } else if (userMessage.indexOf("品詞") != -1) {
          if(userMessage.indexOf("変えたい") != -1 || userMessage.indexOf("変更") != -1) {
            returnText += "品詞を変更します。名詞、代名詞、動詞、形容詞、副詞、接続詞、前置詞、フレーズ、全部、のどれかを入力してください。";
            changeSetting(user_id, "change_type");
          }
        } else if (userMessage.indexOf("順番") != -1) {
          if(userMessage.indexOf("変えたい") != -1 || userMessage.indexOf("変更") != -1) {
            returnText += "出題順を変更します。正順、逆順、ランダム、のどれかを入力してください。";
            changeSetting(user_id, "change_output");
          }
        } else {
          if(userMessage.indexOf("現在の問題") != -1 ) {
            returnText += Question(user_id, "same");
          }else  if(userMessage.indexOf("HELP") != -1 ){
            returnText += "このBotでは、ひたすら問題が出題されます。\n答えだと思う番号を記入して送ってください！\n\n学年を変更するには、『学年を変更したい』\n品詞を変更するには、『品詞を変更したい』\n出題順を変更するには、『順番を変更したい』\nと記入してください！";
          }else if (userMessage.indexOf("現在の設定") != -1 ) {
            var setting_list = [];
            setting_list = IDList(user_id);

            var grade = "";

            if (setting_list[1]=="1"){
              grade = "1年生";
            }else if(setting_list[1]=="2"){
              grade = "2年生";
            }else if(setting_list[1] == "3"){
              grade = "3年生";
            }

            returnText += "学年："+ grade  +"\n"+ "品詞："+setting_list[2]+"\n"+"出題順："+setting_list[3]+"\n";

          }else if (!isNaN(userMessage)) {
            var userMessage = parseInt(userMessage, 10);
            returnText += answerCheck(user_id, userMessage);
          }
          else {
            returnText += '1,2,3,4のどれかを入力してください';

          }
        }
      }

      console.log(returnText);

      // 応答メッセージ用のAPI URLを定義
      let url = 'https://api.line.me/v2/bot/message/reply';
      //ユーザーからの投稿メッセージから応答メッセージを用意
      // let replyMessage = "投稿種別：" + messageType + "\n投稿内容：" + returnText;
      let replyMessage = returnText;
      //APIリクエスト時にセットするペイロード値を設定する
      let payload = {
        'replyToken': replyToken,
        'messages': [{
          'type': 'text',
          'text': replyMessage
        }]
      };
      //HTTPSのPOST時のオプションパラメータを設定する
      let options = {
        'payload': JSON.stringify(payload),
        'myamethod': 'POST',
        'headers': { "Authorization": "Bearer " + token },
        'contentType': 'application/json'
      };
      //LINE Messaging APIにリクエストし、ユーザーからの投稿に返答する
      UrlFetchApp.fetch(url, options);
    }

    function test() {
      var returnText = "";

      var user_id = "U66d1a6a92ed6e63a91ee7d79ed7aad9b";

      var userMessage = "ランダム";

      var setting = IDList(user_id)[0];

      if (setting == "change_grade") {
        if (userMessage.indexOf("１年生") != -1 || userMessage.indexOf("1年生") != -1) {
          changeGrade(user_id, 1);
          returnText += "1年生に変更しました\n"
          returnText += Question(user_id, "same");
        } else if (userMessage.indexOf("２年生") != -1 || userMessage.indexOf("2年生") != -1) {
          changeGrade(user_id, 2);
          returnText += "2年生に変更しました\n"
          returnText += Question(user_id, "same");
        }
        else if (userMessage.indexOf("３年生") != -1 || userMessage.indexOf("3年生") != -1) {
          changeGrade(user_id, 3);
          returnText += "3年生に変更しました\n"
          returnText += Question(user_id, "same");

        } else if (userMessage.indexOf("全部") != -1) {
          changeGrade(user_id, userMessage);
          returnText += "全学年に変更しました\n"
          returnText += Question(user_id, "same");
        }
        else {
          returnText += "学年を変更します。１年生、２年生、３年生、全部、のどれかを入力してください。";
        }
      } else if (setting == "change_type") {
        if (userMessage.indexOf("名詞") != -1 || userMessage.indexOf("代名詞") != -1 || userMessage.indexOf("動詞") != -1 || userMessage.indexOf("形容詞") != -1 || userMessage.indexOf("副詞") != -1 || userMessage.indexOf("前置詞") != -1 || userMessage.indexOf("フレーズ") != -1 || userMessage.indexOf("全部") != -1 || userMessage.indexOf("接続詞") != -1) {
          changeType(user_id, userMessage);
          returnText += userMessage+"に変更しました\n"
          returnText += Question(user_id, "same");
        }
        else {
          returnText += "品詞を変更します。名詞、代名詞、動詞、形容詞、副詞、接続詞、前置詞、フレーズ、全部、のどれかを入力してください。";
        }
      } else if (setting == "change_output") {
        if (userMessage.indexOf("正順") != -1 || userMessage.indexOf("逆順") != -1 || userMessage.indexOf("ランダム") != -1) {
          changeOutput(user_id, userMessage);
          returnText += userMessage+"に変更しました\n"
          returnText += Question(user_id, "same");
        } else {
          returnText += "出題順を変更します。正順、逆順、ランダム、のどれかを入力してください。";
        }
      }
      else {
        if (userMessage.indexOf("学年") != -1 ){
          if(userMessage.indexOf("変えたい") != -1 || userMessage.indexOf("変更") != -1) {
            returnText += "学年を変更します。１年生、２年生、３年生、全部、のどれかを入力してください。";
            changeSetting(user_id, "change_grade");
          } 
        } else if (userMessage.indexOf("品詞") != -1) {
          if(userMessage.indexOf("変えたい") != -1 || userMessage.indexOf("変更") != -1) {
            returnText += "品詞を変更します。名詞、代名詞、動詞、形容詞、副詞、接続詞、前置詞、フレーズ、全部、のどれかを入力してください。";
            changeSetting(user_id, "change_type");
          }
        } else if (userMessage.indexOf("順番") != -1) {
          if(userMessage.indexOf("変えたい") != -1 || userMessage.indexOf("変更") != -1) {
            returnText += "出題順を変更します。正順、逆順、ランダム、のどれかを入力してください。";
            changeSetting(user_id, "change_output");
          }
        } else {
          if(userMessage.indexOf("現在の問題") != -1 ) {
            returnText += Question(user_id, "same");
          }else  if(userMessage.indexOf("HELP") != -1 ){
            returnText += "このBotでは、ひたすら問題が出題されます。\n答えだと思う番号を記入して送ってください！\n\n学年を変更するには、『学年を変更したい』\n品詞を変更するには、『品詞を変更したい』\n出題順を変更するには、『順番を変更したい』\nと記入してください！";
          }else if (userMessage.indexOf("現在の設定") != -1 ) {
            var setting_list = [];
            setting_list = IDList(user_id);

            var grade = "";

            if (setting_list[1]=="1"){
              grade = "1年生";
            }else if(setting_list[1]=="2"){
              grade = "2年生";
            }else if(setting_list[1] == "3"){
              grade = "3年生";
            }else if(setting_list[1] == "all")
            {
              grade = "全学年";
            }

            returnText += "学年："+ grade  +"\n"+ "品詞："+setting_list[2]+"\n"+"出題順："+setting_list[3]+"\n";

          }else if (!isNaN(userMessage)) {
            var userMessage = parseInt(userMessage, 10);
            returnText += answerCheck(user_id, userMessage);
          }
          else {
            returnText += '1,2,3,4のどれかを入力してください';

          }
        }
      }

      console.log(returnText);
    }

    function IDList(id) {
      var ss = SpreadsheetApp.getActiveSpreadsheet();
      var sheet = ss.getSheetByName("Setting");
      var values = sheet.getDataRange().getValues();

      console.log(values);

      for (var i = 0; i < (values.length); i++) {
        if (values[i][0] == id) {
          return [values[i][1], values[i][2], values[i][3], values[i][4]];
        }
      }

      //最終行に追加するデータを定義
      const dataArray = [id, "1", "all", "all","ランダム"];
      const dataArrayTwo = [dataArray]; //二次元配列化
      const dataArrayLen = dataArray.length; //一次元配列時の要素の長さ
      const lastRow = sheet.getLastRow(); //セル内が空白になっている最終行番号を取得

      //C,　最終行のセルにデータを追加
      sheet.getRange(lastRow + 1, 1, 1, dataArrayLen).setValues(dataArrayTwo);

      var spreadsheet = SpreadsheetApp.getActive();
      spreadsheet.insertSheet(id);

      return;
    }

    function duplicateSheet(id, type, val) {
      var ss = SpreadsheetApp.getActiveSpreadsheet();
      var sheet = ss.getSheetByName("Base");
      var values = sheet.getDataRange().getValues();

      var duplicate_list = [];

      console.log(type, val)

      if (type == "grade") {
        var hinsi = IDList(id)[2];
        for (var i = 0; i < (values.length); i++) {
          if (val != "all") {
            if (values[i][1] == val) {
              if (hinsi != "all") {
                if (values[i][2] == hinsi) {
                  duplicate_list.push(values[i]);
                  console.log("val not all hinsi not all");
                }
              } else {
                duplicate_list.push(values[i]);
                console.log("val not all hinsi all")
              }
            }
          } else {
            duplicate_list.push(values[i]);
            console.log("val all")
          }
        }
      } else if (type == "type") {
        var grade = IDList(id)[1];
        for (var i = 0; i < (values.length); i++) {
          if (val != "all") {
            if (values[i][2] == val) {
              if (grade != "all") {
                if (values[i][1] == grade) {
                  duplicate_list.push(values[i]);
                  console.log("val not all grade not all")
                }
              } else {
                duplicate_list.push(values[i]);
                console.log("val not all grade all")
              }
            }
          } else {
            duplicate_list.push(values[i]);
            console.log("val all")
          }
        }
      }
      console.log(duplicate_list);
      var ss = SpreadsheetApp.getActiveSpreadsheet();
      var sheet = ss.getSheetByName(id);
      sheet.getRange(1, 1, duplicate_list.length, duplicate_list[0].length).setValues(duplicate_list);

      return;
    }

    function changeSetting(id, val) {
      var ss = SpreadsheetApp.getActiveSpreadsheet();
      var sheet = ss.getSheetByName("Setting");
      var values = sheet.getDataRange().getValues();

      for (var i = 0; i < (values.length); i++) {
        if (values[i][0] == id) {
          var addArray = [val];
          var range = sheet.getRange(i + 1, 2, 1, 1);
          range.setValues([addArray]);
          return val;
        }
      }

      return "";
    }

    function changeGrade(id, val) {
      var ss = SpreadsheetApp.getActiveSpreadsheet();
      var sheet = ss.getSheetByName(id);
      var data = sheet.getDataRange().getValues();

      var searchTerm = val;

      deleteSheet(id);
      console.log("complete delete");

      if (val == "全部") {
        duplicateSheet(id, "grade", "all");
        val == "all";
      } else {
        duplicateSheet(id, "grade", val);
      }
      console.log("complete duplicate")

      var sheet = ss.getSheetByName("Setting");
      var values = sheet.getDataRange().getValues();

      for (var i = 0; i < (values.length); i++) {
        if (values[i][0] == id) {
          var addArray = [val];
          var range = sheet.getRange(i + 1, 3, 1, 1);
          range.setValues([addArray]);

          return val;
        }
      }

      return "";
    }

    function deleteSheet(SheetByName) {
      const sheet = SpreadsheetApp.getActiveSpreadsheet();
      const trashSheet = sheet.getSheetByName(SheetByName); //削除するシートの名前を引数に記入
      trashSheet.clear(); //スプレッドシートを削除
    }

    function changeType(id, val) {
      var ss = SpreadsheetApp.getActiveSpreadsheet();
      var sheet = ss.getSheetByName(id);
      var data = sheet.getDataRange().getValues();

      var searchTerm = val;

      if (val == "全部") {
        deleteSheet(id);
        duplicateSheet(id, "type", "all");
        val == "all";
      } else {
        deleteSheet(id);
        duplicateSheet(id, "type", "all");
      }


      var sheet = ss.getSheetByName("Setting");
      var values = sheet.getDataRange().getValues();

      for (var i = 0; i < (values.length); i++) {
        if (values[i][0] == id) {
          var addArray = [val];
          var range = sheet.getRange(i + 1, 4, 1, 1);
          range.setValues([addArray]);

          return val;
        }
      }

      return "";
    }

    function changeOutput(id, val) {
      var ss = SpreadsheetApp.getActiveSpreadsheet();
      var sheet = ss.getSheetByName(id);

      var range = sheet.getDataRange();
      if (val == "正順") {
        range.sort([{ column: 1, ascending: true }]);
      } else if (val == "逆順")
        range.sort([{ column: 1, ascending: false }]);
      else {
        val = "ランダム";
        var lastRow = sheet.getLastRow();
        var lastColumn = sheet.getLastColumn();
        var data = sheet.getRange(1, 1, lastRow, lastColumn).getValues();
        var shuffledData = shuffle(data);
        sheet.clearContents();
        sheet.getRange(1, 1, lastRow, lastColumn).setValues(shuffledData);
      }

      var sheet = ss.getSheetByName("Setting");
      var values = sheet.getDataRange().getValues();

      for (var i = 0; i < (values.length); i++) {
        if (values[i][0] == id) {
          var addArray = [val];
          var range = sheet.getRange(i + 1, 5, 1, 1);
          range.setValues([addArray]);

          return val;
        }
      }

      return "";
    }

    function shuffle(array) {
      var currentIndex = array.length, temporaryValue, randomIndex;
      while (0 !== currentIndex) {
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
      }
      return array;
    }

    function shuffleArray(array) {
      for (var i = array.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = array[i];
        array[i] = array[j];
        array[j] = temp;
      }
      return array;
    }

    function answerCheck(id, val) {
      var answer = IDList(id)[0];

      var returnText = "";
      // 正解なら次の問題へ
      if (answer == val) {
        returnText += "正解！\n次の問題はこちら！\n\n"
        returnText += Question(id, "next");
      } else {
        // 不正解なら同じ問題を再出題
        returnText += "残念...Try Again! \n\n"
        returnText += Question(id, "same");
      }


      return returnText;
    }

    function Question(id, mode) {
      var ss = SpreadsheetApp.getActiveSpreadsheet();
      var sheet = ss.getSheetByName(id);
      var answer = 0;

      if (mode == "next") {
        // 次の問題へ　（一番上の行を削除して次の問題を出題する）
        sheet.deleteRow(1);
        var values = sheet.getDataRange().getValues();
        var q = values[0][3];
        var answerlist = [];
        answer = values[0][4];

        for (var i = 0; i < (values.length); i++) {
          if (i > 3) {
            break;
          } else {
            answerlist.push(values[i][4]);
          }
        }
      } else {
        // 同じ問題へ
        var values = sheet.getDataRange().getValues();
        var q = values[0][3];
        var answerlist = [];
        answer = values[0][4];

        for (var i = 0; i < (values.length); i++) {
          if (i > 3) {
            break;
          } else {
            answerlist.push(values[i][4]);
          }
        }
      }

      console.log(answerlist)

      var shuffledArr = shuffleArray(answerlist);
      var anserIndex = shuffledArr.indexOf(answer);

      anserIndex += 1;

      console.log("正解：" + anserIndex);
      changeSetting(id, anserIndex);

      var text = "";

      for (var i = 0; i < answerlist.length; i++){
        text += "\n"+(i+1)+":"+answerlist[i];
      }

      var returnText = "問題：" + q + "\n選択肢：" + text;

      return returnText;
    }

```
</details>

- Tips
  - [Matrkdown to HTML](./Markdown_to_Python/)