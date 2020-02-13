# 仕様

## 画面表示

- liveテーブルに登録済みのYouTubeチャンネルのライブ情報およびライフ状態を表示する。
- 現在時刻から一時間前を基準とした、当日のライブ開始時間を表示する。
- ステータスは、「upcoming」または「live」を表示し、終了中のライブは表示対象外とする。
- liveテーブルから表示に使用するカラムは、thumbnail, channeltitle, videotitle, starttime, status, liveurl, channelurl とする。

## サーバ処理（バッチ処理）

- YouTubeチャンネルのIDを元に、当日に行われるライブストリーミングの情報をAPI経由で取得する。
- API経由での情報取得は毎時0分と30分および手動で、Channelテーブルの channelid を引数に行う。
- API経由で正常に取得できなかった際にエラーメッセージを画面側に出力する。
- 取得したデータは、liveテーブルに保存を行う。
- 取得・保存する内容は、thumbnail, channeltitle, videotitle, starttime, status, liveurl, channelurl とする。
- 処理順は次のとおり 
    - Channel テーブルの channelid をキーに、状態が「upcoming」のVideo IDを取得する。
    - channelid が既に存在するかをチェックし、存在する場合は status のみ確認し差分があったら対象レコードに status のみを更新する。
    - Video IDから、thumbnail, channeltitle, videotitle, starttime, status を取得する。
    - liveテーブルへ、thumbnail, channeltitle, videotitle, starttime, status, liveurl, channelurlを保存する。
- 現在時刻がstarttime以降であれば、status列には live をセットする。
- liveテーブルの starttime から12時間以上が経過した場合、該当レコードは削除対象とする。
- レコードの削除は0時および12時に実施する。

## Channel テーブルへのデータ追加手段

- 手動で追加を行う。
- 対象のチャンネル情報をCSVファイルで用意し、一括追加を行う。

## API
- チャンネル情報取得（状態・サムネ・VideoID）
- https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&eventType=upcoming&channelId={チャネルID}

- ライブストリームの詳細情報取得
- https://www.googleapis.com/youtube/v3/videos?part=snippet,liveStreamingDetails&id={VideoID}

## 参考URL
- ライブ接続URL
- https://www.youtube.com/channel/チャンネルID/live
- https://www.youtube.com/watch?v=VideoID
    - ライブの状態・サムネ・チャンネル名・ライブ名・リンクURLはチャンネルIDから取得可能。
    - 開始時刻を取得したい場合は別APIを叩かなけばいけない。
