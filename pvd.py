from math import *
import os
from random import random
from PIL import Image
import re

l_k = [0, 8, 16, 32, 64, 128, 256]  #区间下界，最后的256为了统一操作
w_k = [8, 8, 16, 32, 64, 128]  #区间长度


def StringtoBit(string):
    return ''.join(bin(ord(c)).replace('0b', '').rjust(8, '0') for c in string)


# 将二进制字符串bitstr转换为字符串
def BittoString(bitstr):
    if (len(bitstr) % 8 != 0):
        print("Invail bit string!")
        exit(0)
    i = len(bitstr) // 8
    return ''.join(
        chr(int(bitstr[8 * j:8 * (j + 1)], 2)
            ) if int(bitstr[8 * j:8 *
                            (j + 1)], 2) in range(ord('A'), ord('Z'))
        or int(bitstr[8 * j:8 * (j + 1)], 2) in range(ord('a'), ord('z'))
        or int(bitstr[8 * j:8 *
                      (j + 1)], 2) in range(ord('0'), ord('9')) else ''
        for j in range(i))


def PVD(path, new_path, data):
    im = Image.open(path)
    data = '00' + data + '00'  #用00包围秘密信息
    data = StringtoBit(data)
    width = im.size[0]
    height = (im.size[1] // 2) * 2  #抛弃不成对的像素
    pi = 0  #下一次要读取的位置
    for w in range(width):
        for h in range(0, height - 1, 2):
            pixel1 = im.getpixel((w, h))
            pixel2 = im.getpixel((w, h + 1))
            diff_old = pixel2 - pixel1
            diff_index = 0
            #确定差值所在区间
            for diff_index in range(len(w_k)):
                if (abs(diff_old) >= l_k[diff_index]
                        and abs(diff_old) < l_k[diff_index + 1]):
                    break
            #秘密信息位数
            data_len = int(log2(w_k[diff_index]))
            if pi + data_len >= len(data):
                data_len = len(data) - pi
            data_temp = data[pi:pi + data_len]
            data_num = int(data_temp, 2)
            btm = l_k[diff_index]  #l_k
            #计算新的差值
            diff_new = btm + data_num if (diff_old >= 0) else -(btm + data_num)
            #分摊差值
            diff_change = (diff_new - diff_old) / 2
            pixel1_new = pixel1 - ceil(diff_change) if (
                diff_old % 2 == 1) else pixel1 - floor(diff_change)
            pixel2_new = pixel2 + floor(diff_change) if (
                diff_old % 2 == 1) else pixel2 + ceil(diff_change)
            im.putpixel((w, h), pixel1_new)
            im.putpixel((w, h + 1), pixel2_new)
            pi += data_len
            if (pi >= len(data)):
                im.save(new_path)
                return


def decode(path):
    data = ''
    im = Image.open(path)
    width = im.size[0]
    height = (im.size[1] // 2) * 2  #抛弃不成对的像素
    for w in range(width):
        for h in range(0, height - 1, 2):
            pixel1 = im.getpixel((w, h))
            pixel2 = im.getpixel((w, h + 1))
            diff = pixel2 - pixel1
            diff_index = 0
            #确定差值所在区间
            for diff_index in range(len(l_k) - 1):
                if (abs(diff) >= l_k[diff_index]
                        and abs(diff) < l_k[diff_index + 1]):
                    break
            secret = abs(diff) - l_k[diff_index]
            data_len = int(log2(w_k[diff_index]))
            data_temp = bin(secret).replace('0b', '').rjust(data_len, '0')
            data = data + data_temp
    data = data + ''.join('0' for i in range(8 - len(data) % 8))
    print(BittoString(data))


def PVD_exec():
    path = input("Input the path of image:")
    while (os.path.exists(path) == False):
        path = input(path + " does not exists , please input again:")
    new_path = input("Input save path:")
    data = input("Input message to insert:")
    while (PVD(path, new_path, data) == False):
        data = input("Input message:")
    print("New image saved to:" + new_path)
    print("Decode :")
    decode(new_path)


PVD_exec()