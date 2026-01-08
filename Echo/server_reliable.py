import socket
import select  # 新增：导入select
import random
# 服务器配置
UDP_IP = "0.0.0.0"
UDP_PORT = 5005
BUFFER_SIZE = 4096  # 和接收缓冲区大小一致

# 可靠UDP相关：记录已处理的序列号
processed_seq = set()

# 创建套接字 + 设置接收缓冲区（保留你之前的配置）
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RECV_BUFFER_SIZE = 4096
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECV_BUFFER_SIZE)

# 绑定端口（保留）
sock.bind((UDP_IP, UDP_PORT))
print(f"可靠UDP服务器已启动（select版），监听 {UDP_IP}:{UDP_PORT}（按Ctrl+C退出）")

try:
    while True:
        # 核心改造：用select替代sock.settimeout + 阻塞recvfrom
        # 最多等1秒，期间有数据会立即唤醒；无数据则1秒后返回空列表
        readable, _, _ = select.select([sock], [], [], 1.0)
        
        if readable:  # 有数据可读（客户端发消息了）
            data, addr = sock.recvfrom(BUFFER_SIZE)
            packet = data.decode('utf-8')
            
            # 解析数据包（保留你之前的可靠UDP逻辑）
            parts = packet.split('|', 2)
            if len(parts) != 3 or parts[0] != "DATA":
                print(f"无效数据包: 跳过：{packet} ")
                continue
            
            # 提取字段（保留）
            data_type = parts[0]
            seq_num = int(parts[1])
            message = parts[2]
            
            # 去重逻辑（保留）
            if seq_num in processed_seq:
                ack_packet = f"ACK|{seq_num}"
                sock.sendto(ack_packet.encode('utf-8'), addr)
                print(f"重复数据包:已经回复ACK，跳过（序列号：{seq_num}）")
                continue

            # 模拟丢包逻辑（新增）
            if random.random() < 2/3:# 模拟1/3的概率丢包（不回复ACK
               print(f"模拟丢包：序列号{seq_num}的数据包被丢弃，不回复ACK")
               continue
            # 正常处理消息 + 回复ACK（保留）
            print(f"收到来自 {addr} 的消息: {message} (序列号: {seq_num})")
            processed_seq.add(seq_num) 
            ack_packet = f"ACK|{seq_num}"
            sock.sendto(ack_packet.encode('utf-8'), addr)
            print(f"已向 {addr} 发送ACK (序列号: {seq_num})")   
        # 无数据时不打印（避免刷屏，想打印可以取消注释）
        # else:
        #     print("等待数据超时（1秒），继续监听...")

except KeyboardInterrupt:
    print("\n收到退出信号，正在关闭服务器...")
finally:
    sock.close()
    print("服务器已关闭，套接字已释放")