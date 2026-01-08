import socket
import time

# 服务器配置
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
BUFFER_SIZE = 1024

# 客户端配置
TIMEOUT = 3.0  # 超时时间（3秒没收到ACK就重传）
MAX_RETRY = 3  # 最大重传次数
current_seq = 1  # 初始序列号

# 创建UDP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(TIMEOUT)  # 设置接收ACK的超时

def send_reliable_message(message):
    """发送可靠消息：带序列号+超时重传"""
    global current_seq
    retry_count = 0
    
    while retry_count < MAX_RETRY:
        try:
            # 构造数据报文
            packet = f"DATA|{current_seq}|{message}"
            print(f"\n发送数据包（序列号{current_seq}，重试{retry_count}次）：{message}")
            sock.sendto(packet.encode('utf-8'), (UDP_IP, UDP_PORT))
            
            # 等待接收ACK
            ack_data, server_addr = sock.recvfrom(BUFFER_SIZE)
            ack_packet = ack_data.decode('utf-8')
            
            # 解析ACK报文
            ack_parts = ack_packet.split('|', 1)
            if len(ack_parts) == 2 and ack_parts[0] == "ACK":
                ack_seq = int(ack_parts[1])
                if ack_seq == current_seq:
                    print(f"成功收到ACK（序列号{ack_seq}），发送完成！")
                    current_seq += 1  # 序列号自增，准备下一次发送
                    return True
            
            # ACK无效，继续重试
            print(f"收到无效ACK：{ack_packet}，准备重试...")
            retry_count += 1
            time.sleep(1)  # 重试前等待1秒
        
        except socket.timeout:
            # 超时，重传
            retry_count += 1
            print(f"超时（{TIMEOUT}秒）未收到ACK，重试{retry_count}次...")
            time.sleep(1)
    
    # 重传次数用尽
    print(f"重传{MAX_RETRY}次后仍未收到ACK，发送失败！")
    current_seq += 1
    return False

# 测试：发送3条消息
if __name__ == "__main__":
    try:
        messages = ["第一条可靠消息", "第二条可靠消息", "第三条可靠消息"]
        for msg in messages:
            send_reliable_message(msg)
    finally:
        sock.close()
        print("\n客户端已关闭")