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

# 接口详细文档
## 企业工商数据查询
* 企业关键字模糊查询
[接口文档地址](http://www.yjapi.com/DataApi/Api?apiCode=410)
```
>>> result, response = client.search(name="小桔科技")
>>> print(result)
[
    {
      "KeyNo": "4659626b1e5e43f1bcad8c268753216e",
      "Name": "北京小桔科技有限公司",
      "OperName": "程维",
      "StartDate": "2012-07-10T00:00:00",
      "Status": "存续（在营、开业、在册）",
      "No": "110108015068911",
      "CreditCode": "9111010859963405XW"
    },
    {
      "KeyNo": "4178fc374c59a79743c59ecaf098d4dd",
      "Name": "深圳市小桔科技有限公司",
      "OperName": "王举",
      "StartDate": "2015-04-22T00:00:00",
      "Status": "存续",
      "No": "440301112653267",
      "CreditCode": "91440300334945450M"
    },
    ...
]
```

# 其他
如有疑问或者需求提供其他接口，欢迎提交PR或者联系 [ramwin@qq.com](mailto:ramwin@qq.com)
