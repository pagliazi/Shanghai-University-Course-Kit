# -*- coding:utf-8 -*-
import msvcrt
def pwd_input(prompt_msg):
    print prompt_msg
    chars = [] 
    while True:
        try:
            newChar = msvcrt.getch().decode(encoding="utf-8")
        except:
            return raw_input("probably not in CMD enviroment,can't hide your input\n")
        if newChar in '\r\n': # 如果是换行，则输入结束             
             break
        elif newChar == '\b': # 如果是退格，则删除密码末尾一位并且删除一个星号 
             if chars:  
                 del chars[-1] 
                 msvcrt.putch('\b'.encode(encoding='utf-8')) # 光标回退一格
                 msvcrt.putch( ' '.encode(encoding='utf-8')) # 输出一个空格覆盖原来的星号
                 msvcrt.putch('\b'.encode(encoding='utf-8')) # 光标回退一格准备接受新的输入                 
        else:
            chars.append(newChar)
            msvcrt.putch('*'.encode(encoding='utf-8')) # 显示为星号
    return (''.join(chars))
