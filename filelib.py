#!/usr/bin/python3
import re
import zipfile
import rarfile
from os.path import splitext

def file_add(filename, add):
    return f'{splitext(filename)[0]}({add}){splitext(filename)[1]}'

class Namelist:
    def __init__(self, file):
        self.file = file
        self.name = ['', '', '', '']  # [姓名, 学号姓名, 文件名, 文件后缀]

    def find(self, filename):
        self.name[3] = splitext(filename)[1]
        for line in open(self.file, encoding='utf-8'):
            line = re.search(r'(.*?)([\u4E00-\u9FA5]+)', line)
            if line.group(2) in filename:
                self.name[0] = line.group(2)
                self.name[1] = line.group()
                self.name[2] = line.group() + self.name[3]
                return True


class Archive:
    def __init__(self, file, type='r'):
        self.list = []
        try:
            if splitext(file)[1] == '.zip':
                file = zipfile.ZipFile(file, type)
            elif splitext(file)[1] == '.rar':
                file = rarfile.RarFile(file, type)
            self.file = file
            self.look()
        except:
            pass

    def __del__(self):
        self.file.close()

    def look(self):
        for file in self.file.namelist():
            try:
                file = file.encode('cp437').decode('gbk')
            except:
                file = file.encode('utf-8').decode('utf-8')
            self.list.append(file)
        return self.list

    def check_pack(self):
        config = Config('config.ini')
        for lists in self.list:
            for key in config.list['file'].keys():
                if key in splitext(lists)[1]:
                    return config.list['file'][key]


class Config:
    def __init__(self, file):
        self.list = {}
        for line in open(file, encoding='utf-8'):
            line = re.sub(r'\s', '', line)  # 去除空白字符
            if not line:  # 跳过空行
                continue
            if re.search(r'\[(.*)\]', line):  # 查找 [   ] 格式
                option = re.search(r'\[(.*)\]', line).group(1)
                self.list[option] = {}
                continue
            key, value = line.split('=')
            try:
                self.list[option][key] = value
            except Exception as E:
                input(f'self.list[option][key] = value\n{E}')
        self.file = file
    
    def write(self, option, key, value):
        if not self.list.get(option):
            self.list[option] = {}
        self.list[option][key] = value
        with open(self.file, 'w', encoding='utf-8') as file:
            for option in self.list.keys():
                file.write(f'[{option}]\n')
                for key in self.list[option].keys():
                    file.write(f'{key} = {self.list[option][key]}\n')
                file.write('\n')

    def find(self, name, option='file'):
        for key in self.list[option].items():
            for value in key:
                if value in name:
                    return key
        return '', ''


if __name__ == '__main__':
    names = Namelist('名单.txt')
    config = Config('config.ini')
    print(config.find('刘志5.思12.doc'))
    # print(config.list['api']['AppID'])
