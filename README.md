```λ  py find_qq_db_imei.py -h
usage: find_qq_db_imei.py [-h] [-l KEY_LENGTH] [-m MODEL] [-n LIMIT_ROWS]
                          [-i INIT_IMEI | -q USER_QQ]
                          db_file

QQ聊天记录db文件获取解密key(IMEI)

positional arguments:
  db_file        db文件路径

optional arguments:
  -h, --help     show this help message and exit
  -l KEY_LENGTH  需要推导的IMEI长度值(默认15)
  -m MODEL       操作模式：1 自动(默认) 2 手动
  -n LIMIT_ROWS  需要查看的组数(默认2)
  -i INIT_IMEI   初始前几位IMEI值
  -q USER_QQ     db文件所属用户qq号,以求解前几位IMEI

```

必输项：db_file  qq聊天db数据文件

可选项：

| 序号 | 命令项 | 默认值 | 注释                   |
| ---- | ------ | ------ | ---------------------- |
| 1    | -h     |        | 帮助                   |
| 2    | -l     | 15     | 需要推导的IMEI值长度   |
| 3    | -n     | 2      | 对比查看的组数         |
| 3    | -i     |        | 初始前几位IMEI         |
| 4    | -q     |        | 用户QQ号               |
| 5    | -m     | 1      | 推导模式 1 自动 2 手动 |



### 使用实例

**根据输出结果，输入解密正确的 0-9 数值**

**自动模式**下只需指定db文件路径就可以

1. 基本操作

   `py find_qq_db_imei.py 'E:\1234567.db'`

   `py find_qq_db_imei.py 'E:\1234567.db' -m2`

2. 设置返回对比组数

   `py find_qq_db_imei.py 'E:\1234567.db' -m2 -n1`

3. 设置初始IMEI

   `py find_qq_db_imei.py 'E:\1234567.db' -m2 -n1 -i 86332`

4. 设置db文件的用户qq号

   `py find_qq_db_imei.py 'E:\1234567.db' -m2 -n 1 -q 9876`

------------------------ 20210616--------------------------------
用新手机测试了下，竟然没有推出来IMEI, 最后发现IMEI竟然是02:00:00:00:00: 所以除了0-9外添加冒号的推导

   
