#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI助手模块 - 为网络安全攻击工具提供实时AI帮助
支持多种AI API，提供攻击策略建议、风险评估和实时指导
"""

import json
import time
import threading
import requests
from typing import Dict, List, Optional
import sys
import os

class AIAssistant:
    """AI助手核心类 - 支持多种AI API集成"""
    
    def __init__(self):
        self.api_config = {
            'moonshot': {
                'base_url': 'https://api.moonshot.cn/v1',
                'api_key': '',
                'model': 'moonshot-v1-8k'
            },
            'openai': {
                'base_url': 'https://api.openai.com/v1',
                'api_key': '',
                'model': 'gpt-3.5-turbo'
            },
            'deepseek': {
                'base_url': 'https://api.deepseek.com/v1',
                'api_key': '',
                'model': 'deepseek-chat'
            },
            'local': {
                'base_url': 'http://localhost:8080/v1',
                'api_key': '',
                'model': 'local-model'
            }
        }
        
        self.active_provider = 'moonshot'  # 默认使用Moonshot
        self.conversation_history = []
        self.max_history = 10
        self.enabled = False
        
        # 攻击策略知识库
        self.attack_knowledge = {
            'arp_spoof': {
                'description': 'ARP欺骗攻击 - 中间人攻击技术',
                'risks': ['网络中断', '数据泄露', '法律风险'],
                'mitigations': ['使用ARP监控工具', '启用端口安全', '静态ARP绑定'],
                'best_practices': ['仅在授权环境测试', '监控网络流量', '及时恢复ARP表']
            },
            'dhcp_starvation': {
                'description': 'DHCP饥饿攻击 - 耗尽DHCP服务器资源',
                'risks': ['网络服务中断', '新设备无法接入'],
                'mitigations': ['DHCP防护机制', '端口安全', 'MAC地址限制'],
                'best_practices': ['测试DHCP服务稳定性', '监控DHCP日志']
            },
            'mac_flood': {
                'description': 'MAC洪泛攻击 - 交换机MAC表溢出',
                'risks': ['网络性能下降', '数据包嗅探'],
                'mitigations': ['端口安全', 'MAC地址限制', '风暴控制'],
                'best_practices': ['测试交换机安全配置']
            },
            'dns_spoof': {
                'description': 'DNS欺骗攻击 - 域名解析重定向',
                'risks': ['钓鱼攻击', '数据窃取', '中间人攻击'],
                'mitigations': ['DNS安全扩展', 'DNS监控', 'HTTPS强制'],
                'best_practices': ['验证DNS响应', '使用安全DNS']
            },
            'icmp_amplification': {
                'description': 'ICMP放大攻击 - DDoS攻击技术',
                'risks': ['网络拥塞', '服务不可用', '法律风险'],
                'mitigations': ['ICMP过滤', '流量监控', 'DDoS防护'],
                'best_practices': ['仅用于压力测试']
            },
            'wifi_cracking': {
                'description': 'WiFi密码破解 - 无线网络渗透',
                'risks': ['未授权访问', '隐私泄露', '法律风险'],
                'mitigations': ['强密码策略', 'WPA3加密', 'MAC过滤'],
                'best_practices': ['仅在授权环境测试']
            }
        }
    
    def set_api_key(self, provider: str, api_key: str):
        """设置API密钥"""
        if provider in self.api_config:
            self.api_config[provider]['api_key'] = api_key
            return True
        return False
    
    def set_active_provider(self, provider: str):
        """设置活跃的AI提供商"""
        if provider in self.api_config:
            self.active_provider = provider
            return True
        return False
    
    def enable_assistant(self):
        """启用AI助手"""
        self.enabled = True
    
    def disable_assistant(self):
        """禁用AI助手"""
        self.enabled = False
    
    def add_to_history(self, role: str, content: str):
        """添加对话历史"""
        self.conversation_history.append({'role': role, 'content': content})
        # 限制历史记录长度
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def call_ai_api(self, prompt: str, attack_context: Dict = None) -> Optional[str]:
        """调用AI API获取响应"""
        if not self.enabled:
            return "AI助手当前已禁用，请在配置中启用"
        
        config = self.api_config[self.active_provider]
        
        if not config['api_key']:
            return f"未设置{self.active_provider.upper()} API密钥，请在配置中设置"
        
        # 构建完整的提示词
        full_prompt = self._build_prompt(prompt, attack_context)
        
        try:
            if self.active_provider in ['openai', 'deepseek', 'moonshot']:
                return self._call_openai_compatible_api(config, full_prompt)
            elif self.active_provider == 'local':
                return self._call_local_api(config, full_prompt)
            else:
                return "不支持的AI提供商"
        except Exception as e:
            return f"AI API调用失败: {str(e)}"
    
    def _build_prompt(self, user_prompt: str, attack_context: Dict = None) -> str:
        """构建完整的提示词"""
        system_prompt = """你是一个专业的网络安全专家AI助手，专门为渗透测试和安全研究提供指导。

