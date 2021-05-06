# DES 加解密實現
# 所有內容都以str作為bin運算

import random
import sys

def KeyGenerator(bits):
  key = ''
  for i in range(0, bits):
    key = key + str(random.randint(0, 1))
  return key

def IPTransfer(msg):
  transfer_table = [
                    57, 49, 41, 33, 25, 17, 9, 1, 
                    59, 51, 43, 35, 27, 19, 11, 3, 
                    61, 53, 45, 37, 29, 21, 13, 5, 
                    63, 55, 47, 39, 31, 23, 15, 7, 
                    56, 48, 40, 32, 24, 16, 8, 0, 
                    58, 50, 42, 34, 26, 18, 10, 2, 
                    60, 52, 44, 36, 28, 20, 12, 4, 
                    62, 54, 46, 38, 30, 22, 14, 6
                   ]
  temp_msg = ''
  for i in range(0, 64):
    temp_msg = temp_msg + msg[transfer_table[i]]
  return temp_msg

def KeyReduce(key_64bit):
  # 將金鑰長度降為56bit
  key_reduce_table = [
                      56, 48, 40, 32, 24, 16, 8, 0, 57, 49, 41, 33, 25, 17, 
                      9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 
                      62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 
                      13, 5, 60, 52, 44, 36, 28, 20, 12, 4, 27, 19, 11, 3
                     ]
  temp_key = ''
  for i in range(0, 56):
    temp_key = temp_key + key_64bit[key_reduce_table[i]]
  return temp_key

def KeyTransfer(key_56bit,round, type):
  if type =='encrypt':
    pass
  else:
    round = 15 - round

  # 將金鑰長度降為48bit
  # 將56bit金鑰分為兩部分，照不同round循環左移不同的量
  # 最後將之合併，並挑出48個值。
  #key_offset = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
  key_offset = [1, 2, 4, 6, 8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 27, 28]
  key_reduce_table = [
                      13, 16, 10, 23, 0, 4, 2, 27, 14, 5, 20, 9, 
                      22, 18, 11, 3, 25, 7, 15, 6, 26, 19, 12, 1, 
                      40, 51, 30, 36, 46, 54, 29, 39, 50, 44, 32, 47, 
                      43, 48, 38, 55, 33, 52, 45, 41, 49, 35, 28, 31
                     ]
  offset_key_left = key_56bit[0 + key_offset[round]:28] + key_56bit[0:key_offset[round]]
  offset_key_right = key_56bit[28 + key_offset[round]:56] + key_56bit[28:28 + key_offset[round]]
  offset_key = offset_key_left + offset_key_right
  
  temp_key = ''
  for i in range(0, 48):
    temp_key = temp_key + offset_key[key_reduce_table[i]]
  return temp_key

def FFunction(l,r,key):
  return r, XOR(l, Feistel(r, key))

def Feistel(msg, key):
  return PReplace(SBoxReplace(XOR(EExtension(msg), key)))

def EExtension(msg):
  e_extension_table = [
                        31, 0, 1, 2, 3, 4, 
                        3, 4, 5, 6, 7, 8, 
                        7, 8, 9, 10, 11, 12, 
                        11, 12, 13, 14, 15, 16, 
                        15, 16, 17, 18, 19, 20, 
                        19, 20, 21, 22, 23, 24, 
                        23, 24, 25, 26, 27, 28, 
                        27, 28, 29, 30, 31, 0
                      ]
  temp_msg = ''
  for i in range(0, 48):
    temp_msg = temp_msg + msg[e_extension_table[i]]
  return temp_msg

def XOR(a,b):
  result = ''
  for i in range(0,len(a)):
    if a[i] == '1' and b[i] == '1':
      result += '0'
    elif a[i] == '1' and b[i] == '0':
      result += '1'
    elif a[i] == '0' and b[i] == '1':
      result += '1'
    elif a[i] == '0' and b[i] == '0':
      result += '0'
    else:
      print("XOR_ERROR!")
  return result

def SBoxReplace(msg):
  s_box_table = [
                  [
                    14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7, 
                    0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8, 
                    4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0, 
                    15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13
                  ], 
                  [
                    15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10, 
                    3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5, 
                    0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15, 
                    13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9
                  ], 
                  [
                    10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8, 
                    13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1, 
                    13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7, 
                    1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12
                  ], 
                  [
                    7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,  
                    13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,  
                    10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,  
                    3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14
                  ], 
                  [
                    2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9, 
                    14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6, 
                    4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14, 
                    11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3
                  ], 
                  [
                    12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11, 
                    10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8, 
                    9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6, 
                    4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13
                  ], 
                  [
                    4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1, 
                    13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6, 
                    1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2, 
                    6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12
                  ], 
                  [
                    13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7, 
                    1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2, 
                    7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8, 
                    2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11
                  ]
                ]

  output_msg = ''
  for i in range (0, 8):
    (h, l) = GetIndex(msg[i * 6: (i + 1) * 6])
    output_msg = output_msg + GetBin(s_box_table[i][h * 16 + l])
  return output_msg
    
def PReplace(msg):
  p_table = [
                    15, 6, 19, 20, 28, 11, 27, 16, 
                    0, 14, 22, 25, 4, 17, 30, 9, 
                    1, 7, 23, 13, 31, 26, 2, 8, 
                    18, 12, 29, 5, 21, 10, 3, 24
                   ]
  temp_msg = ''
  for i in range(0, 32):
    temp_msg = temp_msg + msg[p_table[i]]
  return temp_msg
  
