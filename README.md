# find_qq_db_imei
推导出手机qq数据库db文件的加密IMEI值

```
py find_qq_db_imei.py -h
usage: find_qq_db_imei.py [-h] [-l KEY_LENGTH] [-n LIMIT_ROWS]
                          [-i INIT_IMEI | -q USER_QQ]
                          db_file

QQ聊天记录db文件获取解密key(IMEI)

positional arguments:
  db_file        db文件路径

optional arguments:
  -h, --help     show this help message and exit
  -l KEY_LENGTH  需要解出的IMEI长度值(默认15)
  -n LIMIT_ROWS  需要查看的组数(默认2)
  -i INIT_IMEI   初始前几位IMEI值
  -q USER_QQ     db文件所属用户qq号,以求解前几位IMEI

```

必输项：db_file  qq聊天db数据文件

可选项：

| 序号 | 命令项 | 默认值 | 注释                 |
| ---- | ------ | ------ | -------------------- |
| 1    | -h     |        | 帮助                 |
| 2    | -l     | 15     | 需要推导的IMEI值长度 |
| 3    | -n     | 2      | 对比查看的组数       |
| 3    | -i     |        | 初始前几位IMEI       |
| 4    | -q     |        | 用户QQ号             |



### 使用实例

**根据输出结果，输入解密正确的 0-9 数值**

1. 基本操作

   `py find_qq_db_imei.py 'E:\1234567.db'`

2. 设置返回对比组数

   `py find_qq_db_imei.py 'E:\1234567.db' -n 1`

3. 设置初始IMEI

   `py find_qq_db_imei.py 'E:\1234567.db' -n 1 -i 86332`

4. 设置db文件的用户qq号

   `py find_qq_db_imei.py 'E:\1234567.db' -n 1 -q 9876`

   

