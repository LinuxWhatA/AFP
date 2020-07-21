#!/usr/bin/python3

import poplib
import time
import filelib
from email.parser import Parser
from email.header import decode_header
from email.header import Header


def charset(_name):
    h = Header(_name)
    dh = decode_header(h)
    _name, char = decode_header(str(dh[0][0], dh[0][1]))[0]
    if char:
        _name = _name.decode(char)
    return _name


class POP3:
    def __init__(self, _pop, _user, _pass):
        try:
            self.server = poplib.POP3(_pop)
            self.server.user(_user)
            self.server.pass_(_pass)
            self.sums = self.server.stat()[0]
            self.msg = self.start(self.sums)
        except Exception as E:
            print('连接错误，检查服务器、账号、密码')
            input(E)

    def start(self, index):
        msg = self.server.retr(index)
        msg = b'\r\n'.join(msg[1]).decode('utf-8')
        return Parser().parsestr(msg)

    def time(self, _type=2):
        if _type == 0:
            return self.msg.get("Date")[0:24]
        elif _type == 1:
            return time.strptime(self.msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S')
        elif _type == 2:
            return time.mktime(self.time(1))


if __name__ == '__main__':
    try:
        config = filelib.Config('config.ini')
        names = filelib.Namelist('名单.txt')
        server = POP3(config.list['server']['pop服务器'], config.list['server']['邮箱账号'], config.list['server']['独立密码'])
        for i in range(server.sums, 0, -1):
            server.msg = server.start(i)
            for part in server.msg.walk():
                if part.is_multipart():
                    continue
                name = part.get_param('name')
                if name:
                    name = charset(name)
                    subject = charset(server.msg.get("Subject"))
                    print('subject:', subject)
                    if not names.find(name):         # 判断附件名
                        name_last = names.name[3]    # [姓名, 学号姓名, 文件名, 文件后缀]
                        if not names.find(subject):  # 判断主题
                            print('break:', name)
                            continue
                        else:
                            names.find(f'{names.name[1]}.{name_last}')  # 主题匹配成功，加上附件的后缀
                    print('->', names.name[2])
    except Exception as E:
        input(E)

    # file_date = time.strptime(msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S')
    # charset(msg.get("Subject"))
    # part.get_payload(decode=True)