请遵守以下原则：
1. 仅提供合法的安全测试指导
2. 强调授权测试的重要性
3. 分析攻击的风险和缓解措施
4. 提供实用的技术建议
5. 提醒用户遵守法律法规

当前工具支持的攻击类型：ARP欺骗、DHCP饥饿、MAC洪泛、DNS欺骗、ICMP放大、WiFi破解"""
        
        context_info = ""
        if attack_context:
            attack_type = attack_context.get('attack_type', '')
            if attack_type in self.attack_knowledge:
                knowledge = self.attack_knowledge[attack_type]
                context_info = f"\n\n当前攻击类型: {attack_type}\n描述: {knowledge['description']}\n"
        
        return f"{system_prompt}{context_info}\n\n用户问题: {user_prompt}"
    
    def _call_openai_compatible_api(self, config: Dict, prompt: str) -> str:
        """调用OpenAI兼容的API"""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {config['api_key']}"
        }
        
        data = {
            'model': config['model'],
            'messages': [
                {'role': 'system', 'content': '你是一个网络安全专家助手'},
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': 1000,
            'temperature': 0.7
        }
        
        response = requests.post(
            f"{config['base_url']}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"API调用失败: {response.status_code} - {response.text}"
    
    def _call_local_api(self, config: Dict, prompt: str) -> str:
        """调用本地API"""
        # 简化的本地API调用
        headers = {
            'Content-Type': 'application/json'
        }
        
        if config['api_key']:
            headers['Authorization'] = f"Bearer {config['api_key']}"
        
        data = {
            'prompt': prompt,
            'max_tokens': 1000
        }
        
        try:
            response = requests.post(
                f"{config['base_url']}/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('text', result.get('response', 'API响应格式未知'))
            else:
                return f"本地API调用失败: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"本地API连接失败: {str(e)}"
    
    def get_attack_advice(self, attack_type: str, context: Dict = None) -> str:
        """获取特定攻击类型的建议"""
        if attack_type not in self.attack_knowledge:
            return f"未知的攻击类型: {attack_type}"
        
        knowledge = self.attack_knowledge[attack_type]
        
        advice = f"""
🎯 {attack_type.upper()} 攻击建议

📖 攻击描述: {knowledge['description']}

⚠️  主要风险:
"""
        
        for risk in knowledge['risks']:
            advice += f"  • {risk}\n"
        
        advice += f"""
🛡️  防护措施:
"""
        
        for mitigation in knowledge['mitigations']:
            advice += f"  • {mitigation}\n"
        
        advice += f"""
