[English](../../en/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Deutsch](../../de/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Español](../../es/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Français](../../fr/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Italiano](../../it/09-raspberry-pi-agnss/baidu-map-api-key.md) | [日本語](../../ja/09-raspberry-pi-agnss/baidu-map-api-key.md) | [한국어](../../ko/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Português (BR)](../../pt-br/09-raspberry-pi-agnss/baidu-map-api-key.md) | [Português (PT)](../../pt-pt/09-raspberry-pi-agnss/baidu-map-api-key.md) | [简体中文](../../zh-hans/09-raspberry-pi-agnss/baidu-map-api-key.md) | 繁體中文

**百度地圖api申請教學**

**1.** **註冊方法**

進入百度地圖開放平台https://lbsyun.baidu.com/

滑動到頁面底端

點擊立即註冊

![img](../../en/09-raspberry-pi-agnss/images/19.jpg) 

建議選擇成為個人開發者（因為當天申請即可使用）

按照提示一步步完成即可

![img](../../en/09-raspberry-pi-agnss/images/20.jpg) 

**2. 取得ak**

我們使用的是web服務裡的 普通IP定位，文件可在下面的連接查閱。

https://lbsyun.baidu.com/index.php?title=webapi/ip-api

點擊 主控台，選擇 我的應用，選擇 建立應用。

![img](../../en/09-raspberry-pi-agnss/images/21.jpg) 

應用名隨便寫，應用類型選擇 伺服器端 ，啟用服務，白名單輸入一個 0.0.0.0/0。

![img](../../en/09-raspberry-pi-agnss/images/22.jpg) 

點擊 提交 產生一個應用。

![img](../../en/09-raspberry-pi-agnss/images/23.jpg) 

複製我們應用的ak值

![img](../../en/09-raspberry-pi-agnss/images/24.jpg) 

貼上在程式裡，儲存，即可透過百度地圖讀取到位置資訊。

![img](../../en/09-raspberry-pi-agnss/images/25.jpg) 