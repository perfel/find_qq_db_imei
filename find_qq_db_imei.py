# -*- coding: utf-8 -*-
# @Time   : 2020/04/01
# @Author : perfel
# @Desc   : 手动求解手机QQ sqlite数据文件的加密IMEI值

import sqlite3

class FindImei:
    def __init__(self, arg):
        self.db_file = arg.db_file
        self.key_length = arg.key_length
        self.limit_rows = arg.limit_rows
        self.init_imei = arg.init_imei
        self.user_qq = arg.user_qq

        self.start_pos = 0
        self.imei = 'x' * self.key_length
        self.conn = None
        self.curs = None
        self.init_data()

    # 初始数据
    def init_data(self):
        self.conn = sqlite3.connect(self.db_file)
        self.curs = self.conn.cursor()

        if len(self.user_qq) > 0:
            self.init_imei = self.decode_qq_imei(self.user_qq)
        self.start_pos = len(self.init_imei)
        self.imei = self.init_imei + 'x' * (self.key_length - self.start_pos)

        print(f'\n文件路径：{self.db_file} \n求解IMEI长度：{self.key_length} \n初始IMEI值：{self.imei} \n起始位置：{self.start_pos}')
        print(f'文件所属用户QQ：{self.user_qq}')

    # 使用qq号求解部分imei
    def decode_qq_imei(self, qq):
        sql = 'select uin from Ability'
        uin = self.curs.execute(sql).fetchone()[0]

        v_min_len = len(qq) if len(qq) < len(uin) else len(uin)

        ret = ''
        for i in range(0, v_min_len):
            xor = ord(qq[i]) ^ ord(uin[i])
            ret = ret + chr(xor)
        return ret

    # 打印信息
    def print_info(self, tup, pos, imeis):
        for num in range(0, 10):
            imeis[pos] = str(num)
            imei = ''.join(imeis)

            tmp = f'[{num}] || '
            for it in tup:
                data = self.decode(it, imei)[:pos+1]
                tmp = f'{tmp} || {data}'
            tmp = f'{tmp} || [{num}]'
            print(tmp)

    # 手动求解
    def manual_start(self):
        sql = f'select remark, mCompareSpell from Friends order by length(remark) desc limit {self.limit_rows}'
        rst = self.curs.execute(sql).fetchall()
        imeis = [it for it in self.imei]
        pos = self.start_pos

        v_len = len(imeis)
        print(v_len)
        while pos < v_len:

            imeis[pos] = '[X]'
            self.imei = ''.join(imeis)
            print('\n## 当前位置:', pos)
            print('## 当前IMEI:', self.imei)

            for tup in rst:
                self.print_info(tup, pos, imeis.copy())
                print('')

            print('选择最后字符显示正确序号：', end=' ')
            while True:
                value = input()
                if value.isdigit() and int(value) >= 0 and int(value) <= 10:
                    imeis[pos] = value
                    pos += 1
                    break
                elif value.lower() == 'x':
                    if pos > 0:
                        imeis[pos] = 'x'
                        pos -= 1
                    break
                else:
                    print('输入值错误，请重新输入[x] [0-9]:', end=' ')

        self.imei = ''.join(imeis)
        print('求解出的IMEI值为：', self.imei, '\n')
        return self.imei

    # 使用指定imei解密数据
    def decode(self, data, imei):
        ret = ''
        if isinstance(data, str):
            for i in range(0, len(data)):
                xor = ord(data[i]) ^ ord(imei[i % 15])
                ret = ret + chr(xor)
        return ret


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='QQ聊天记录db文件获取解密key(IMEI)')
    parser.add_argument('db_file', type=str, help='db文件路径')
    parser.add_argument('-l', type=int, default=15,
                        dest="key_length", help='需要解出的IMEI长度值')
    parser.add_argument('-n', type=int, default=2,
                        dest="limit_rows", help='需要查看的组数')
                        
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', type=str, default='',
                       dest="init_imei", help='初始前几位IMEI值')
    group.add_argument('-q', type=str, default='',
                       dest="user_qq", help='db文件所属用户qq号,以求解前几位IMEI')

    args = parser.parse_args()

    ant = FindImei(args)
    ant.manual_start()

