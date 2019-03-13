<h1 align="center"><font color="#B0E2FF">EPC_lot</font></h1>

<br>

<h3 align="center"><font color="#B0E2FF">想法虽小，重在践行！</font></h3>

<h4 align="center">像python一样简单方便，轻量级和快速是物联网世界的一门武术。</h4>

<br>

<hr>
<br>

<h3 align="center">EPC_lot架构图</h3>

<img src="https://wenhuan.oss-cn-beijing.aliyuncs.com/EPC_lot_%E6%A8%A1%E5%9E%8B%E5%9B%BE.png" >

<br>

> ##### EPC模型：`Erlang` + `Python` + `C` 



<h3 align="center">EMQ 消息服务器架构</h3>

<p align="center"><img src="https://wenhuan.oss-cn-beijing.aliyuncs.com/emqlogo.png" alt="EMQ-消息服务器架构" width="200"></p>

<br>

<h2 align="center"><font color="#B0E2FF">精准CNC！</font></h2>

> <center><h4>EPC架构是CNC行业的一次物联网尝试，我们对此有备而来，只为一个目标前行。</h4></center>

> 前端可视化研发中
>
> - - [ ] 新版本

> 消息持久化研发中 
>
> - - [x] 新版本
> - - [x] 本地化
> - - [x] 数据库持久化 

> 订阅持久化研发中
>
> - - [x] 新版本
> - - [x] 来自json

<hr>

> 依照EMQX消息服务器的架构，我们对其进行自动化调整。

> 尽管如此，EPC架构也依旧只是一个模块化功能。在不久的将来，我们将会使用`Golang`进行精准开发。针对CNC行业所需要的部署环境，从而实现一个高度自动化的`SAC`(消息服务器 + 代理 + 客户端)模型。

> 将在`WIKI`版本声明中指出` 添加 | 修改 | 删除 `的一些特性。  
> [更新声明] (https://github.com/haitanghuadeng/RHCNC.EPC_lot/wiki )

<hr>
<br>

<h2 align="center"><font color="#B0E2FF">低延时的架构处理！</font></h2>

> 在最近的开发测试中，EPC团队根据真实场景，对EPC_lot架构进行延时并发测试。

> `10s / 100KB`  |  `8~10包 / 1KB`  |  `持久化写入`  |  `单线程`



<p align="center"><img src="https://wenhuan.oss-cn-beijing.aliyuncs.com/%E5%8D%81%E6%AF%AB%E7%A7%92%E7%BA%A7%E5%BB%B6%E6%97%B6.png" alt="EMQ-消息服务器架构"></p>

> 尽管在场景中受到一些波动因素，但依旧借助`Python`和`Erlang`完成了消息处理。 
>
> `614包 / 100kB `, `均处理时间16ms/`, `持久化`

<hr>
<br>

<h2 align="center"><font color="#B0E2FF">粒度级别、亲缘和可寻址</font></h2>

> 粒度：在更新架构声明1.2中，提出。
>
> - - [x] 根据粒度级别设定，处理`publish / subscription`中`subscription`的订阅队列消息。
> - - [x] 无论传感器传输速率`↑↓`，作为集群节点依旧可以选择该主题的消息粒度级别。

> 亲缘：在更新架构声明1.2中，提出。
>
> - - [x] 在未来可预见的版本中，EPC将会把容器化理念融入。这将为亲缘关系提供一个可以依赖和借鉴的关系。

> 可寻址：在更新架构声明1.2中，提出。
>
> - - [x] 可寻址仅仅只是一个EMQ命令语句，但依旧为监管集群提供了一个方法。

