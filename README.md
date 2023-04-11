# RaspberryPiを使用したLINEbot
![image](https://d20r2glx6euv0l.cloudfront.net/editor/0bea064010fb16da.jpg)
![image](https://d20r2glx6euv0l.cloudfront.net/thumbnail/293f828a7810306c.png)

**1. 制作物の動作概要**

ラズパイにngrokとWebhhokを利用してLINEmessagingAPIが動作する環境を用意し、デバイス(スマホやPC)から「LINEトーク」の対話形式でラズベリーパイにコマンドを送るシステム。

今回用意したコマンドは「モーションカメラ」,「ラズパイCPU温度測定」,「カチューシャ(サウンド)」,「じゃんけん(ミニゲーム)」,「人感センサー」,「カメラ(撮影)」の6つ。

**2.使用した技術**

・ngrok

・Webhook

・LINEmessagingAPI

・Python3.x



**3.用意した機器**

・RasberryPiZero

・ブレッドボード

・ジャンパー

・人感センサー

・ブザー

・RasberryPiカメラ

・スマートフォン(LINE)

## 苦労した点
まずは、ラズパイ内に構築するLINEmessagingAPIの環境作りである。特にLINEmessagingAPIで指定するwebhook先のサーバーをラズベリーパイ内で構築するところが、最初の大きな躓きであった。しかし、「ngrok」と呼ばれるwebhookを利用するためのpublicURLを発行してくれるサービスを使うことにより解決した。次に苦労した点は、LINEBOTを細かく扱うことができる「line-bot-sdk」と呼ばれるパッケージの活用だ。これはオープンソースであるため、web上にはある程度の使い方や作品例などは挙がっていた。しかし、上記で挙げたコマンド全てを実装するのには0からコーディングする必要があった。
