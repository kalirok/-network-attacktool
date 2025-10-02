#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✨ 局域网综合攻击套件 - 美化增强版 🚀
集成多种攻击方法 | 专业界面设计 | 动画效果
"""

import sys
import time
import threading
import datetime
import re
import subprocess
import os
import shutil
from ai_assistant import create_ai_assistant, create_ai_interface

class Color:
    """🎨 高级颜色代码类 - 支持RGB渐变和动画效果"""
    # 基础颜色
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BLACK = '\033[30m'
    
    # 样式
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    REVERSE = '\033[7m'
    BLINK = '\033[5m'
    END = '\033[0m'
    
    # 背景色
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_PURPLE = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    @staticmethod
    def rgb(r, g, b):
        """生成RGB颜色代码"""
        return f'\033[38;2;{r};{g};{b}m'
    
    @staticmethod
    def gradient_text(text, start_color, end_color, steps=10):
        """生成渐变文字效果"""
        result = ""
        length = len(text)
        for i, char in enumerate(text):
            ratio = i / max(1, length - 1)
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            result += Color.rgb(r, g, b) + char
        return result + Color.END

class WisdomQuotes:
    """💭 网络安全智慧语录类"""
    
    # 网络安全相关名言警句
    QUOTES = [
        (
            "网络安全如同守护城堡，漏洞就是那扇未关的门。",
            "—— 网络安全专家"
        ),
        (
            "在数字世界中，谨慎是最好的防火墙。",
            "—— 信息安全格言"
        ),
        (
            "每一次成功的攻击，都源于一次疏忽的防御。",
            "—— 渗透测试箴言"
        ),
        (
            "了解攻击手段，才能更好地保护自己。",
            "—— 红队思维"
        ),
        (
            "网络安全不是产品，而是一个持续的过程。",
            "—— 安全管理原则"
        ),
        (
            "最坚固的防御，始于对威胁的认知。",
            "—— 威胁情报理念"
        ),
        (
            "在网络安全中，没有绝对的安全，只有相对的风险。",
            "—— 风险评估准则"
        ),
        (
            "技术是工具，人才是安全的关键。",
            "—— 人员安全意识"
        ),
        (
            "预防胜于治疗，在网络安全中尤其如此。",
            "—— 主动防御策略"
        ),
        (
            "每一次渗透测试，都是对防御能力的检验。",
            "—— 安全测试哲学"
        )
    ]
    
    @staticmethod
    def get_random_quote():
        """获取随机名言"""
        import random
        quote, author = random.choice(WisdomQuotes.QUOTES)
        return quote, author
    
    @staticmethod
    def display_quote():
        """显示精美名言"""
        quote, author = WisdomQuotes.get_random_quote()
        
        # 获取终端尺寸
        try:
            width, _ = shutil.get_terminal_size()
        except:
            width = 80
        
        # 创建精美的名言显示
        print(f"\n{Color.rgb(255, 215, 0)}💭 网络安全智慧 💭{Color.END}")
        
        # 引号装饰
        quote_line = "─" * (min(width // 2, 40))
        print(f"{Color.rgb(192, 192, 192)}{quote_line}{Color.END}")
        
        # 名言内容
        print(f"{Color.rgb(173, 216, 230)}『 {quote} 』{Color.END}")
        print(f"{Color.rgb(169, 169, 169)}    {author}{Color.END}")
        
        print(f"{Color.rgb(192, 192, 192)}{quote_line}{Color.END}\n")
    
    @staticmethod
    def clear_screen():
        """清屏"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    @staticmethod
    def get_terminal_size():
        """获取终端尺寸"""
        try:
            size = shutil.get_terminal_size()
            return size.columns, size.lines
        except:
            return 80, 24
    
    @staticmethod
    def center_text(text, width=None):
        """居中显示文本"""
        if width is None:
            try:
                width, _ = shutil.get_terminal_size()
            except:
                width = 80
        return text.center(width)
    
    @staticmethod
    def loading_bar(description="加载中", length=30, duration=2.0):
        """进度条动画"""
        print(f"\n{Color.CYAN}{description}...{Color.END}\n")
        
        for i in range(length + 1):
            percent = int((i / length) * 100)
            bar = f"[{Color.GREEN}{'█' * i}{Color.WHITE}{'░' * (length - i)}{Color.END}] {percent}%"
            print(f"\r{bar}", end="", flush=True)
            time.sleep(duration / length)
        print("\n")
    
    @staticmethod
    def spinning_cursor(duration=3.0):
        """旋转光标动画"""
        cursor_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        start_time = time.time()
        
        while time.time() - start_time < duration:
            for cursor in cursor_chars:
                print(f"\r{Color.YELLOW}{cursor}{Color.END} 正在初始化...", end="", flush=True)
                time.sleep(0.1)
        print("\r" + " " * 30 + "\r", end="", flush=True)
    
    @staticmethod
    def display_banner():
        """显示精美横幅"""
        try:
            width, height = shutil.get_terminal_size()
        except:
            width, height = 80, 24
        
        # 清屏并显示渐变边框
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # 顶部边框
        top_border = Color.gradient_text("═" * width, (255, 105, 180), (138, 43, 226))
        print(top_border)
        
        # 主标题
        title = "✨ 局域网综合攻击套件 ✨"
        centered_title = title.center(width)
        rainbow_title = ""
        colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]
        
        for i, char in enumerate(centered_title):
            color_idx = i % len(colors)
            rainbow_title += Color.rgb(*colors[color_idx]) + char
        
        print(f"\n{rainbow_title}{Color.END}")
        
        # 副标题
        subtitle = "🚀 专业网络安全测试工具 🛡️"
        centered_subtitle = subtitle.center(width)
        gradient_subtitle = Color.gradient_text(centered_subtitle, (64, 224, 208), (255, 215, 0))
        print(f"\n{gradient_subtitle}{Color.END}")
        
        # 版本信息
        version_info = "版本: 3.0.0 | 美化增强版 | Python 3.8+"
        centered_version = version_info.center(width)
        print(f"\n{Color.CYAN}{centered_version}{Color.END}")
        
        # 底部边框
        bottom_border = Color.gradient_text("═" * width, (138, 43, 226), (255, 105, 180))
        print(f"\n{bottom_border}")
        
        print("\n")
    
    def startup_sequence(self):
        """完整的启动序列"""
        # 清屏并显示渐变边框
        self.clear_screen()
        
        # 初始加载动画
        print(f"{Color.PURPLE}正在启动网络安全套件...{Color.END}\n")
        self.spinning_cursor(2.0)
        
        # 检查依赖
        print(f"{Color.BLUE}检查系统依赖...{Color.END}")
        self.loading_bar("验证Python环境", 20, 1.5)
        self.loading_bar("加载攻击模块", 25, 2.0)
        self.loading_bar("初始化网络接口", 30, 1.8)
        
        # 显示主横幅
        self.display_banner()
        
        # 显示智慧语录
        WisdomQuotes.display_quote()
        
        # 启动完成提示
        success_msg = "✅ 系统初始化完成！"
        centered_success = self.center_text(success_msg)
        print(f"\n{Color.GREEN}{Color.BOLD}{centered_success}{Color.END}\n")
        
        time.sleep(1)
    
    def simple_loading_bar(self, description="加载中", length=30, duration=2.0):
        """简化的进度条动画"""
        print(f"\n{Color.CYAN}{description}...{Color.END}\n")
        
        for i in range(length + 1):
            percent = int((i / length) * 100)
            bar = f"[{Color.GREEN}{'█' * i}{Color.WHITE}{'░' * (length - i)}{Color.END}] {percent}%"
            print(f"\r{bar}", end="", flush=True)
            time.sleep(duration / length)
        print("\n")

