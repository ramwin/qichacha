**Xiang Wang @ 2019-02-18 15:41:48**

企查查api文档

# 安装步骤
1. [申请自己的数据](http://www.yjapi.com/DataCenter/ApplyData#)
2. 安装
```
    pip install qichacha
```
3. 创建client
```
from qichacha import QichachaClient
client = QichachaClient(key="您的key", secretkey="您的密钥", logger="您的logger，可以不填")
```
4. 调用接口
```
client.search(name="小桔科技")
```
