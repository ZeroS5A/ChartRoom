import socket
# 建立一个服务端
import threading
import time

thread = threading.Condition()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), 12345))  # 绑定要监听的端口
server.listen(5)    # 开始监听 表示可以使用五个链接排队
print("正在等待连接....")


# 处理收到客户端的信息
def tcplink(sock, addr):
    try:
        global data
        global addrData
        print('Accept new connection from %s:%s...' % addr)
        sock.send(b'Welcome to charRoom! your port is '+str(addr[1]).encode('UTF-8'))
        while True:
            data = sock.recv(1024)
            addrData = '%s:%s' % addr
            if data.decode('utf-8') == 'exit':
                break
            # 通知所有进程结束等待
            print("收到\t" + addrData + '\n' + data.decode("UTF-8") + '\n======================================')
            NotifyAll()
            # print("%s:%s Says:\n" % addr + data.decode("utf-8"))
            # sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
        sock.close()
        print('Connection from %s:%s closed.' % addr)
    except Exception:
        sock.close()
        print("客户机已关闭")


# 发送数据的线程，与连接一起创建
def sendData(sock, addr):
    global data
    global addrData
    while True:
        if thread.acquire():
            thread.wait()
            if data:
                TempData = time.strftime("%m-%d %H:%M:%S", time.localtime()) + '\n' + data.decode("utf-8")
                sock.send(TempData.encode('UTF-8'))
                # print(TempData)


# 通知所有正在wait的进程发送信息
def NotifyAll():
    global data
    if thread.acquire():
        thread.notifyAll()
        thread.release()


while True:
    # 接受一个新连接:
    sock, addr = server.accept()
    # 创建新线程来处理TCP连接、发送等待:
    threading.Thread(target=tcplink, args=(sock, addr)).start()
    threading.Thread(target=sendData, args=(sock, addr)).start()
