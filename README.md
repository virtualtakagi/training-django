# 仕様

## 画面表示

- データベースに登録済みのYouTubeチャンネルのブロードキャストステータスを表示する。
- 現在時刻を基準とした当日のブロードキャスト開始時間を表示する。
- ステータスは、「upcoming」のみ表示し、開始済みおよび終了中のブロードキャストは表示対象外とする。
- liveテーブルから表示に使用するカラムは、Thumbnail, Channel Title, Video Title, Scheduled Time, Status とする。

## サーバ処理（バッチ処理）

- YouTubeチャンネルのIDを元に、ブロードキャストの情報をAPI経由で取得する。
- API経由での情報取得は30分に1度、ChannelテーブルのチャンネルIDを引数に行う。
- 取得したデータは、liveテーブルに保存を行う。
- 取得・保存する内容は、Thumbnail, Channel ID, Video ID, Video Title, Channel Title, Start Time, Status とする。
- 処理順は次のとおり 
- - チャンネルIDから、状態がupcomingの場合に限り、Video IDを取得する。
- - Video IDから、Thumbnail, Video Title, Channel Title, StartTime, Status を取得する。
- - liveテーブルへ、Thumbnail, Video Title, Video ID, Channel ID, Channel Title, StartTime, Statusを保存する。

## API
- チャンネル情報取得（状態・サムネ・VideoID）
- https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&eventType=upcoming&channelId={チャネルID}

- ライブストリームの詳細情報取得
- https://www.googleapis.com/youtube/v3/video?part=snippet,liveStreamingDetails&id={VideoID}

## 参考URL
- ライブ接続URL
- https://www.youtube.com/channel/チャンネルID/live
- https://www.youtube.com/watch?v=VideoID
ライブの状態・サムネ・チャンネル名・ライブ名・リンクURLはチャンネルIDから取得可能。
開始時刻を取得したい場合は別APIを叩かなければいけない。
