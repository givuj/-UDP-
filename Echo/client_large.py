import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sockt =   socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

long_message = "A" * 2000  # 创建一个超过典型UDP包大小的长消息  
print(f"UDP 客户端已启动，准备向 {len(long_message)} 发送长消息...")
try:
    sockt.sendto(long_message.encode('utf-8'), (UDP_IP, UDP_PORT))
    print(f"已发送长消息，共 {len(long_message)} 字节。")
    #接受服务器响应
    sockt.settimeout(2.0)
    data, server = sockt.recvfrom(4096)
    print(f"实际接收字节数：{len(data)}")
except socket.timeout:
    print("等待服务器响应超时！\n")
finally:
    print("关闭客户端套接字。")
    sockt.close()       