💡 最佳实践:
"""
        
        for practice in knowledge['best_practices']:
            advice += f"  • {practice}\n"
        
        return advice
    
    def analyze_attack_risk(self, attack_type: str, target_info: Dict) -> Dict:
        """分析攻击风险"""
        risk_levels = {
            'arp_spoof': '高风险',
            'dhcp_starvation': '中风险',
            'mac_flood': '中风险',
            'dns_spoof': '高风险',
            'icmp_amplification': '极高风险',
            'wifi_cracking': '高风险'
        }
        
        risk_score = {
            '低风险': 1,
            '中风险': 2,
            '高风险': 3,
            '极高风险': 4
        }
        
        base_risk = risk_levels.get(attack_type, '未知风险')
        
        # 基于目标信息调整风险等级
        adjusted_risk = base_risk
        if target_info.get('production_environment', False):
            risk_level = risk_score.get(base_risk, 2)
            if risk_level < 4:
                adjusted_risk = list(risk_levels.keys())[risk_level]
        
        return {
            'attack_type': attack_type,
            'base_risk': base_risk,
            'adjusted_risk': adjusted_risk,
            'recommendation': f"建议在{adjusted_risk}环境下谨慎使用此攻击"
        }
    
    def real_time_help(self, attack_type: str, current_step: str) -> str:
        """提供实时帮助"""
        help_responses = {
            'arp_spoof': {
                'scanning': "正在扫描网络设备... 建议先确认目标网络范围",
                'attacking': "正在进行ARP欺骗... 注意监控网络流量变化",
                'recovery': "正在恢复ARP表... 确保网络恢复正常"
            },
            'dhcp_starvation': {
                'starting': "开始DHCP饥饿攻击... 监控DHCP服务器响应",
                'flooding': "正在发送DHCP请求... 观察IP地址池状态"
            },
            'mac_flood': {
                'starting': "开始MAC洪泛... 注意交换机性能影响",
                'flooding': "正在发送伪造MAC包... 监控网络延迟"
            }
        }
        
        attack_help = help_responses.get(attack_type, {})
        return attack_help.get(current_step, "继续执行当前操作...")


class AIHelpInterface:
    """AI帮助界面类 - 提供用户交互界面"""
    
    def __init__(self, ai_assistant: AIAssistant):
        self.ai = ai_assistant
        self.color = self._init_colors()
    
    def _init_colors(self):
        """初始化颜色类（简化版）"""
        class SimpleColor:
            RED = '\033[91m'
            GREEN = '\033[92m'
            YELLOW = '\033[93m'
            BLUE = '\033[94m'
            PURPLE = '\033[95m'
            CYAN = '\033[96m'
            WHITE = '\033[97m'
            END = '\033[0m'
            BOLD = '\033[1m'
        return SimpleColor()
    
    def show_welcome(self):
        """显示欢迎信息"""
        print(f"\n{self.color.CYAN}{self.color.BOLD}🤖 AI网络安全助手已启动{self.color.END}")
        print(f"{self.color.BLUE}当前AI提供商: {self.color.YELLOW}{self.ai.active_provider.upper()}{self.color.END}")
        print(f"{self.color.BLUE}助手状态: {self.color.GREEN if self.ai.enabled else self.color.RED}{'已启用' if self.ai.enabled else '已禁用'}{self.color.END}")
    
    def chat_interface(self):
        """聊天界面"""
        print(f"\n{self.color.PURPLE}💬 进入AI助手聊天模式{self.color.END}")
        print(f"{self.color.YELLOW}输入 'quit' 退出聊天，'help' 查看帮助{self.color.END}")
        
        while True:
            try:
                user_input = input(f"\n{self.color.GREEN}🤔 你的问题: {self.color.END}").strip()
                
                if user_input.lower() == 'quit':
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                elif not user_input:
                    continue
                
                print(f"{self.color.BLUE}🔄 AI正在思考...{self.color.END}")
                
                response = self.ai.call_ai_api(user_input)
                
                print(f"\n{self.color.CYAN}🤖 AI助手: {self.color.END}")
                print(f"{self.color.WHITE}{response}{self.color.END}")
                
            except KeyboardInterrupt:
                print(f"\n{self.color.YELLOW}退出聊天模式{self.color.END}")
                break
            except Exception as e:
                print(f"{self.color.RED}错误: {e}{self.color.END}")
    
    def show_attack_advice(self, attack_type: str):
        """显示攻击建议"""
        advice = self.ai.get_attack_advice(attack_type)
        print(f"\n{self.color.CYAN}{advice}{self.color.END}")
    
    def show_risk_analysis(self, attack_type: str, target_info: Dict = None):
        """显示风险分析"""
        if target_info is None:
            target_info = {}
        
        analysis = self.ai.analyze_attack_risk(attack_type, target_info)
        
        print(f"\n{self.color.PURPLE}📊 风险分析报告{self.color.END}")
        print(f"{self.color.BLUE}攻击类型: {self.color.WHITE}{analysis['attack_type']}{self.color.END}")
        print(f"{self.color.BLUE}基础风险: {self.color.YELLOW}{analysis['base_risk']}{self.color.END}")
        print(f"{self.color.BLUE}调整风险: {self.color.RED if analysis['adjusted_risk'] in ['高风险', '极高风险'] else self.color.YELLOW}{analysis['adjusted_risk']}{self.color.END}")
        print(f"{self.color.BLUE}建议: {self.color.GREEN}{analysis['recommendation']}{self.color.END}")
    
    def show_help(self):
        """显示帮助信息"""
        help_text = f"""
{self.color.CYAN}🤖 AI助手使用指南{self.color.END}

