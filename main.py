import os
import json
import requests
from os.path import join, dirname
from dotenv import load_dotenv


def main():
    # .envから環境変数を読み込み
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    token = os.environ.get("TOKEN")
    host = os.environ.get("HOST")
    # ランキング初期化
    ranking = {}
    # チャンネルリストを取得・整形
    url = host + 'channels.list?token=' + token + '&exclude_archived=true'
    r = requests.get(url)
    data = r.json()
    channels = [{'id': channel['id'], 'name': channel['name']}
                for channel in data['channels']]
    for channel in channels:
        # 各チャンネルから上位1000件を取得する
        url = host + 'channels.history?token=' + \
            token + '&channel=' + channel['id'] + '&count=1000'
        r = requests.get(url)
        data = r.json()

        # reactionを取得
        try:
            for message in data['messages']:
                try:
                    for reaction in message['reactions']:
                        if reaction['name'] not in ranking:
                            ranking[reaction['name']] = reaction['count']
                        else:
                            ranking[reaction['name']] += reaction['count']
                except KeyError:
                    pass
        except KeyError:
            pass
    # 並び替え
    ranking_sorted = sorted(
        ranking.items(), key=lambda x: x[1], reverse=True)
    # ターミナルでは収まりきらないのでファイルに保存する
    with open(dirname(__file__) + 'output.txt', mode='w') as f:
        f.write(json.dumps(ranking_sorted))


if __name__ == '__main__':
    main()