def GetIndex(str):
  h = int(str[0]) * 2 + int(str[5])
  l = int(str[1]) * 8 + int(str[2]) * 4 + int(str[3]) * 2 + int(str[4])
  return (h, l)

def GetBin(number):
  num = int(number)
  ans = ''
  if num >= 8:
    ans = ans + '1'
    num = num - 8
  else:
    ans = ans + '0'

  if num >= 4:
    ans = ans + '1'
    num = num - 4
  else:
    ans = ans + '0'

  if num >= 2:
    ans = ans + '1'
    num = num - 2
  else:
    ans = ans + '0'

  if num >= 1:
    ans = ans + '1'
    num = num - 1
  else:
    ans = ans + '0'

  return ans

def IPFinalTransfer(msg):
  transfer_table = [
                    39, 7, 47, 15, 55, 23, 63, 31, 
                    38, 6, 46, 14, 54, 22, 62, 30, 
                    37, 5, 45, 13, 53, 21, 61, 29, 
                    36, 4, 44, 12, 52, 20, 60, 28, 
                    35, 3, 43, 11, 51, 19, 59, 27, 
                    34, 2, 42, 10, 50, 18, 58, 26, 
                    33, 1, 41, 9, 49, 17, 57, 25, 
                    32, 0, 40, 8, 48, 16, 56, 24
                   ]
  temp_msg = ''
  for i in range(0, 64):
    temp_msg = temp_msg + msg[transfer_table[i]]
  return temp_msg
  
def bin2text(s): 
  return "".join([chr(int(s[i:i+8],2)) for i in range(0,len(s),8)])

def DES(msg, key, method):
  bits = len(msg)
  now_bit = 0
  chiper = ''
  # 分割
  while(now_bit < bits):
    # 實現等長加解密
    # 64bit原文
    # 64bit金鑰
    chipher_1 = IPTransfer(msg[now_bit:now_bit + 64])
    (l ,r) = (chipher_1[0:32], chipher_1[32:64])
    key_56bit = KeyReduce(key)

    for k in range(0,16):
      l,r = FFunction(l, r, KeyTransfer(key_56bit,k,method))

    chiper += IPFinalTransfer(r + l)
    now_bit += 64
  return chiper

def Utf8ToBitString(str):
  bytes = []
  bin_str = ''
  for byte in bytearray(str, "utf8"):
    bin_str += bin(byte)[2:].zfill(8)
  return bin_str

def Padding(bit_string):
  while not len(bit_string)% 64 == 0:
    bit_string += '0'
  return bit_string

def BitstringToUtf8(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big').decode('utf-8')

def TDES(msg, key, method):
  if method == 'encrypt':
    (k1, k2, k3) = (key[:64], key[64:128], key[128:])
    return DES(DES(DES(msg, k1, 'encrypt'), k2, 'decrypt'), k3, 'encrypt')
  elif method == 'decrypt':
    (k1, k2, k3) = (key[128:], key[64:128], key[:64])
    return DES(DES(DES(msg, k1, 'decrypt'), k2, 'encrypt'), k3, 'decrypt')

def CheckKey(key, bits):
  if key == '':
      key = KeyGenerator(bits)
  while not key_pass:
    if len(key) == bits:
      for i in key:
        if not (i == '0' or i == '1'):
          print("金鑰僅能包含0與1。")
          return False
      return True
    else:
      print("金鑰長度須為64bit。")
      return False


def Welcome():
  choice = ''
  while not (choice == '1' or choice == '2' or choice == '3' or choice == '4' or choice == 'q'):
    print("\n\n\
=============================================\n\
本程式以UTF-8進行處理，僅對尾部做補零。\n\
1. DES加密\n\
2. DES解密\n\
3. 3DES加密\n\
4. 3DES解密\n\
q. 離開\n\
=============================================")
    print("請選擇功能: ", end = "")
    choice = input()
  return choice 


while True:
  choice = Welcome()
  if choice == '1':
    print("\n==================DES加密====================")
    print("請輸入UTF-8原始訊息: ", end = "")
    plaintext = Padding(Utf8ToBitString(input()))

    print("請輸入DES加密金鑰64bitsting，如需自動產生請留空白: ", end = '')
    key = input()

    while not CheckKey(key, 64):
      key = input()

      


      
    

    print("加密結果: ", end = "")
    print(DES(plaintext, key, 'encrypt'))
  

  elif choice == '2':
    print("\n==================DES解密====================")
    print("請輸入密文: ", end = "")
    chipher = input()

    print("請輸入DES加密金鑰64bitsting，如需自動產生請留空白: ", end = "")
    key = input()

    print("解密結果如下:")
    print(BitstringToUtf8(DES(chipher, key, 'decrypt')))


  elif choice == '3':
    print("\n=================TDES加密====================")
    print("請輸入UTF-8原始訊息")
    plaintext = Padding(Utf8ToBitString(input()()))

    print("請輸入TDES加密金鑰192bitsting，如需自動產生請留空白")
    key = input()

    print("加密結果如下:")
    print(TDES(plaintext, key, 'encrypt'))


  elif choice == '4':
    print("\n=================TDES解密====================")
    print("請輸入密文")
    chipher = input()

    print("請輸入TDES加密金鑰192bitsting")
    key = input()

    print("解密結果如下:")
    print(BitstringToUtf8(TDES(chipher, key, 'decrypt')))

  elif choice == 'q':
    sys.exit(0)



