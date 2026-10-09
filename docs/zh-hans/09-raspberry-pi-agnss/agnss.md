[English](../../en/09-raspberry-pi-agnss/agnss.md) | [Deutsch](../../de/09-raspberry-pi-agnss/agnss.md) | [Español](../../es/09-raspberry-pi-agnss/agnss.md) | [Français](../../fr/09-raspberry-pi-agnss/agnss.md) | [Italiano](../../it/09-raspberry-pi-agnss/agnss.md) | [日本語](../../ja/09-raspberry-pi-agnss/agnss.md) | [한국어](../../ko/09-raspberry-pi-agnss/agnss.md) | [Português (BR)](../../pt-br/09-raspberry-pi-agnss/agnss.md) | [Português (PT)](../../pt-pt/09-raspberry-pi-agnss/agnss.md) | 简体中文 | [繁體中文](../../zh-hant/09-raspberry-pi-agnss/agnss.md)

**AGNSS辅助定位**

**1. 学习目标**

本次课程我们主要学习使用树莓派和GPS模块和agnss服务器实现弱信号下位置信息读取解析。

**2. AGNSS说明**

2.1. **为什么要用AGNSS**

• 自主式GNSS接收机定位的条件包括：

\- 捕获并跟踪卫星信号，解析时间

\- 从卫星获取电文

• 强信号环境，自主式GNSS接收机可以在30秒左右冷启动定位；但是在弱信号环境，无外部辅助的接收机捕获卫星很慢，很难从卫星获取电文，因此需要很久才能定位，甚至无法定位。

• AGNSS可以为接收机提供定位必需的辅助信息，比如电文，粗略位置和时间。不管是在强信号还是弱信号环境，这些信息可以显著的缩短首次定位时间。

2.2. **AGNSS解决方案**

• AGNSS服务器从多个GNSS数据源获取并管理AGNSS辅助信息。服务器时刻监听并响应客户端的AGNSS请求（需要用户名和密码）。

• 用户通过TCP/IP协议从AGNSS服务器获取辅助信息，获取到辅助信息可以直接传输给GNSS接收机。

• 用户也可以建立自己的代理服务器。

![img](../../en/09-raspberry-pi-agnss/images/1.png) 

2.3. **AGNSS流程**

• 连接AGNSS服务器

–服务器的地址为121.41.40.95(域名：www.gnss-aide.com)

–端口号为2621

• 发送AGNSS请求

–请求语句：(用户名和密码字段是必需项)

–user=<your-username>;pwd=<your-password>;cmd=full;gnss=gps+bd;lat=60.0;lon=55.0;alt=0;

• 获取AGNSS辅助信息

• 把AGNSS辅助信息发送给接收机

2.4. **AGNSS请求参数**

• 用户端发送请求到AGNSS服务器，请求语句的格式如下

–请求语句是多组key=value;的组合，如：key=value;key=value;

• 示例：user=<your-username>;pwd=<your-password>;cmd=full;gnss=gps+bd;lat=60.0;lon=55.0;alt=0;

• 具体的key和value定义如下表

| 关键字(Key) | 取值(value) | 可选性 | 备注                                                         |
| ----------- | ----------- | ------ | ------------------------------------------------------------ |
| **user**    | 字符串      | 必须   | 用户名。强烈建议用户名为一个有效的邮箱地址，重要的AGNSS服务器维护信息将会发送到该邮箱。 |
| **pwd**     | 字符串      | 必须   | 用户密码                                                     |
| **gnss**    | 字符串      | 可选   | 用逗号隔开的GNSS列表，目前支持GPS。有效的取值有：gps,bds,glo”gnss=gps;”表示请求GPS辅助信息；gnss=gps,bds;”表示请求GPS和BDS辅助信息； |
| **cmd**     | 字符串      | 可选   | full:全部信息，包括星历，估计的时间和位置eph:仅提供星历信息aid:辅助时间、位置等信息此项若不填，默认为full |
| **lat**     | 数值        | 可选   | 用户位置纬度的估计值。纬度的单位：度。取值范围是-90~90度。两者位置辅助格式，经纬高格式和ECEF格式，二选一。有效的经纬高位置辅助格式是”lat=30;lon=120.3;alt=100;”三个字段都必须完整。 |
| **lon**     | 数值        | 可选   | 用户位置经度的估计值。经度的单位：度。取值范围是-180~180度。 |
| **alt**     | 数值        | 可选   | 用户位置高度的估计值。单位:米。                              |
| **x**       | 数值        | 可选   | 用户位置（ECEF坐标系下的X,Y,Z）的估计值。单位:米。有效的ECEF位置辅助格式是”x=30000;y=1111120.3;z=3345100;”三个字段都必须完整。 |
| **y**       | 数值        | 可选   | 用户位置（ECEF坐标系下的X,Y,Z）的估计值。单位:米。           |
| **z**       | 数值        | 可选   | 用户位置（ECEF坐标系下的X,Y,Z）的估计值。单位:米。           |
| **pacc**    | 数值        | 可选   | 用户位置的准确度。单位为米。                                 |

2.5. **服务器返回信息**