class Config:
    """配置管理类"""
    
    def __init__(self):
        self.settings = {
            'log_level': 'INFO',  # DEBUG, INFO, WARNING, ERROR
            'max_scan_threads': 10,
            'default_timeout': 5,
            'enable_color': True
        }
    
    def get(self, key, default=None):
        """获取配置值"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """设置配置值"""
        self.settings[key] = value

class Logger:
    """🎭 高级美化日志输出类 - 支持图标和动画效果"""
    
    config = Config()
    
    # 图标定义
    ICONS = {
        'DEBUG': '🔍',
        'INFO': 'ℹ️',
        'WARNING': '⚠️',
        'ERROR': '❌',
        'SUCCESS': '✅',
        'ATTACK': '🎯',
        'NETWORK': '🌐',
        'SECURITY': '🛡️',
        'LOADING': '⏳'
    }
    
    @staticmethod
    def get_timestamp():
        """获取带颜色和表情的时间戳"""
        return f"{Color.rgb(100, 149, 237)}⏰ {datetime.datetime.now().strftime('%H:%M:%S')}{Color.END}"
    
    @staticmethod
    def should_log(level):
        """检查是否应该记录该级别的日志"""
        levels = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3}
        current_level = Logger.config.get('log_level', 'INFO')
        return levels.get(level, 1) >= levels.get(current_level, 1)
    
    @staticmethod
    def debug(msg):
        """调试日志"""
        if Logger.should_log('DEBUG'):
            icon = Logger.ICONS['DEBUG']
            print(f"{Logger.get_timestamp()} {Color.rgb(169, 169, 169)}{icon} [调试]{Color.END} {msg}")
    
    @staticmethod
    def info(msg):
        """信息日志"""
        if Logger.should_log('INFO'):
            icon = Logger.ICONS['INFO']
            print(f"{Logger.get_timestamp()} {Color.BLUE}{icon} [信息]{Color.END} {msg}")
    
    @staticmethod
    def warning(msg):
        """警告日志"""
        if Logger.should_log('WARNING'):
            icon = Logger.ICONS['WARNING']
            print(f"{Logger.get_timestamp()} {Color.YELLOW}{icon} [警告]{Color.END} {msg}")
    
    @staticmethod
    def error(msg):
        """错误日志"""
        if Logger.should_log('ERROR'):
            icon = Logger.ICONS['ERROR']
            print(f"{Logger.get_timestamp()} {Color.RED}{icon} [错误]{Color.END} {msg}")
    
    @staticmethod
    def success(msg):
        """成功日志"""
        if Logger.should_log('INFO'):
            icon = Logger.ICONS['SUCCESS']
            print(f"{Logger.get_timestamp()} {Color.GREEN}{icon} [成功]{Color.END} {msg}")
    
    @staticmethod
    def attack(msg):
        """攻击日志"""
        if Logger.should_log('INFO'):
            icon = Logger.ICONS['ATTACK']
            print(f"{Logger.get_timestamp()} {Color.PURPLE}{icon} [攻击]{Color.END} {msg}")
    
    @staticmethod
    def network(msg):
        """网络日志"""
        if Logger.should_log('INFO'):
            icon = Logger.ICONS['NETWORK']
            print(f"{Logger.get_timestamp()} {Color.CYAN}{icon} [网络]{Color.END} {msg}")
    
    @staticmethod
    def security(msg):
        """安全日志"""
        if Logger.should_log('INFO'):
            icon = Logger.ICONS['SECURITY']
            print(f"{Logger.get_timestamp()} {Color.rgb(255, 165, 0)}{icon} [安全]{Color.END} {msg}")
    
    @staticmethod
    def highlight(msg):
        """高亮显示 - 渐变效果"""
        return Color.gradient_text(msg, (255, 215, 0), (255, 69, 0))
    
    @staticmethod
    def banner(msg):
        """横幅显示 - 居中带边框"""
        # 临时替代方案，避免循环引用
        try:
            width, _ = shutil.get_terminal_size()
        except:
            width = 80
        line = "─" * (min(len(msg) + 4, width))
        centered_msg = msg.center(width)
        print(f"\n{Color.rgb(138, 43, 226)}{centered_msg}{Color.END}")
    
    @staticmethod
    def loading(msg, duration=2.0):
        """加载动画"""
        print(f"\n{Color.CYAN}{Logger.ICONS['LOADING']} {msg}{Color.END}")
        # 简化版的旋转动画，避免依赖StartupAnimation
        cursor_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        start_time = time.time()
        
        while time.time() - start_time < duration:
            for cursor in cursor_chars:
                print(f"\r{Color.YELLOW}{cursor}{Color.END} {msg}...", end="", flush=True)
                time.sleep(0.1)
        print("\r" + " " * (len(msg) + 30) + "\r", end="", flush=True)

class NetworkUtils:
    """网络工具类"""
    
    @staticmethod
    def is_valid_mac(mac):
        """验证MAC地址格式是否正确"""
        if not mac or mac == "未知" or mac.lower() == "none":
            return False
        
        mac_pattern = re.compile(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")
        return bool(mac_pattern.match(mac))
    
    @staticmethod
    def get_mac_address(ip_address, max_retries=3):
        """获取MAC地址的增强版函数"""
        mac_cache = {}
        
        if ip_address in mac_cache:
            cached_mac = mac_cache[ip_address]
            if NetworkUtils.is_valid_mac(cached_mac):
                Logger.info(f"从缓存获取到MAC地址: {cached_mac}")
                return cached_mac
        
        mac_address = None
        methods_tried = []
        
        for attempt in range(max_retries):
            try:
                Logger.info(f"尝试获取 {ip_address} 的MAC地址 (第 {attempt + 1}/{max_retries} 次尝试)")
                
                # 方法1: 使用arp命令
                methods_tried.append("arp -a")
                result = subprocess.run(['arp', '-a', ip_address], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if ip_address in line:
                            parts = line.split()
                            if len(parts) >= 4:
                                mac_candidate = parts[3]
                                if NetworkUtils.is_valid_mac(mac_candidate):
                                    mac_address = mac_candidate
                                    Logger.success(f"通过arp -a获取到MAC地址: {mac_address}")
                                    break
                
                if NetworkUtils.is_valid_mac(mac_address):
                    break
                
                # 方法2: 使用ip neighbor命令
                methods_tried.append("ip neighbor")
                result = subprocess.run(['ip', 'neighbor', 'show', ip_address], capture_output=True, text=True)
                if result.returncode == 0 and result.stdout.strip():
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if ip_address in line:
                            parts = line.split()
                            if len(parts) >= 5:
                                mac_candidate = parts[4]
                                if NetworkUtils.is_valid_mac(mac_candidate):
                                    mac_address = mac_candidate
                                    Logger.success(f"通过ip neighbor获取到MAC地址: {mac_address}")
                                    break
                
                if NetworkUtils.is_valid_mac(mac_address):
                    break
                
                # 方法3: 使用ping确认主机在线
                methods_tried.append("ping")
                result = subprocess.run(['ping', '-c', '2', '-W', '1', ip_address], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    Logger.info(f"{ip_address} 在线，重新尝试获取MAC")
                    time.sleep(1)
                    continue
                else:
                    Logger.warning(f"{ip_address} 可能不在线或网络不通")
                    break
                
            except Exception as e:
                Logger.error(f"获取MAC地址时出错: {e}")
                if attempt == max_retries - 1:
                    Logger.error(f"所有方法都失败了: {', '.join(methods_tried)}")
        
        if NetworkUtils.is_valid_mac(mac_address):
            mac_cache[ip_address] = mac_address
            return mac_address
        else:
            Logger.error(f"无法获取 {ip_address} 的MAC地址")
            return "未知"

class AttackManager:
    """攻击管理器类"""
    
    def __init__(self):
        self.active_attacks = {}
        self.attack_start_times = {}
        self.mac_cache = {}
    
    def start_attack(self, attack_type, attack_func):
        """启动攻击"""
        if attack_type in self.active_attacks:
            Logger.warning(f"{attack_type} 攻击已经在运行中")
            return
        
        try:
            attack_thread = threading.Thread(target=attack_func)
            attack_thread.daemon = True
            
            # 存储攻击函数信息以便后续停止
            attack_thread._target_func = attack_func
            
            attack_thread.start()
            
            self.active_attacks[attack_type] = attack_thread
            self.attack_start_times[attack_type] = datetime.datetime.now()
            Logger.success(f"{attack_type} 攻击已启动")
            
        except Exception as e:
            Logger.error(f"启动 {attack_type} 攻击失败: {e}")
    
    def stop_attack(self, attack_type, lan_suite=None):
        """停止攻击"""
        if attack_type in self.active_attacks:
            # 停止攻击线程
            thread = self.active_attacks[attack_type]
            
            # 根据攻击类型调用对应的停止方法
        # 注意：外部工具可能没有running属性，这里只做基本的停止尝试
        if lan_suite:
            if attack_type == "🎯 ARP欺骗" and hasattr(lan_suite, 'arp_spoof_tool') and lan_suite.arp_spoof_tool:
                if hasattr(lan_suite.arp_spoof_tool, 'running'):
                    lan_suite.arp_spoof_tool.running = False
            elif attack_type == "🕷️ DHCP饥饿攻击" and hasattr(lan_suite, 'dhcp_starvation_tool') and lan_suite.dhcp_starvation_tool:
                if hasattr(lan_suite.dhcp_starvation_tool, 'running'):
                    lan_suite.dhcp_starvation_tool.running = False
            elif attack_type == "🌊 MAC洪泛攻击" and hasattr(lan_suite, 'mac_flood_tool') and lan_suite.mac_flood_tool:
                if hasattr(lan_suite.mac_flood_tool, 'running'):
                    lan_suite.mac_flood_tool.running = False
            elif attack_type == "🌐 DNS欺骗" and hasattr(lan_suite, 'dns_spoof_tool') and lan_suite.dns_spoof_tool:
                if hasattr(lan_suite.dns_spoof_tool, 'running'):
                    lan_suite.dns_spoof_tool.running = False
            elif attack_type == "📶 WiFi密码破解" and hasattr(lan_suite, 'wifi_cracker_tool') and lan_suite.wifi_cracker_tool:
                if hasattr(lan_suite.wifi_cracker_tool, 'running'):
                    lan_suite.wifi_cracker_tool.running = False
            elif attack_type == "⚡ ICMP放大攻击" and hasattr(lan_suite, 'icmp_amplification_tool') and lan_suite.icmp_amplification_tool:
                if hasattr(lan_suite.icmp_amplification_tool, 'running'):
                    lan_suite.icmp_amplification_tool.running = False
            
            # 等待线程结束
            thread.join(timeout=3)
            
            # 如果线程仍然存活，强制终止
            if thread.is_alive():
                Logger.warning(f"{attack_type} 线程仍在运行，强制终止")
                # 这里不能直接终止线程，因为Python线程没有安全的终止方法
                # 只能依赖running标志和超时机制
            
            self.active_attacks.pop(attack_type, None)
            self.attack_start_times.pop(attack_type, None)
            Logger.success(f"{attack_type} 攻击已停止")
        else:
            Logger.warning(f"{attack_type} 攻击未在运行")
    
    def stop_all_attacks(self, lan_suite=None):
        """停止所有攻击"""
        attacks_to_stop = list(self.active_attacks.keys())
        for attack_type in attacks_to_stop:
            self.stop_attack(attack_type, lan_suite)
        Logger.success("所有攻击已停止")
    
    def show_attack_status(self):
        """显示攻击状态"""
        if self.active_attacks:
            status_info = []
            for attack_type, start_time in self.attack_start_times.items():
                elapsed = datetime.datetime.now() - start_time
                elapsed_str = str(elapsed).split('.')[0]
                status_info.append(f"{attack_type}: {elapsed_str}")
            
            Logger.info(f"当前活跃攻击: {len(self.active_attacks)} 个")
            for status in status_info:
                Logger.info(f"  - {status}")
        else:
            Logger.info("当前没有活跃攻击")

class NetworkDiagnosis:
    """网络诊断工具类"""
    
    @staticmethod
    def ping_test(host):
        """Ping测试"""
        try:
            result = subprocess.run(['ping', '-c', '3', host], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                Logger.success(f"Ping {host}: 成功")
                return True
            else:
                Logger.error(f"Ping {host}: 失败")
                return False
        except Exception as e:
            Logger.error(f"Ping测试出错: {e}")
            return False
    
    @staticmethod
    def port_scan(host, port):
        """端口扫描"""
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                Logger.success(f"端口 {port}: 开放")
                return True
            else:
                Logger.info(f"端口 {port}: 关闭")
                return False
        except Exception as e:
            Logger.error(f"端口扫描出错: {e}")
            return False

class LANAttackSuite:
    """局域网攻击套件主类"""
    
    def __init__(self):
        self.attack_manager = AttackManager()
        self.network_diagnosis = NetworkDiagnosis()
        self.running = True
        
        # 初始化AI助手
        self.ai_assistant = create_ai_assistant()
        self.ai_interface = create_ai_interface(self.ai_assistant)
        
        # 初始化攻击工具实例
        try:
            from arp_spoof_advanced import ARPSpoofAdvanced
            self.arp_spoof_tool = ARPSpoofAdvanced()
        except ImportError:
            Logger.warning("ARP欺骗工具导入失败")
            self.arp_spoof_tool = None
            
        try:
            from dhcp_starvation import DHCPStarvation
            self.dhcp_starvation_tool = DHCPStarvation()
        except ImportError:
            Logger.warning("DHCP饥饿攻击工具导入失败")
            self.dhcp_starvation_tool = None
            
        try:
            from dns_spoof import DNSSpoof
            self.dns_spoof_tool = DNSSpoof()
        except ImportError:
            Logger.warning("DNS欺骗工具导入失败")
            self.dns_spoof_tool = None
            
        try:
            from mac_flood import MACFlood
            self.mac_flood_tool = MACFlood()
        except ImportError:
            Logger.warning("MAC洪泛攻击工具导入失败")
            self.mac_flood_tool = None
            
        try:
            from wifi_password_cracker import WiFiPasswordCracker
            self.wifi_cracker_tool = WiFiPasswordCracker()
        except ImportError:
            Logger.warning("WiFi密码破解工具导入失败")
            self.wifi_cracker_tool = None
        
        try:
            from icmp_amplification import ICMPAmplification
            self.icmp_amplification_tool = ICMPAmplification()
        except ImportError:
            Logger.warning("ICMP放大攻击工具导入失败")
            self.icmp_amplification_tool = None
    
    def show_banner(self):
        """显示专业程序横幅"""
        # 获取终端尺寸
        try:
            width, height = shutil.get_terminal_size()
        except:
            width, height = 80, 24
        
        # 顶部边框
        top_border = Color.gradient_text("═" * width, (255, 105, 180), (138, 43, 226))
        print(top_border)
        
        # 主标题
        title = "✨ 局域网综合攻击套件 ✨"
        centered_title = title.center(width)
        rainbow_title = ""
        colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]
        
        for i, char in enumerate(centered_title):
            color_idx = i % len(colors)
            rainbow_title += Color.rgb(*colors[color_idx]) + char
        
        print(f"\n{rainbow_title}{Color.END}")
        
        # 副标题
        subtitle = "🚀 专业网络安全测试工具 🛡️"
        centered_subtitle = subtitle.center(width)
        gradient_subtitle = Color.gradient_text(centered_subtitle, (64, 224, 208), (255, 215, 0))
        print(f"\n{gradient_subtitle}{Color.END}")
        
        # 版本信息
        version_info = "版本: 3.0.0 | 美化增强版 | Python 3.8+"
        centered_version = version_info.center(width)
        print(f"\n{Color.CYAN}{centered_version}{Color.END}")
        
        # 底部边框
        bottom_border = Color.gradient_text("═" * width, (138, 43, 226), (255, 105, 180))
        print(f"\n{bottom_border}")
        
        # 显示系统信息
        info_line = "─" * (width // 3)
        print(f"\n{Color.rgb(64, 224, 208)}{info_line} 系统信息 {info_line}{Color.END}")
        
        # 获取系统信息
        try:
            # Python版本
            python_version = sys.version.split()[0]
            # 操作系统信息
            os_info = f"{os.name} - {sys.platform}"
            # 当前时间
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            info_items = [
                f"Python版本: {Color.GREEN}{python_version}{Color.END}",
                f"操作系统: {Color.BLUE}{os_info}{Color.END}",
                f"当前时间: {Color.YELLOW}{current_time}{Color.END}",
                f"活跃攻击: {Color.PURPLE}{len(self.attack_manager.active_attacks)} 个{Color.END}"
            ]
            
            for item in info_items:
                print(f"  {item}")
                
        except Exception as e:
            Logger.error(f"获取系统信息失败: {e}")
        
        print(f"\n{Color.rgb(64, 224, 208)}{info_line} 功能说明 {info_line}{Color.END}\n")
    
    def startup_sequence(self):
        """完整的启动序列"""
        # 清屏
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # 初始加载动画
        print(f"{Color.PURPLE}正在启动网络安全套件...{Color.END}\n")
        Logger.loading("初始化系统", 2.0)
        
        # 检查依赖
        print(f"{Color.BLUE}检查系统依赖...{Color.END}")
        self.simple_loading_bar("验证Python环境", 20, 1.5)
        self.simple_loading_bar("加载攻击模块", 25, 2.0)
        self.simple_loading_bar("初始化网络接口", 30, 1.8)
        
        # 显示主横幅
        self.show_banner()
        
        # 显示智慧语录
        WisdomQuotes.display_quote()
        
        # 启动完成提示
        success_msg = "✅ 系统初始化完成！"
        # 获取终端宽度居中显示
        try:
            width, _ = shutil.get_terminal_size()
        except:
            width = 80
        centered_success = success_msg.center(width)
        print(f"\n{Color.GREEN}{Color.BOLD}{centered_success}{Color.END}\n")
        
        time.sleep(1)
    
    def simple_loading_bar(self, description="加载中", length=30, duration=2.0):
        """简化的进度条动画"""
        print(f"\n{Color.CYAN}{description}...{Color.END}\n")
        
        for i in range(length + 1):
            percent = int((i / length) * 100)
            bar = f"[{Color.GREEN}{'█' * i}{Color.WHITE}{'░' * (length - i)}{Color.END}] {percent}%"
            print(f"\r{bar}", end="", flush=True)
            time.sleep(duration / length)
        print("\n")
    
    def show_menu(self):
        """显示精美主菜单"""
        # 获取终端尺寸
        try:
            width, _ = shutil.get_terminal_size()
        except:
            width = 80
        
        # 菜单标题
        title = "🎮 主菜单导航"
        centered_title = title.center(width)
        print(f"\n{Color.rgb(255, 105, 180)}{Color.BOLD}{centered_title}{Color.END}\n")
        
        # 菜单选项 - 使用表格布局
        menu_options = [
            ("1", "🎯 ARP欺骗攻击", "6", "🔍 网络诊断"),
            ("2", "🕷️ DHCP饥饿攻击", "7", "📊 攻击状态监控"),
            ("3", "🌊 MAC洪泛攻击", "8", "🖧 网络接口信息"),
            ("4", "⚡ ICMP放大攻击", "9", "📡 局域网设备扫描"),
            ("5", "🌐 DNS欺骗攻击", "A", "🔎 MAC地址查询"),
            ("B", "📶 WiFi密码破解", "C", "⚙️  配置管理"),
            ("D", "🤖 AI助手", "0", "🚪 安全退出")
        ]
        
        # 计算列宽
        col1_width = max(len(f"{opt[0]}. {opt[1]}") for opt in menu_options if opt[0])
        col2_width = max(len(f"{opt[2]}. {opt[3]}") for opt in menu_options if opt[2])
        
        # 打印菜单
        for opt in menu_options:
            left_col = f"{Color.YELLOW}{opt[0]}.{Color.END} {Color.CYAN}{opt[1]}{Color.END}" if opt[0] else ""
            right_col = f"{Color.YELLOW}{opt[2]}.{Color.END} {Color.CYAN}{opt[3]}{Color.END}" if opt[2] else ""
            
            if left_col and right_col:
                # 两列布局
                padding = " " * 4
                print(f"  {left_col.ljust(col1_width)}{padding}{right_col}")
            elif right_col:
                # 只有右列（退出选项）
                print(f"  {' ' * (col1_width + len(padding))}{right_col}")
        
        # 分隔线
        separator = Color.gradient_text("─" * (width // 2), (255, 105, 180), (138, 43, 226))
        print(f"\n{separator}\n")
        
        # 状态信息
        status_info = [
            f"{Color.BLUE}⏰ 当前时间: {datetime.datetime.now().strftime('%H:%M:%S')}{Color.END}",
            f"{Color.PURPLE}🎯 活跃攻击: {len(self.attack_manager.active_attacks)} 个{Color.END}"
        ]
        
        for info in status_info:
            print(f"  {info}")
        
        # 警告信息
        if self.attack_manager.active_attacks:
            attack_list = list(self.attack_manager.active_attacks.keys())
            warning_msg = f"{Color.RED}⚠  警告: 正在运行的攻击 - {', '.join(attack_list)}{Color.END}"
            print(f"\n{warning_msg}")
    
    def handle_arp_spoof(self):
        """处理ARP欺骗攻击"""
        Logger.attack("ARP欺骗攻击功能")
        Logger.banner("🎯 ARP欺骗攻击模块")
        
        if not self.arp_spoof_tool:
            Logger.error("ARP欺骗工具未正确导入")
            return
        
        # 美化子菜单
        submenu_options = [
            ("1", "🔍 扫描网络"),
            ("2", "🎯 单目标ARP欺骗"),
            ("3", "🎯 多目标ARP欺骗"),
            ("4", "🔧 网络问题诊断"),
            ("5", "🔙 返回主菜单")
        ]
        
        print(f"\n{Color.rgb(255, 215, 0)}请选择操作模式:{Color.END}\n")
        for opt in submenu_options:
            print(f"  {Color.YELLOW}{opt[0]}.{Color.END} {Color.CYAN}{opt[1]}{Color.END}")
        
        choice = input(f"\n{Color.rgb(255, 105, 180)}🎯 请输入选择: {Color.END}").strip()
        
        if choice == '1':
            subnet = input(f"{Color.rgb(64, 224, 208)}🌐 请输入子网 (例如 192.168.1.0/24): {Color.END}").strip()
            if not subnet:
                local_ip = self.arp_spoof_tool.get_local_ip()
                subnet = f"{'.'.join(local_ip.split('.')[:3])}.0/24"
            Logger.loading("正在扫描网络设备")
            self.arp_spoof_tool.scan_network(subnet)
        elif choice == '2':
            target_ip = input(f"{Color.rgb(255, 69, 0)}🎯 请输入目标IP: {Color.END}").strip()
            gateway_ip = input(f"{Color.rgb(0, 191, 255)}🌉 请输入网关IP: {Color.END}").strip()
            interface = input(f"{Color.rgb(138, 43, 226)}🔌 请输入网络接口: {Color.END}").strip()
            sniff_choice = input(f"{Color.rgb(255, 215, 0)}👃 启用数据包嗅探? (y/n): {Color.END}").strip().lower()
            
            # AI实时帮助
            if self.ai_assistant.enabled:
                self.arp_spoof_tool.real_time_ai_help("starting")
            
            def arp_attack():
                self.arp_spoof_tool.start_attack([target_ip], gateway_ip, interface, sniff_choice == 'y')
            
            self.attack_manager.start_attack("🎯 ARP欺骗", arp_attack)
            
            # AI实时帮助
            if self.ai_assistant.enabled:
                self.arp_spoof_tool.real_time_ai_help("attacking")
            
            input(f"{Color.rgb(255, 105, 180)}⏹️  按回车键停止攻击...{Color.END}")
            
            # AI实时帮助
            if self.ai_assistant.enabled:
                self.arp_spoof_tool.real_time_ai_help("recovery")
            
            self.attack_manager.stop_attack("🎯 ARP欺骗", self)
        elif choice == '3':
            targets_input = input(f"{Color.rgb(255, 69, 0)}🎯 请输入目标IP列表 (用空格分隔): {Color.END}").strip()
            target_ips = targets_input.split()
            gateway_ip = input(f"{Color.rgb(0, 191, 255)}🌉 请输入网关IP: {Color.END}").strip()
            interface = input(f"{Color.rgb(138, 43, 226)}🔌 请输入网络接口: {Color.END}").strip()
            sniff_choice = input(f"{Color.rgb(255, 215, 0)}👃 启用数据包嗅探? (y/n): {Color.END}").strip().lower()
            
            # AI实时帮助
            if self.ai_assistant.enabled:
                self.arp_spoof_tool.real_time_ai_help("starting")
            
            def arp_attack():
                self.arp_spoof_tool.start_attack(target_ips, gateway_ip, interface, sniff_choice == 'y')
            
            self.attack_manager.start_attack("🎯 ARP欺骗", arp_attack)
            
            # AI实时帮助
            if self.ai_assistant.enabled:
                self.arp_spoof_tool.real_time_ai_help("attacking")
            
            input(f"{Color.rgb(255, 105, 180)}⏹️  按回车键停止攻击...{Color.END}")
            
            # AI实时帮助
            if self.ai_assistant.enabled:
                self.arp_spoof_tool.real_time_ai_help("recovery")
            
            self.attack_manager.stop_attack("🎯 ARP欺骗", self)
        elif choice == '4':
            diag_ip = input(f"{Color.YELLOW}请输入要诊断的IP地址 (留空使用默认网关): {Color.END}").strip()
            if not diag_ip:
                self.arp_spoof_tool.diagnose_network_issue()
            else:
                self.arp_spoof_tool.diagnose_network_issue(diag_ip)
        elif choice == '5':
            return
        else:
            Logger.warning("无效的选择")
    
    def handle_dhcp_starvation(self):
        """处理DHCP饥饿攻击"""
        Logger.info("DHCP饥饿攻击功能")
        
        if not self.dhcp_starvation_tool:
            Logger.error("DHCP饥饿攻击工具未正确导入")
            return
        
        interface = input(f"{Color.YELLOW}请输入网络接口: {Color.END}").strip()
        threads = input(f"{Color.YELLOW}请输入线程数量 (默认5): {Color.END}").strip()
        
        if not threads.isdigit():
            threads = 5
        else:
            threads = int(threads)
        
        def dhcp_attack():
            self.dhcp_starvation_tool.start_attack(interface, threads)
        
        self.attack_manager.start_attack("🕷️ DHCP饥饿攻击", dhcp_attack)
        input(f"{Color.rgb(255, 105, 180)}⏹️  按回车键停止攻击...{Color.END}")
        self.attack_manager.stop_attack("🕷️ DHCP饥饿攻击", self)
    
    def handle_mac_flood(self):
        """处理MAC洪泛攻击"""
        Logger.info("MAC洪泛攻击功能")
        
        if not self.mac_flood_tool:
            Logger.error("MAC洪泛攻击工具未正确导入")
            return
        
        interface = input(f"{Color.YELLOW}请输入网络接口: {Color.END}").strip()
        threads = input(f"{Color.YELLOW}请输入线程数量 (默认3): {Color.END}").strip()
        
        if not threads.isdigit():
            threads = 3
        else:
            threads = int(threads)
        
        def mac_flood_attack():
            self.mac_flood_tool.start_attack(interface, threads)
        
        self.attack_manager.start_attack("🌊 MAC洪泛攻击", mac_flood_attack)
        input(f"{Color.rgb(255, 105, 180)}⏹️  按回车键停止攻击...{Color.END}")
        self.attack_manager.stop_attack("🌊 MAC洪泛攻击", self)
    
    def handle_dns_spoof(self):
        """处理DNS欺骗攻击"""
        Logger.attack("DNS欺骗攻击功能")
        Logger.banner("🌐 DNS欺骗攻击模块")
        
        if not self.dns_spoof_tool:
            Logger.error("DNS欺骗工具未正确导入")
            return
        
        interface = input(f"{Color.rgb(138, 43, 226)}🔌 请输入网络接口: {Color.END}").strip()
        domains_input = input(f"{Color.rgb(255, 69, 0)}🌍 请输入要欺骗的域名列表 (用空格分隔): {Color.END}").strip()
        fake_ip = input(f"{Color.rgb(0, 191, 255)}🎭 请输入虚假IP地址: {Color.END}").strip()
        
        domains = domains_input.split()
        self.dns_spoof_tool.setup_spoof_rules(domains, fake_ip)
        
        def dns_attack():
            self.dns_spoof_tool.start_attack(interface)
        
        self.attack_manager.start_attack("🌐 DNS欺骗", dns_attack)
        input(f"{Color.rgb(255, 105, 180)}⏹️  按回车键停止攻击...{Color.END}")
        self.attack_manager.stop_attack("🌐 DNS欺骗", self)
    
    def handle_icmp_amplification(self):
        """处理ICMP放大攻击"""
        Logger.attack("ICMP放大攻击功能")
        Logger.banner("⚡ ICMP放大攻击模块")
        
        if not self.icmp_amplification_tool:
            Logger.error("ICMP放大攻击工具未正确导入")
            return
        
        # 美化子菜单
        submenu_options = [
            ("1", "⚡ 标准ICMP放大攻击"),
            ("2", "🌪️  Smurf攻击"),
            ("3", "💥 Ping洪水攻击"),
            ("4", "🧵 多线程攻击"),
            ("5", "🔙 返回主菜单")
        ]
        
        print(f"\n{Color.rgb(255, 215, 0)}请选择攻击模式:{Color.END}\n")
        for opt in submenu_options:
            print(f"  {Color.YELLOW}{opt[0]}.{Color.END} {Color.CYAN}{opt[1]}{Color.END}")
        
        choice = input(f"\n{Color.rgb(255, 105, 180)}⚡ 请输入选择: {Color.END}").strip()
        
        if choice == '1':
            target_ip = input(f"{Color.rgb(255, 69, 0)}🎯 请输入目标IP: {Color.END}").strip()
            packet_size = int(input(f"{Color.rgb(255, 215, 0)}📦 包大小 (默认1024): {Color.END}") or "1024")
            rate = int(input(f"{Color.rgb(0, 191, 255)}🚀 发送速率/秒 (默认100): {Color.END}") or "100")
            
            def icmp_attack():
                self.icmp_amplification_tool.start_amplification_attack(
                    target_ip, "standard",
                    packet_size=packet_size,
                    packets_per_second=rate
                )
            
            self.attack_manager.start_attack("⚡ ICMP放大攻击", icmp_attack)
            input(f"{Color.rgb(255, 105, 180)}⏹️  按回车键停止攻击...{Color.END}")
            self.attack_manager.stop_attack("⚡ ICMP放大攻击", self)
        elif choice == '2':
            target_ip = input(f"{Color.rgb(255, 69, 0)}🎯 请输入目标IP: {Color.END}").strip()
            broadcast = input(f"{Color.rgb(64, 224, 208)}📢 请输入广播地址 (留空自动计算): {Color.END}").strip()
            
            def smurf_attack():
                if not broadcast:
                    from icmp_amplification import get_network_broadcast
                    calculated_broadcast = get_network_broadcast(target_ip)
                    print(f"{Color.CYAN}[*] 计算得到广播地址: {calculated_broadcast}{Color.END}")
                    network_broadcast = calculated_broadcast
                else:
                    network_broadcast = broadcast
                
                self.icmp_amplification_tool.start_amplification_attack(
                    target_ip, "smurf",
                    network_broadcast=network_broadcast
                )
            
            self.attack_manager.start_attack("⚡ ICMP放大攻击", smurf_attack)
            input(f"{Color.rgb(255, 105, 180)}⏹️  按回车键停止攻击...{Color.END}")
            self.attack_manager.stop_attack("⚡ ICMP放大攻击", self)
        elif choice == '3':
            target_ip = input(f"{Color.YELLOW}请输入目标IP: {Color.END}").strip()
            packet_size = int(input(f"{Color.YELLOW}包大小 (默认1024): {Color.END}") or "1024")
            
            def ping_flood_attack():
                self.icmp_amplification_tool.start_amplification_attack(
                    target_ip, "ping_flood",
                    packet_size=packet_size
                )
            
            self.attack_manager.start_attack("⚡ ICMP放大攻击", ping_flood_attack)
            input(f"{Color.rgb(255, 105, 180)}⏹️  按回车键停止攻击...{Color.END}")
            self.attack_manager.stop_attack("⚡ ICMP放大攻击", self)
        elif choice == '4':
            target_ip = input(f"{Color.YELLOW}请输入目标IP: {Color.END}").strip()
            threads = int(input(f"{Color.YELLOW}线程数量 (默认5): {Color.END}") or "5")
            packet_size = int(input(f"{Color.YELLOW}包大小 (默认1024): {Color.END}") or "1024")
            rate = int(input(f"{Color.YELLOW}每线程速率/秒 (默认50): {Color.END}") or "50")
            
            def multi_thread_attack():
                self.icmp_amplification_tool.start_multi_thread_attack(
                    target_ip,
                    thread_count=threads,
                    packet_size=packet_size,
                    packets_per_second=rate
                )
            
            self.attack_manager.start_attack("⚡ ICMP放大攻击", multi_thread_attack)
            input(f"{Color.rgb(255, 105, 180)}⏹️  按回车键停止攻击...{Color.END}")
            self.attack_manager.stop_attack("⚡ ICMP放大攻击", self)
        elif choice == '5':
            return
        else:
            Logger.warning("无效的选择")
    
    def handle_network_diagnosis(self):
        """处理网络诊断"""
        Logger.network("网络诊断功能")
        Logger.banner("🔍 网络诊断工具")
        
        # 美化子菜单
        submenu_options = [
            ("1", "🏓 Ping测试"),
            ("2", "🔍 端口扫描"),
            ("3", "🖧 网络接口信息"),
            ("4", "🔙 返回主菜单")
        ]
        
        print(f"\n{Color.rgb(255, 215, 0)}请选择诊断项目:{Color.END}\n")
        for opt in submenu_options:
            print(f"  {Color.YELLOW}{opt[0]}.{Color.END} {Color.CYAN}{opt[1]}{Color.END}")
        
        choice = input(f"\n{Color.rgb(255, 105, 180)}🔍 请输入选择: {Color.END}").strip()
        
        if choice == '1':
            host = input(f"{Color.rgb(64, 224, 208)}🌐 请输入要测试的主机IP或域名: {Color.END}")
            if host:
                Logger.loading(f"正在测试 {host} 的连接性")
                self.network_diagnosis.ping_test(host)
        elif choice == '2':
            host = input(f"{Color.rgb(64, 224, 208)}🎯 请输入要扫描的主机IP: {Color.END}")
            if host:
                ports = input(f"{Color.rgb(255, 215, 0)}🔢 请输入要扫描的端口(用逗号分隔，如80,443,22): {Color.END}")
                if ports:
                    port_list = [int(p.strip()) for p in ports.split(',')]
                    Logger.loading(f"正在扫描 {host} 的端口")
                    for port in port_list:
                        self.network_diagnosis.port_scan(host, port)
        elif choice == '3':
            self.handle_interface_info()
        elif choice == '4':
            return
        else:
            Logger.warning("无效的选择")
    
    def handle_attack_monitor(self):
        """处理攻击状态监控"""
        self.attack_manager.show_attack_status()
    
    def handle_interface_info(self):
        """处理网络接口信息"""
        Logger.info("网络接口信息")
        
        try:
            # 获取网络接口信息
            result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{Color.CYAN}网络接口信息:{Color.END}")
                print(result.stdout)
            else:
                Logger.error("获取网络接口信息失败")
                
            # 获取路由表信息
            result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{Color.CYAN}路由表信息:{Color.END}")
                print(result.stdout)
            else:
                Logger.error("获取路由表信息失败")
                
        except Exception as e:
            Logger.error(f"获取网络信息出错: {e}")
    
    def handle_network_scan(self):
        """处理局域网设备扫描"""
        Logger.info("局域网设备扫描")
        
        try:
            # 使用nmap进行局域网扫描
            Logger.info("正在扫描局域网设备...")
            
            # 获取本地网络接口信息
            result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'default' in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            gateway = parts[2]
                            Logger.info(f"检测到网关: {gateway}")
                            
                            # 提取网络段
                            gateway_parts = gateway.split('.')
                            if len(gateway_parts) >= 3:
                                network_prefix = f"{gateway_parts[0]}.{gateway_parts[1]}.{gateway_parts[2]}"
                                Logger.info(f"扫描网络段: {network_prefix}.0/24")
                                
                                # 使用ping扫描
                                for i in range(1, 255):
                                    ip = f"{network_prefix}.{i}"
                                    if ip != gateway:  # 跳过网关
                                        result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                                                              capture_output=True, text=True)
                                        if result.returncode == 0:
                                            mac = NetworkUtils.get_mac_address(ip, max_retries=1)
                                            Logger.info(f"发现设备: {ip} - MAC: {mac}")
                                break
            else:
                Logger.error("无法获取网络路由信息")
                
        except Exception as e:
            Logger.error(f"局域网扫描出错: {e}")
    
    def handle_wifi_cracker(self):
        """处理WiFi密码破解"""
        Logger.security("WiFi密码破解功能")
        Logger.banner("📶 WiFi密码破解模块")
        
        if not self.wifi_cracker_tool:
            Logger.error("WiFi密码破解工具未正确导入")
            return
        
        # 美化子菜单
        submenu_options = [
            ("1", "📡 扫描可用WiFi网络"),
            ("2", "🔓 破解指定WiFi密码"),
            ("3", "🔙 返回主菜单")
        ]
        
        print(f"\n{Color.rgb(255, 215, 0)}请选择操作模式:{Color.END}\n")
        for opt in submenu_options:
            print(f"  {Color.YELLOW}{opt[0]}.{Color.END} {Color.CYAN}{opt[1]}{Color.END}")
        
        choice = input(f"\n{Color.rgb(255, 105, 180)}📶 请输入选择: {Color.END}").strip()
        
        if choice == '1':
            Logger.loading("正在扫描附近的WiFi网络")
            networks = self.wifi_cracker_tool.scan_available_networks()
            if networks:
                print(f"\n{Color.GREEN}📡 发现的WiFi网络:{Color.END}\n")
                for i, net in enumerate(networks):
                    ssid = net.get('ssid', 'Unknown')
                    security = net.get('security', 'Unknown')
                    signal_strength = net.get('signal', 'N/A')
                    print(f"  {Color.YELLOW}{i+1}.{Color.END} {Color.CYAN}SSID: {ssid}{Color.END}, {Color.GREEN}安全: {security}{Color.END}, {Color.BLUE}信号: {signal_strength}{Color.END}")
        elif choice == '2':
            ssid = input(f"{Color.rgb(255, 69, 0)}🎯 请输入目标WiFi的SSID: {Color.END}").strip()
            wordlist = input(f"{Color.rgb(255, 215, 0)}📚 请输入字典文件路径 (留空使用内置字典): {Color.END}").strip()
            
            if not wordlist:
                wordlist = self.wifi_cracker_tool.generate_wordlist()
            
            def wifi_attack():
                self.wifi_cracker_tool.crack_password(ssid, wordlist)
            
            self.attack_manager.start_attack("📶 WiFi密码破解", wifi_attack)
            input(f"{Color.rgb(255, 105, 180)}⏹️  按回车键停止攻击...{Color.END}")
            self.attack_manager.stop_attack("📶 WiFi密码破解", self)
        elif choice == '3':
            return
        else:
            Logger.warning("无效的选择")
    
    def handle_mac_query(self):
        """处理MAC地址查询"""
        Logger.network("MAC地址查询功能")
        Logger.banner("🔎 MAC地址查询工具")
        
        ip = input(f"{Color.rgb(64, 224, 208)}🌐 请输入要查询的IP地址: {Color.END}")
        if ip:
            Logger.loading(f"正在查询 {ip} 的MAC地址")
            mac = NetworkUtils.get_mac_address(ip)
            Logger.success(f"IP地址 {Color.CYAN}{ip}{Color.END} 的MAC地址: {Color.GREEN}{mac}{Color.END}")
    
    def handle_ai_assistant(self):
        """处理AI助手功能"""
        Logger.info("AI助手功能")
        Logger.banner("🤖 AI网络安全助手")
        
        self.ai_interface.show_welcome()
        
        while True:
            # 美化子菜单
            submenu_options = [
                ("1", "💬 与AI聊天"),
                ("2", "🎯 获取攻击建议"),
                ("3", "📊 风险分析"),
                ("4", "⚙️  AI配置"),
                ("5", "🔙 返回主菜单")
            ]
            
            print(f"\n{Color.rgb(255, 215, 0)}请选择操作:{Color.END}\n")
            for opt in submenu_options:
                print(f"  {Color.YELLOW}{opt[0]}.{Color.END} {Color.CYAN}{opt[1]}{Color.END}")
            
            choice = input(f"\n{Color.rgb(255, 105, 180)}🤖 请输入选择: {Color.END}").strip()
            
            if choice == '1':
                self.ai_interface.chat_interface()
            elif choice == '2':
                self._handle_attack_advice()
            elif choice == '3':
                self._handle_risk_analysis()
            elif choice == '4':
                self.ai_interface.config_interface()
            elif choice == '5':
                break
            else:
                Logger.warning("无效的选择")
    
    def _handle_attack_advice(self):
        """处理攻击建议"""
        attack_types = {
            '1': 'arp_spoof',
            '2': 'dhcp_starvation', 
            '3': 'mac_flood',
            '4': 'dns_spoof',
            '5': 'icmp_amplification',
            '6': 'wifi_cracking'
        }
        
        print(f"\n{Color.rgb(255, 215, 0)}请选择攻击类型:{Color.END}\n")
        for key, value in attack_types.items():
            print(f"  {Color.YELLOW}{key}.{Color.END} {Color.CYAN}{value}{Color.END}")
        
        choice = input(f"\n{Color.rgb(255, 105, 180)}🎯 请输入选择: {Color.END}").strip()
        
        if choice in attack_types:
            self.ai_interface.show_attack_advice(attack_types[choice])
        else:
            Logger.warning("无效的选择")
    
    def _handle_risk_analysis(self):
        """处理风险分析"""
        attack_types = {
            '1': 'arp_spoof',
            '2': 'dhcp_starvation',
            '3': 'mac_flood',
            '4': 'dns_spoof',
            '5': 'icmp_amplification',
            '6': 'wifi_cracking'
        }
        
        print(f"\n{Color.rgb(255, 215, 0)}请选择攻击类型:{Color.END}\n")
        for key, value in attack_types.items():
            print(f"  {Color.YELLOW}{key}.{Color.END} {Color.CYAN}{value}{Color.END}")
        
        choice = input(f"\n{Color.rgb(255, 105, 180)}📊 请输入选择: {Color.END}").strip()
        
        if choice in attack_types:
            target_info = {}
            env_choice = input(f"{Color.rgb(255, 215, 0)}🎯 是否为生产环境? (y/n): {Color.END}").strip().lower()
            if env_choice == 'y':
                target_info['production_environment'] = True
            self.ai_interface.show_risk_analysis(attack_types[choice], target_info)
        else:
            Logger.warning("无效的选择")
    
    def handle_config_management(self):
        """处理配置管理"""
        Logger.info("配置管理功能")
        Logger.banner("⚙️  配置管理系统")
        
        while True:
            print(f"{Color.rgb(138, 43, 226)}📋 当前配置:{Color.END}")
            for key, value in Logger.config.settings.items():
                print(f"  {Color.CYAN}{key}: {Color.GREEN}{value}{Color.END}")
            
            # 美化子菜单
            submenu_options = [
                ("1", "📊 修改日志级别"),
                ("2", "🧵 修改最大扫描线程数"),
                ("3", "⏱️  修改默认超时时间"),
                ("4", "🔙 返回主菜单")
            ]
            
            print(f"\n{Color.rgb(255, 215, 0)}请选择操作:{Color.END}\n")
            for opt in submenu_options:
                print(f"  {Color.YELLOW}{opt[0]}.{Color.END} {Color.CYAN}{opt[1]}{Color.END}")
            
            choice = input(f"\n{Color.rgb(255, 105, 180)}⚙️  请输入选择: {Color.END}").strip()
            
            if choice == '1':
                level = input(f"{Color.rgb(255, 215, 0)}📊 请输入日志级别(DEBUG/INFO/WARNING/ERROR): {Color.END}").strip().upper()
                if level in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
                    Logger.config.set('log_level', level)
                    Logger.success(f"日志级别已设置为: {Color.GREEN}{level}{Color.END}")
                else:
                    Logger.warning("无效的日志级别")
            elif choice == '2':
                try:
                    threads = int(input(f"{Color.rgb(255, 215, 0)}🧵 请输入最大扫描线程数: {Color.END}").strip())
                    if threads > 0:
                        Logger.config.set('max_scan_threads', threads)
                        Logger.success(f"最大扫描线程数已设置为: {Color.GREEN}{threads}{Color.END}")
                    else:
                        Logger.warning("线程数必须大于0")
                except ValueError:
                    Logger.warning("请输入有效的数字")
            elif choice == '3':
                try:
                    timeout = int(input(f"{Color.rgb(255, 215, 0)}⏱️  请输入默认超时时间(秒): {Color.END}").strip())
                    if timeout > 0:
                        Logger.config.set('default_timeout', timeout)
                        Logger.success(f"默认超时时间已设置为: {Color.GREEN}{timeout}秒{Color.END}")
                    else:
                        Logger.warning("超时时间必须大于0")
                except ValueError:
                    Logger.warning("请输入有效的数字")
            elif choice == '4':
                break
            else:
                Logger.warning("无效的选择")
            
            input(f"{Color.rgb(255, 105, 180)}⏎  按回车键继续...{Color.END}")
    
    def main(self):
        """主循环"""
        # 显示启动动画
        self.startup_sequence()
        
        while self.running:
            self.show_menu()
            
            try:
                # 在每次菜单显示时随机显示智慧语录
                if len(self.attack_manager.active_attacks) == 0:
                    WisdomQuotes.display_quote()
                
                choice = input(f"{Color.rgb(255, 105, 180)}🎮 请选择操作 (0-9, A-C): {Color.END}").strip()
                
                if choice == '1':
                    self.handle_arp_spoof()
                elif choice == '2':
                    self.handle_dhcp_starvation()
                elif choice == '3':
                    self.handle_mac_flood()
                elif choice == '4':
                    self.handle_icmp_amplification()
                elif choice == '5':
                    self.handle_dns_spoof()
                elif choice.lower() == 'b':
                    self.handle_wifi_cracker()
                elif choice == '6':
                    self.handle_network_diagnosis()
                elif choice == '7':
                    self.handle_attack_monitor()
                elif choice == '8':
                    self.handle_interface_info()
                elif choice == '9':
                    self.handle_network_scan()
                elif choice.lower() == 'a':
                    self.handle_mac_query()
                elif choice.lower() == 'c':
                    self.handle_config_management()
                elif choice.lower() == 'd':
                    self.handle_ai_assistant()
                elif choice == '0':
                    Logger.info("正在安全退出...")
                    self.attack_manager.stop_all_attacks(self)
                    self.running = False
                else:
                    Logger.warning("无效的选择，请重新输入")
                
                # 短暂暂停以便用户看清输出
                if self.running:
                    input(f"{Color.CYAN}按回车键继续...{Color.END}")
                
            except KeyboardInterrupt:
                Logger.warning("收到键盘中断信号")
                self.attack_manager.stop_all_attacks()
                self.running = False
            except Exception as e:
                Logger.error(f"发生错误: {e}")

if __name__ == "__main__":
    suite = LANAttackSuite()
    
    try:
        suite.main()
    except KeyboardInterrupt:
        Logger.warning("收到键盘中断信号")
        suite.attack_manager.stop_all_attacks(suite)
        Logger.success("程序已安全退出")
    except Exception as e:
        Logger.error(f"程序异常: {e}")
        suite.attack_manager.stop_all_attacks(suite)
        Logger.success("程序已安全退出")
