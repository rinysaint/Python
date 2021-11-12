import os


def rename(dir):
    with open(dir) as lines:  # 一次性读入txt文件，并把内容放在变量lines中
        array = lines.readlines()  # 返回的是一个列表，该列表每一个元素是txt文件的每一行
        array2 = []  # 使用一个新的列表来装去除换行符\n后的数据
    for i in array:  # 遍历array中的每个元素
        oldpathfile = i.split(':')[0]
        newpathfile = i.split(':')[1]
        os.renames(oldpathfile, newpathfile)


if __name__ == '__main__':
    dir = 'E:\\PYWorkSpaces\\getmp3\\musics\\1\\namelist.txt'
    rename(dir)