![img](../../en/09-raspberry-pi-agnss/images/2.png) 

• AGNSS服务器返回的数据示例：数据头+辅助数据内容

• 二进制数据就是GNSS接收机所需的辅助数据，这些二进制数据中都自带了数据校验。二进制数据格式参考中科微的接收机协议规范。

• 如果把数据头也发送给了GNSS接收机，不会对GNSS接收机产生影响。

2.6. **AGNSS性能对比**

• 相比普通的独立式GNSS接收机，AGNSS接收机在TTFF性能上具有显著的提升，尤其是在弱信号条件下。

![img](../../en/09-raspberry-pi-agnss/images/3.jpg) 

2.7. **注意事项**

• 粗略位置辅助需要用户端通过其它方式获取，比如

–GSM/GPRS/3G通信模块，这些模块都可以利用CELL ID的方式获取当前粗略的位置

–WiFi等其它无线模块，也可以粗略定位

• 粗略位置的精度要求在15km以内，错误的位置辅助会影响接收机的性能

• 如果无法获取粗略位置，在AGNSS请求语句中忽略位置的字段（lat,lon,alt,x,y,z)，接收机会自动选择历史定位的有效位置

• 没有必要把GNSS接收机自己输出的位置作为粗略位置

2.8. **什么时候需要AGNSS**

• 不需要每次开机都从服务器下载，节省流量

–中科微的芯片内部有电池备份SRAM，以及永久备份FLASH，都可以自动保存接收到星历数据等

–芯片在正常工作中，不断的从卫星下载最新的星历数据

• 通过查询接收机的状态，决定是否需要从服务器下载AGNSS数据

–接收机可以输出电文状态语句（默认不输出，需要配置才输出）

2.9. **电文状态语句介绍**

![img](../../en/09-raspberry-pi-agnss/images/4.png) 

![img](../../en/09-raspberry-pi-agnss/images/5.png) 

• 该语句输出的是当前接收机内部的时间+电文状态。

• 可以发送命令$PCAS03,,,,,,,,,,,1*1F，每秒输出一次电文状态语句

• 可以发送命令$PCAS03,,,,,,,,,,,0*1E，停止输出电文状态语句

• 注意：每条语句后面都必须\r\n结尾(0x0D,0x0A)，语句中有11个逗号

• 如果时间标志有效（非0），且有效星历数目很多（大于8个），就不必下载AGNSS星历了。

 

**3. 课前准备**

**3.1. 接线**

GPS模块采用的是UART通讯或USB通讯，这里以USB通讯为例。

![img](../../en/09-raspberry-pi-agnss/images/6.png)

使用type-c线连接树莓派和GPS模块，运行命令 ls /dev | grep 'ttyUSB' ，可以看到识别到GPS模块为USB0

![img](../../en/09-raspberry-pi-agnss/images/7.png) 

**3.2. 申请百度地图ak**

请看文档 [百度地图api申请教程](baidu-map-api-key.md)

 

**4. 程序**

本次课程的程序请参考：GPS-agnss.py

初始化USB：

![img](../../en/09-raspberry-pi-agnss/images/8.jpg) 

资料ak需要填上自己申请的ak值，然后就能通过百度地图获得当前粗略的经纬度信息

![img](../../en/09-raspberry-pi-agnss/images/9.jpg) 

这里把百度地图获取到的粗略经纬度信息发送给服务器，请填入你自己的 AGNSS 账号，获取完成之后把整个包发送给模块

![img](../../en/09-raspberry-pi-agnss/images/10.jpg) 

![img](../../en/09-raspberry-pi-agnss/images/11.jpg) 

位置信息获取和解析函数，下图中在位置信息中筛选出GNGGA开头的位置信息，然后解析出数据存到各个全局变量中。

![img](../../en/09-raspberry-pi-agnss/images/12.jpg) 

![img](../../en/09-raspberry-pi-agnss/images/13.jpg) 

同样的方法获取了GNVTG的航向信息并解析。

![img](../../en/09-raspberry-pi-agnss/images/14.jpg) 

解析后的数据循环打印

![img](../../en/09-raspberry-pi-agnss/images/15.jpg) 

**5.运行程序**

终端输入sudo python2 GPS-agnss.py运行程序。

**6.实验现象**

**注意，辅助定位下树莓派必须联网。**

模块在弱信号下通电后，开始初始化USB，初始化成功显示“GPS Serial Opened! Baudrate=9600”，否则显示“GPS Serial Open Failed!”，如果错误需要检查接线或USB端口。

之后显示"GPS Agnss start"开始将辅助定位信息发送给服务器，发送完成之后显示"GPS Agnss success"

在发送之后的一段时间内还未读取到GPS信号，此时显示"GPS no found"并且打印百度地图读取到的粗略经纬度信息。

![img](../../en/09-raspberry-pi-agnss/images/16.jpg) 

过一段时间识别到GPS之后，识别会循环打印位置和航向信息。

![img](../../en/09-raspberry-pi-agnss/images/17.jpg) 

按Ctrl+C退出信息读取。

![img](../../en/09-raspberry-pi-agnss/images/18.jpg) 