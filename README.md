# 仕様

## Google API利用制限が厳しく、開発中止(2/18/2020)

- 100件のチャンネルをDBに登録し、一度にAPI経由のリクエストを行うと一瞬で利用制限に引っかかってしまうことが判明。
- YouTube Data API の仕様上、10,000ユニット/日 まで利用可能だが、1チャンネル分の情報リクエストで約100ユニット消費されることが後にわかった。
- Googleに対しAPI利用制限の拡張申請を行うことは可能であるが、多くの時間と情報、作業が必要とされる見込み。
- そのため本プロジェクトの開発はここまでとし、直近で必要とされる技術の学習にリソースを割り当てる。

## コンセプト

- 各ユーザーに特化したYouTube Live番組表を提供する。

## 画面表示

- Liveテーブルに登録済みのYouTubeチャンネルのライブ情報およびライブ状態を表示する。
- 現在時刻から2時間前以降の当日のライブストリームの情報を表示する。
- ステータスは、「upcoming」または「live」、「completed」を表示する。
- Liveテーブルから表示に使用するカラムは、thumbnail, channeltitle, videotitle, starttime, status, liveurl, channelurl とする。
- ライブストリームの情報更新ボタンを押下し、レスポンスがあるまでプログレスバーを表示。（未実装）
- デザインはイイ感じのサイトを参考にする。（未実装）
- ログイン機能の実装により、ユーザー別のチャンネル一覧の提供（未実装）

## サーバ処理（バッチ処理）

- YouTubeチャンネルのIDを元に、当日に行われるライブストリームの情報をAPI経由で取得する。
- API経由での情報取得は毎時0分と30分および手動で、Channelテーブルの channelid を引数に行う。
- API経由で正常に取得できなかった際にエラーメッセージを画面側に出力する。（未実装）
- 取得したデータは、Liveテーブルに保存を行う。
- 取得・保存する内容は、thumbnail, channeltitle, videotitle, starttime, status, liveurl, channelurl とする。
- 処理順は次のとおり 
    - Channel テーブルの channelid をキーに、状態が「upcoming」のVideo IDを取得する。
    - channelid が既に存在するかをチェックし、存在する場合は status のみ確認し差分があったら対象レコードに status のみを更新する。
    - Video IDから、thumbnail, channeltitle, videotitle, starttime, status を取得する。
    - Liveテーブルへ、thumbnail, channeltitle, videotitle, starttime, status, liveurl, channelurlを保存する。
- Liveテーブルの starttime から12時間以上が経過した場合、該当レコードは削除対象とする。

## Channel テーブルへのデータ追加手段

- 手動で追加を行う。
- 対象のチャンネル情報をCSVファイルで用意し、一括追加を行う。

## YouTube Data API v3
- チャンネル情報取得
- https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&eventType=upcoming&channelId={チャネルID}

- ライブストリームの詳細情報取得
- https://www.googleapis.com/youtube/v3/videos?part=snippet,liveStreamingDetails&id={VideoID}

## 参考URL
- ライブストリームURL
- https://www.youtube.com/channel/チャンネルID/live
- https://www.youtube.com/watch?v=VideoID
    - ライブの状態・サムネ・チャンネル名・ライブ名・リンクURLはチャンネルIDから取得可能。
    - 開始時刻を取得したい場合はvideo:listのAPIを経由する必要がある。
