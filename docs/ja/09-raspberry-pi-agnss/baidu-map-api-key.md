[English](../../en/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Deutsch](../../de/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Español](../../es/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Français](../../fr/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Italiano](../../it/09-raspberry-pi-agnss/baidu-map-api-key.md) | 日本語 | [한국어](../../ko/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Português (BR)](../../pt-br/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Português (PT)](../../pt-pt/09-raspberry-pi-agnss/baidu-map-api-key.md) | [简体中文](../../zh-hans/09-raspberry-pi-agnss/baidu-map-api-key.md) | [繁體中文](../../zh-hant/09-raspberry-pi-agnss/baidu-map-api-key.md)

**Baidu Map API キーの申請**

**1. アカウント登録**

Baidu Map オープンプラットフォームへアクセスします：<https://lbsyun.baidu.com/>

ページの最下部までスクロールし、「Register now」をクリックします。

![登録](../../en/09-raspberry-pi-agnss/images/19.jpg)

個人開発者として登録することを推奨します。キーを当日中に使用できるためです。

画面の指示に従って登録を完了します。

![登録手順](../../en/09-raspberry-pi-agnss/images/20.jpg)

**2. AK の取得**

ここで使用するのは Web Service API の IP 位置情報サービスです。そのドキュメントは次のとおりです：

<https://lbsyun.baidu.com/index.php?title=webapi/ip-api>

**コンソール**をクリックし、**マイアプリケーション**を選択してから**アプリケーションを作成**をクリックします。

![コンソール](../../en/09-raspberry-pi-agnss/images/21.jpg)

アプリケーションに任意の名前を付け、アプリケーション種別で**サーバーサイド**を選択し、サービスを有効化して、ホワイトリストに `0.0.0.0/0` を入力します。

![アプリケーションの作成](../../en/09-raspberry-pi-agnss/images/22.jpg)

**Submit** をクリックしてアプリケーションを作成します。

![送信済み](../../en/09-raspberry-pi-agnss/images/23.jpg)

アプリケーションの AK 値をコピーします。

![AK のコピー](../../en/09-raspberry-pi-agnss/images/24.jpg)

プログラムに貼り付けて保存します。これで Baidu Map を通じて測位情報を読み取れるようになります。

![AK の貼り付け](../../en/09-raspberry-pi-agnss/images/25.jpg)
