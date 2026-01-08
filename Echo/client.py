import socket
import time

# 定义要连接的服务器的IP地址和端口
# 如果服务器和客户端在同一台电脑上，使用 "127.0.0.1" (localhost)
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# 创建UDP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"UDP 客户端已启动，准备向 {UDP_IP}:{UDP_PORT} 发送消息...")

try:
    for i in range(5):
        message = f"这是第 {i+1} 条消息"
        
        # 发送数据
        # encode('utf-8') 将字符串编码为二进制数据
        sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
        print(f"已发送: '{message}'")

        # 设置超时，避免recvfrom无限期等待
        sock.settimeout(2.0)
        
        try:
            # 等待接收服务器的响应
            data, server = sock.recvfrom(1024)
            response = data.decode('utf-8')
            print(f"从服务器 {server} 收到响应: '{response}'\n")
        except socket.timeout:
            print("等待服务器响应超时！\n")

        time.sleep(1)

finally:
    # 关闭套接字
    print("关闭客户端套接字。")
    sock.close()