# -*- coding: utf-8 -*-
# @Time   : 2020/04/01
# @Author : perfel
# @Desc   : 手动求解手机QQ sqlite数据文件的加密IMEI值

import sqlite3

class FindImei:
    V_SQL_ABILITY = 'select uin from Ability'
    V_SQL_AUTO = '''select coalesce(remark,name), mCompareSpell 
                         from Friends 
                         order by length(mCompareSpell) desc'''
    V_SQL_MANUAL = '''select coalesce(remark,name), mCompareSpell 
                         from Friends 
                         order by length(mCompareSpell) desc 
                         limit {0}'''
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


    # 使用指定imei解密数据
    def decode(self, data, imei):
        ret = ''
        if isinstance(data, str):
            for i in range(0, len(data)):
                xor = ord(data[i]) ^ ord(imei[i % 15])
                ret = ret + chr(xor)
        return ret


    # 使用qq号推导部分imei
    def decode_qq_imei(self, qq):
        uin = self.curs.execute(FindImei.V_SQL_ABILITY).fetchone()[0]
        v_min_len = len(qq) if len(qq) < len(uin) else len(uin)

        ret = ''
        for i in range(0, v_min_len):
            xor = ord(qq[i]) ^ ord(uin[i])
            ret = ret + chr(xor)
        return ret


    # 打印信息
    def print_info(self, tup, pos, imeis):
        for i in range(0, 10):
            imeis[pos] = str(i)
            imei = ''.join(imeis)

            tmp = f'[{i}]'
            for it in tup:
                data = self.decode(it, imei)[:pos+1]
                tmp = f'{tmp} || {data}'
            tmp = f'{tmp} || [{i}]'
            print(tmp)


    # 手动推导
    def manual_find(self):
        sql = FindImei.V_SQL_MANUAL.format(self.limit_rows)
        rows = self.curs.execute(sql).fetchall()
        v_imeis = [it for it in self.imei]
        v_len = len(v_imeis)
        pos = self.start_pos

        while pos < v_len:

            v_imeis[pos] = '[X]'
            self.imei = ''.join(v_imeis)

            print('\n[位置]:', pos, '[IMEI]:', self.imei)
            
            for tup in rows:
                print('--------------------------')
                self.print_info(tup, pos, v_imeis.copy())
                print('--------------------------')


            print('\n选择最后字符显示正确的序号值：', end=' ')
            while True:
                value = input()
                if value.isdigit() and int(value) >= 0 and int(value) <= 10:
                    v_imeis[pos] = value
                    pos += 1
                    break
                elif value.lower() == 'x':
                    if pos > 0:
                        v_imeis[pos] = 'x'
                        pos -= 1
                    break
                else:
                    print('输入值错误，请重新输入字母[x] 或 数字[0-9]:', end=' ')

        self.imei = ''.join(v_imeis)
        print('\n推导出的IMEI值为：', self.imei, '\n')
        return self.imei

    # 找到指定位置可以匹配的imei列表
    def find_match_imeis(self, p_name, p_spell, p_imei, p_pos, p_py):
        v_imeis = [ it for it in p_imei]
        name = p_name[:p_pos+1]
        spell = p_spell[:p_pos+1]
        p = p_py
        keys = []

        print(f'[{p_pos:2d}]', p_imei)
        for i in range(0, 10):
            v_imeis[p_pos] = str(i)
            imei = ''.join(v_imeis)
            dec_name = self.decode(name, imei)
            dec_spell = self.decode(spell, imei)

            py_name = p.get_pinyin(dec_name, '').lower()
            # 名字对应的拼音是否不是字母数字
            if not py_name[:p_pos+1].encode().isalnum():
                continue
            elif py_name[:p_pos+1] == dec_spell:
                keys.append(imei)
                print(f'[{p_pos:2d}] | [{i}] | {py_name[:20]:20s} |---| {dec_spell:15s} | {dec_name} ' )

        if len(keys) == 0:
            print('# 发现特殊符号或不匹配,跳过此数据')
            return None
        else:
            return keys

    # 自动推导
    def auto_find(self):
        from xpinyin import Pinyin

        rows = self.curs.execute(FindImei.V_SQL_AUTO).fetchall()
        py = Pinyin()
        # 遍历所有好友数据   
        for item in rows:
            s_name, s_spell = item
            imei_list = [self.imei]
            pos = 0
            while pos < self.key_length:
                vlist = []
                for imei in imei_list:
                    ret_imei_list = self.find_match_imeis(s_name, s_spell, imei, pos, py)
                    if ret_imei_list is None:
                        break
                    else:
                        vlist.extend(ret_imei_list)

                imei_list = vlist.copy()
                if len(vlist)>0:
                    pos += 1
                else:
                    break

            # 找到imei则退出遍历
            if len(imei_list) == 1:
                break

        if len(imei_list) == 1:
            self.imei = imei_list[0]
            print(f'\n恭喜！ 找到IMEI值：{self.imei}\n')
        else:
            print('\n失败！未找到IMEI值，请使用手动模式...\n')

        return self.imei



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='QQ聊天记录db文件获取解密key(IMEI)')
    parser.add_argument('db_file', type=str, help='db文件路径')
    parser.add_argument('-l', type=int, default=15,
                        dest="key_length", help='需要推导的IMEI长度值(默认15)')
    parser.add_argument('-m', type=int, default=1,
                        dest="model", help='操作模式：1 自动(默认) 2 手动')
    parser.add_argument('-n', type=int, default=2,
                        dest="limit_rows", help='需要查看的组数(默认2)')


    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', type=str, default='',
                       dest="init_imei", help='初始前几位IMEI值')
    group.add_argument('-q', type=str, default='',
                       dest="user_qq", help='db文件所属用户qq号,以求解前几位IMEI')

    args = parser.parse_args()

    fd = FindImei(args)
    if args.model == 1:
        fd.auto_find()
    else:
        fd.manual_find()
