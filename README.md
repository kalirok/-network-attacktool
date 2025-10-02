# 🚀 Network Attacktool - 网络安全渗透测试套件

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)
![Version](https://img.shields.io/badge/Version-3.0.0-orange.svg)

✨ **专业级网络安全渗透测试工具集合** ✨

</div>

## 📖 项目简介

**Network Attacktool** 是一个集成了多种网络安全攻击和渗透测试工具的综合套件，专为网络安全研究人员、渗透测试工程师和安全爱好者设计。本项目采用模块化架构，界面美观，功能强大，支持多种网络攻击技术。

### 🎯 核心特性

- 🎨 **精美界面**: 支持彩色输出、图标和动画效果
- 🔧 **模块化设计**: 每个攻击工具独立模块，易于扩展
- 📊 **实时监控**: 攻击状态实时显示和监控
- 🛡️ **安全退出**: 完善的异常处理和资源清理机制
- 🌐 **多协议支持**: 支持ARP、DHCP、DNS、ICMP等多种协议

---

## 🏗️ 项目架构

```
network-Attacktool/
├── 📄 netattack.py              # 主程序 - 集成所有工具
├── 🔧 arp_spoof_advanced.py      # ARP欺骗攻击模块
├── 🌐 dhcp_starvation.py         # DHCP饥饿攻击模块
├── 🔍 dns_spoof.py               # DNS欺骗攻击模块
├── ⚡ icmp_amplification.py      # ICMP放大攻击模块
├── 🌊 mac_flood.py               # MAC洪泛攻击模块
├── 📶 wifi_password_cracker.py   # WiFi密码破解模块
└── 📁 __pycache__/              # Python缓存文件
```

---

## 🛠️ 工具功能详解

### 1. 🎯 ARP欺骗攻击 (`arp_spoof_advanced.py`)

**功能描述**: 通过发送伪造的ARP响应包，实现中间人攻击，截获目标主机的网络流量。

#### 🔧 功能特性：
- ✅ **网络扫描**: 自动扫描局域网内活跃设备
- ✅ **单目标攻击**: 针对单个目标进行ARP欺骗
- ✅ **多目标攻击**: 同时攻击多个目标主机
- ✅ **数据包嗅探**: 实时捕获和分析网络流量
- ✅ **网络诊断**: 检测网络中的ARP欺骗攻击

#### 📋 使用场景：
- 网络流量监控和分析
- 中间人攻击演示
- 网络安全教学和研究

#### 🚀 命令示例：
```bash
# 扫描网络设备
python3 netattack.py
# 选择1 → 1 (扫描网络)

# 单目标ARP欺骗
python3 netattack.py
# 选择1 → 2 → 输入目标IP、网关IP、网络接口
```

---

### 2. 🕷️ DHCP饥饿攻击 (`dhcp_starvation.py`)

**功能描述**: 通过发送大量DHCP请求，耗尽DHCP服务器的IP地址池，导致新设备无法获取IP地址。

#### 🔧 功能特性：
- ✅ **多线程攻击**: 支持多线程并发攻击
- ✅ **自定义接口**: 指定网络接口进行攻击
- ✅ **实时监控**: 显示攻击进度和效果
- ✅ **资源管理**: 自动管理攻击线程

#### 📋 使用场景：
- DHCP服务压力测试
- 网络服务可用性测试
- 无线网络渗透测试

#### 🚀 命令示例：
```bash
python3 netattack.py
# 选择2 → 输入网络接口和线程数量
```

---

### 3. 🌊 MAC洪泛攻击 (`mac_flood.py`)

**功能描述**: 向交换机发送大量伪造的MAC地址数据包，导致交换机MAC地址表溢出，实现网络监听。

#### 🔧 功能特性：
- ✅ **MAC地址伪造**: 生成随机MAC地址
- ✅ **流量控制**: 可调节攻击强度
- ✅ **接口选择**: 支持指定网络接口
- ✅ **性能优化**: 高效的包发送机制

#### 📋 使用场景：
- 交换机安全测试
- 网络监听和嗅探
- 网络设备压力测试

#### 🚀 命令示例：
```bash
python3 netattack.py
# 选择3 → 输入网络接口和线程数量
```

---

### 4. ⚡ ICMP放大攻击 (`icmp_amplification.py`)

**功能描述**: 利用ICMP协议的放大效应，向目标发送大量数据包，实现DDoS攻击效果。

#### 🔧 功能特性：
- ✅ **多种攻击模式**: 
  - 标准ICMP放大攻击
  - Smurf攻击（利用广播地址）
  - Ping洪水攻击
  - 多线程并发攻击
- ✅ **参数定制**: 可调节包大小和发送速率
- ✅ **广播计算**: 自动计算网络广播地址

#### 📋 使用场景：
- DDoS攻击演示
- 网络设备抗压测试
- 安全防护方案验证

#### 🚀 命令示例：
```bash
python3 netattack.py
# 选择4 → 选择攻击模式 → 输入目标IP和参数
```

---

### 5. 🌐 DNS欺骗攻击 (`dns_spoof.py`)

**功能描述**: 伪造DNS响应，将域名解析指向恶意服务器，实现钓鱼攻击或流量重定向。

#### 🔧 功能特性：
- ✅ **域名列表支持**: 支持多个域名同时欺骗
- ✅ **自定义重定向**: 指定虚假IP地址
- ✅ **实时拦截**: 实时捕获和修改DNS请求
- ✅ **协议分析**: DNS协议深度解析

#### 📋 使用场景：
- 网络钓鱼攻击演示
- DNS安全测试
- 流量监控和重定向

#### 🚀 命令示例：
```bash
python3 netattack.py
# 选择5 → 输入网络接口、域名列表和虚假IP
```

---

### 6. 📶 WiFi密码破解 (`wifi_password_cracker.py`)

**功能描述**: 扫描附近WiFi网络，并使用字典攻击方式尝试破解WiFi密码。

#### 🔧 功能特性：
- ✅ **网络扫描**: 自动发现附近WiFi网络
- ✅ **字典攻击**: 支持自定义字典文件
- ✅ **内置字典**: 提供常用密码字典
- ✅ **进度显示**: 实时显示破解进度

#### 📋 使用场景：
- WiFi安全评估
- 无线网络渗透测试
- 密码强度测试

#### 🚀 命令示例：
```bash
python3 netattack.py
# 选择B → 选择扫描或破解模式
```

---

## 🎨 界面特色

### 🌈 视觉设计
- **彩色终端输出**: 使用ANSI颜色代码实现丰富的视觉效果
- **图标集成**: 每个功能都有对应的表情图标
- **渐变效果**: 支持RGB渐变文字显示
- **动画加载**: 进度条和旋转光标动画

### 📊 信息显示
- **实时状态**: 显示当前时间、活跃攻击数量
- **智慧语录**: 随机显示网络安全相关名言
- **系统信息**: Python版本、操作系统信息
- **日志系统**: 分级日志输出，支持调试模式

### 🎮 交互体验
- **菜单导航**: 清晰的数字和字母选项
- **输入验证**: 完善的参数检查和错误处理
- **快捷键支持**: 支持键盘快捷键操作
- **批量操作**: 支持多目标同时操作

---

## 🚀 快速开始

### 环境要求
- **Python版本**: 3.8+
- **操作系统**: Linux / macOS / Windows (建议Linux)
- **权限要求**: 需要root权限（部分功能）

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/your-username/network-attacktool.git
cd network-attacktool
```

2. **安装依赖**
```bash
# 大多数系统已包含所需依赖
# 如需额外依赖，请参考 requirements.txt
```

3. **运行程序**
```bash
# 需要root权限运行
sudo python3 netattack.py
```

### 🎯 使用示例

```bash
# 1. 启动程序
sudo python3 netattack.py

# 2. 显示启动动画和智慧语录
# 3. 选择相应功能编号
# 4. 按照提示输入参数
# 5. 开始攻击/测试
# 6. 按回车键停止攻击
# 7. 选择0安全退出
```

---

## ⚠️ 免责声明

### 🛡️ 法律声明

**重要提示**: 本工具仅用于：
- 🔒 **授权的安全测试**
- 📚 **网络安全教学和研究**
- 🛡️ **个人网络环境测试**

**禁止用于**:
- ❌ **未经授权的网络攻击**
- ❌ **非法入侵他人系统**
- ❌ **任何违法活动**

### 🔒 使用规范
1. **仅限授权测试**: 仅在获得明确授权的情况下使用
2. **遵守法律法规**: 严格遵守当地网络安全法律法规
3. **责任自负**: 使用者对自身行为承担全部责任
4. **教育目的**: 推荐用于学习和研究目的

---

## 🛠️ 技术架构

### 📁 核心模块

```python
# 主要类结构
class LANAttackSuite:          # 主程序类
class AttackManager:           # 攻击管理
class Logger:                  # 日志系统
class Color:                   # 颜色管理
class StartupAnimation:        # 启动动画
class WisdomQuotes:            # 智慧语录
class NetworkUtils:            # 网络工具
class NetworkDiagnosis:        # 网络诊断
```

### 🔧 技术特性
- **多线程支持**: 支持并发攻击操作
- **异常处理**: 完善的错误处理和资源清理
- **配置管理**: 可配置的日志级别和参数
- **模块化**: 易于扩展新攻击模块

---

## 🤝 贡献指南

我们欢迎社区贡献！请遵循以下步骤：

1. **Fork 项目**
2. **创建功能分支** (`git checkout -b feature/AmazingFeature`)
3. **提交更改** (`git commit -m 'Add some AmazingFeature'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **创建 Pull Request**

### 📋 贡献规范
- 遵循PEP 8代码规范
- 添加适当的注释和文档
- 测试新功能的兼容性
- 更新README文档

---

## 📄 许可证

本项目采用 **MIT 许可证** - 详见 [LICENSE](LICENSE) 文件

---

## 📞 联系我们

如有问题或建议，请通过以下方式联系：

- 📧 **邮箱**: your-email@example.com
- 💬 **Issues**: [GitHub Issues](https://github.com/your-username/network-attacktool/issues)
- 📚 **文档**: 本项目文档

---

## ⭐ 致谢

感谢所有为网络安全事业贡献的开发者！

---

<div align="center">

**⚠️ 再次提醒：请负责任地使用本工具！**

**网络安全，人人有责** 🔒

</div>