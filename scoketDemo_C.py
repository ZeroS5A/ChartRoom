import socket  # 导入 socket 模块
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect((socket.gethostname(), 12345))
# 接收欢迎消息:
print(s.recv(1024).decode('utf-8'))


def receiveChart(s):
    try:
        while True:
            print(s.recv(1024).decode('utf-8') + "\n===================================")
    except Exception:
        print("断开连接")


def inputChart(s):
    try:
        global nickName
        content = ''
        while content != 'exit':
            content = input()
            s.send(bytes(str(nickName + ': ' +content).encode('utf-8')))
        s.send(b'exit')
        s.close()
    except Exception:
        print("你已退出聊天室")


global nickName
nickName = input("输入你的昵称开始聊天\n")
print("===================================")
threading.Thread(target=receiveChart, args=(s,)).start()
threading.Thread(target=inputChart, args=(s,)).start()



