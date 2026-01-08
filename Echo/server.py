import socket
import select # 导入select模块

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RECV_BUFFER_SIZE = 4096
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECV_BUFFER_SIZE)

# 使用select时，通常不需要为socket本身设置超时
# sock.settimeout(5.0) 

sock.bind((UDP_IP, UDP_PORT))
print(f"UDP 服务器已启动，正在 {UDP_IP}:{UDP_PORT} 监听...（按Ctrl+C退出）")

try:
    while True:
        # select会等待'sock'变为可读，超时时间为1秒
        # 如果超时，readable列表为空
        readable, _, _ = select.select([sock], [], [], 1.0)
        if readable:
            # 列表不为空，说明sock上有数据可读
            data, addr = sock.recvfrom(4096)
            message = data.decode('utf-8')
            print(f"收到来自 {addr} 的消息: {message} 长度为 {len(data)} 字节")
            response = f"服务器已收到: {message}"
            sock.sendto(response.encode('utf-8'), addr)
            print(f"已向 {addr} 发送响应")
        # else:
            # 超时，可以在这里打印日志或做其他事
            # print("等待数据超时，继续监听...")
            

except KeyboardInterrupt:
    print("\n收到退出信号，正在关闭服务器...")
finally:
    sock.close()
    print("服务器已关闭，套接字已释放")