# 仕様

## コンセプト

- YouTube Live番組表を提供する。

## 画面表示

- Channel テーブルに存在するYouTubeチャンネルのライブストリーム情報およびライブストリームの状態を表示する。
- 現在時刻から2時間前以降の当日のライブストリームの情報を表示する。
- ステータスは、「Upcoming」または「Live●」を表示する。
- Liveテーブルから表示に使用するカラムは、thumbnail, channeltitle, videotitle, starttime, status, liveurl, channelurl とする。
- デザインはイイ感じのサイトを参考にする。（未実装）

## サーバ処理（バッチ処理）

- YouTubeチャンネルのIDを元に、当日に行われるライブストリームの情報をAPI経由で取得する。
- 情報取得は毎時10分、30分、50分に Channel テーブルの channelid を引数に行う。
- 取得したデータは、Liveテーブルに保存を行う。
- 取得・保存する内容は、thumbnail, channeltitle, videotitle, starttime, status, liveurl, channelurl とする。
- 処理順は次のとおり 
    - channelid が既に存在するかをチェックし、存在する場合は status のみ確認し差分があったら対象レコードに status のみを更新する。
    - channelid が存在しない場合は、channelid をキーに、VideoID を取得する。
    - VideoIDをキーにYouTube Data API経由で、thumbnail, channeltitle, videotitle, starttime, status を取得する。
    - Liveテーブルへ、thumbnail, channeltitle, videotitle, starttime, status, liveurl, channelurlを保存する。
- Liveテーブルの starttime から12時間以上が経過した場合、該当レコードは削除対象とする。

## Channel テーブルへのデータ追加手段

- 手動で追加を行う。
- 対象のチャンネル情報をCSVファイルで用意し、一括追加を行う。
- チャンネルを新たに追加したい場合は、ChannelテーブルをCSVファイルとしてエクスポートし、修正を加え、再度インポートする。
- utf-8でインポートしてもエラーとなる場合はLinux環境でCSVファイルを作成する。

## YouTube Data API v3
- ライブストリームの詳細情報取得
    - https://www.googleapis.com/youtube/v3/videos?part=snippet,liveStreamingDetails&id={VideoID}

## 参考URL
- ライブストリームURL
- https://www.youtube.com/channel/チャンネルID/live
- https://www.youtube.com/watch?v=VideoID
    - ライブの状態・サムネ・チャンネル名・ライブ名・リンクURLはチャンネルIDから取得可能。
    - 開始時刻を取得したい場合はvideo:listのAPIを経由する必要がある。
