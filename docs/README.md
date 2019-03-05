<br>

<h2 align="center"><font color="#B0E2FF">Small as the idea is, it is important to realize it</font></h2>

<center>Simple and convenient as python, lightweight and fast is a martial art for the Internet of things world.</center>

<hr>

<br>


```mermaid
graph LR
   EPC -- 应用层 --> WEB
   EPC -. 管理层 .-> DB
   EPC -- 研发回弹层 --- ALARM
   
```



<hr>

<br>

> ##### EPC模型：`Erlang` + `Python` + `C` 

```mermaid
graph LR
   Erlang -- 消息聚拢 --> EMQ
   Python -. 管理层 .-> WEB
   C -- 研发回弹层 --- ALARM
```