{self.color.YELLOW}可用命令:{self.color.END}
  • {self.color.GREEN}attack <类型>{self.color.END} - 获取特定攻击的建议
  • {self.color.GREEN}risk <类型>{self.color.END} - 分析攻击风险
  • {self.color.GREEN}config{self.color.END} - 配置AI设置
  • {self.color.GREEN}help{self.color.END} - 显示此帮助
  • {self.color.GREEN}quit{self.color.END} - 退出聊天

{self.color.YELLOW}支持的攻击类型:{self.color.END}
  • arp_spoof - ARP欺骗攻击
  • dhcp_starvation - DHCP饥饿攻击
  • mac_flood - MAC洪泛攻击
  • dns_spoof - DNS欺骗攻击
  • icmp_amplification - ICMP放大攻击
  • wifi_cracking - WiFi密码破解

{self.color.YELLOW}示例:{self.color.END}
  • "如何配置ARP欺骗攻击？"
  • "attack arp_spoof"
  • "risk dns_spoof"
"""
        print(help_text)
    
    def config_interface(self):
        """配置界面"""
        print(f"\n{self.color.PURPLE}⚙️  AI助手配置{self.color.END}")
        
        while True:
            print(f"\n{self.color.BLUE}当前配置:{self.color.END}")
            print(f"  提供商: {self.color.YELLOW}{self.ai.active_provider}{self.color.END}")
            print(f"  状态: {self.color.GREEN if self.ai.enabled else self.color.RED}{'已启用' if self.ai.enabled else '已禁用'}{self.color.END}")
            
            print(f"\n{self.color.YELLOW}配置选项:{self.color.END}")
            print(f"  1. 切换AI提供商")
            print(f"  2. 设置API密钥")
            print(f"  3. 启用/禁用助手")
            print(f"  4. 返回")
            
            choice = input(f"\n{self.color.GREEN}请选择: {self.color.END}").strip()
            
            if choice == '1':
                self._switch_provider()
            elif choice == '2':
                self._set_api_key()
            elif choice == '3':
                self._toggle_assistant()
            elif choice == '4':
                break
            else:
                print(f"{self.color.RED}无效选择{self.color.END}")
    
    def _switch_provider(self):
        """切换AI提供商"""
        print(f"\n{self.color.YELLOW}可用提供商:{self.color.END}")
        providers = list(self.ai.api_config.keys())
        for i, provider in enumerate(providers, 1):
            print(f"  {i}. {provider}")
        
        try:
            choice = int(input(f"\n{self.color.GREEN}选择提供商: {self.color.END}")) - 1
            if 0 <= choice < len(providers):
                self.ai.set_active_provider(providers[choice])
                print(f"{self.color.GREEN}已切换到 {providers[choice]}{self.color.END}")
            else:
                print(f"{self.color.RED}无效选择{self.color.END}")
        except ValueError:
            print(f"{self.color.RED}请输入数字{self.color.END}")
    
    def _set_api_key(self):
        """设置API密钥"""
        provider = self.ai.active_provider
        current_key = self.ai.api_config[provider]['api_key']
        
        if current_key:
            masked_key = current_key[:4] + '*' * (len(current_key) - 8) + current_key[-4:]
            print(f"{self.color.YELLOW}当前{provider} API密钥: {masked_key}{self.color.END}")
        else:
            print(f"{self.color.RED}未设置{provider} API密钥{self.color.END}")
        
        new_key = input(f"\n{self.color.GREEN}输入新的API密钥 (留空保持当前): {self.color.END}").strip()
        
        if new_key:
            if self.ai.set_api_key(provider, new_key):
                print(f"{self.color.GREEN}API密钥已更新{self.color.END}")
            else:
                print(f"{self.color.RED}更新失败{self.color.END}")
    
    def _toggle_assistant(self):
        """切换助手状态"""
        if self.ai.enabled:
            self.ai.disable_assistant()
            print(f"{self.color.YELLOW}AI助手已禁用{self.color.END}")
        else:
            self.ai.enable_assistant()
            print(f"{self.color.GREEN}AI助手已启用{self.color.END}")


def create_ai_assistant():
    """创建AI助手实例"""
    return AIAssistant()

def create_ai_interface(ai_assistant):
    """创建AI界面实例"""
    return AIHelpInterface(ai_assistant)

if __name__ == "__main__":
    # 测试代码
    ai = create_ai_assistant()
    interface = create_ai_interface(ai)
    
    interface.show_welcome()
    interface.chat_interface()