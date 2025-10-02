# 🚀 Network Attacktool AI - Network Security Penetration Testing Suite

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)
![Version](https://img.shields.io/badge/Version-3.0.0-orange.svg)

✨ **Professional Network Security Penetration Testing Toolkit** ✨

</div>

## 📖 Project Introduction

**Network Attacktool** is a comprehensive suite integrating various network security attacks and penetration testing tools, designed specifically for network security researchers, penetration testing engineers, and security enthusiasts. This project features a modular architecture, beautiful interface, powerful functionality, and supports multiple network attack techniques.

### 🎯 Core Features

- 🎨 **Beautiful Interface**: Supports colored output, icons, and animation effects
- 🔧 **Modular Design**: Each attack tool is an independent module, easy to extend
- 📊 **Real-time Monitoring**: Real-time attack status display and monitoring
- 🛡️ **Safe Exit**: Comprehensive exception handling and resource cleanup mechanisms
- 🌐 **Multi-protocol Support**: Supports ARP, DHCP, DNS, ICMP and other protocols
- 🤖 **AI Assistant**: Integrated Moonshot AI API for real-time help and attack suggestions

---

## 🏗️ Project Architecture

```
network-Attacktool/
├── 📄 netattack.py              # Main program - integrates all tools
├── 🤖 ai_assistant.py           # AI assistant module
├── 🔧 arp_spoof_advanced.py     # ARP spoofing attack module
├── 🌐 dhcp_starvation.py        # DHCP starvation attack module
├── 🔍 dns_spoof.py              # DNS spoofing attack module
├── ⚡ icmp_amplification.py     # ICMP amplification attack module
├── 🌊 mac_flood.py              # MAC flooding attack module
├── 📶 wifi_password_cracker.py  # WiFi password cracking module
├── 🧪 test_ai_assistant.py      # AI assistant test script
└── 📁 __pycache__/             # Python cache files
```

---

## 🛠️ Tool Function Details

### 1. 🎯 ARP Spoofing Attack (`arp_spoof_advanced.py`)

**Function Description**: Implements man-in-the-middle attacks by sending forged ARP response packets to intercept target host network traffic.

#### 🔧 Features:
- ✅ **Network Scanning**: Automatically scans active devices on the local network
- ✅ **Single Target Attack**: ARP spoofing against a single target
- ✅ **Multi-target Attack**: Simultaneously attacks multiple target hosts
- ✅ **Packet Sniffing**: Real-time network traffic capture and analysis
- ✅ **Network Diagnosis**: Detects ARP spoofing attacks in the network

#### 📋 Usage Scenarios:
- Network traffic monitoring and analysis
- Man-in-the-middle attack demonstrations
- Network security teaching and research

#### 🚀 Command Examples:
```bash
# Scan network devices
python3 netattack.py
# Select 1 → 1 (Scan network)

# Single target ARP spoofing
python3 netattack.py
# Select 1 → 2 → Enter target IP, gateway IP, network interface
```

---

### 2. 🕷️ DHCP Starvation Attack (`dhcp_starvation.py`)

**Function Description**: Sends a large number of DHCP requests to exhaust the DHCP server's IP address pool, preventing new devices from obtaining IP addresses.

#### 🔧 Features:
- ✅ **Multi-threaded Attack**: Supports concurrent multi-threaded attacks
- ✅ **Custom Interface**: Specify network interface for attack
- ✅ **Real-time Monitoring**: Displays attack progress and effects
- ✅ **Resource Management**: Automatic attack thread management

#### 📋 Usage Scenarios:
- DHCP service stress testing
- Network service availability testing
- Wireless network penetration testing

#### 🚀 Command Examples:
```bash
python3 netattack.py
# Select 2 → Enter network interface and thread count
```

---

### 3. 🌊 MAC Flooding Attack (`mac_flood.py`)

**Function Description**: Sends a large number of forged MAC address packets to the switch, causing the switch's MAC address table to overflow and enabling network monitoring.

#### 🔧 Features:
- ✅ **MAC Address Spoofing**: Generates random MAC addresses
- ✅ **Traffic Control**: Adjustable attack intensity
- ✅ **Interface Selection**: Supports specifying network interface
- ✅ **Performance Optimization**: Efficient packet sending mechanism

#### 📋 Usage Scenarios:
- Switch security testing
- Network monitoring and sniffing
- Network device stress testing

#### 🚀 Command Examples:
```bash
python3 netattack.py
# Select 3 → Enter network interface and thread count
```

---

### 4. ⚡ ICMP Amplification Attack (`icmp_amplification.py`)

**Function Description**: Utilizes ICMP protocol amplification effect to send a large number of packets to the target, achieving DDoS attack effect.

#### 🔧 Features:
- ✅ **Multiple Attack Modes**:
  - Standard ICMP amplification attack
  - Smurf attack (using broadcast address)
  - Ping flood attack
  - Multi-threaded concurrent attack
- ✅ **Parameter Customization**: Adjustable packet size and sending rate
- ✅ **Broadcast Calculation**: Automatic network broadcast address calculation

#### 📋 Usage Scenarios:
- DDoS attack demonstrations
- Network device stress testing
- Security protection solution verification

#### 🚀 Command Examples:
```bash
python3 netattack.py
# Select 4 → Select attack mode → Enter target IP and parameters
```

---

### 5. 🌐 DNS Spoofing Attack (`dns_spoof.py`)

**Function Description**: Forges DNS responses, redirecting domain name resolution to malicious servers, implementing phishing attacks or traffic redirection.

#### 🔧 Features:
- ✅ **Domain List Support**: Supports multiple domain spoofing simultaneously
- ✅ **Custom Redirect**: Specify fake IP address
- ✅ **Real-time Interception**: Real-time DNS request capture and modification
- ✅ **Protocol Analysis**: Deep DNS protocol analysis

#### 📋 Usage Scenarios:
- Phishing attack demonstrations
- DNS security testing
- Traffic monitoring and redirection

#### 🚀 Command Examples:
```bash
python3 netattack.py
# Select 5 → Enter network interface, domain list, and fake IP
```

---

### 6. 📶 WiFi Password Cracking (`wifi_password_cracker.py`)

**Function Description**: Scans nearby WiFi networks and attempts to crack WiFi passwords using dictionary attacks.

#### 🔧 Features:
- ✅ **Network Scanning**: Automatically discovers nearby WiFi networks
- ✅ **Dictionary Attack**: Supports custom dictionary files
- ✅ **Built-in Dictionary**: Provides common password dictionaries
- ✅ **Progress Display**: Real-time cracking progress display

#### 📋 Usage Scenarios:
- WiFi security assessment
- Wireless network penetration testing
- Password strength testing

#### 🚀 Command Examples:
```bash
python3 netattack.py
# Select B → Select scan or crack mode
```

---

### 7. 🤖 AI Assistant (`ai_assistant.py`)

**Function Description**: Integrates Moonshot AI API to provide real-time AI help, strategy suggestions, and risk assessment for network security attacks.

#### 🔧 Features:
- ✅ **Multiple AI Provider Support**: Supports Moonshot, OpenAI, DeepSeek, etc.
- ✅ **Real-time Help**: Provides real-time guidance during attacks
- ✅ **Attack Suggestions**: Professional suggestions for different attack types
- ✅ **Risk Analysis**: Analyzes attack risks and provides mitigation measures
- ✅ **Chat Mode**: Natural language conversation with AI assistant

#### 📋 Usage Scenarios:
- Learning network security techniques
- Obtaining attack strategy guidance
- Assessing attack risks
- Solving technical problems

#### 🚀 Command Examples:
```bash
python3 netattack.py
# Select D → Enter AI assistant mode
# Select 1 → Chat with AI
# Select 2 → Get attack suggestions
# Select 3 → Risk analysis
# Select 4 → Configure AI settings
```

#### 🔧 AI Assistant Configuration:
1. Select `D` in main menu to enter AI assistant
2. Select `4` to enter configuration interface
3. Set API key and enable status
4. Select AI provider (default: Moonshot)

---

## 🎨 Interface Features

### 🌈 Visual Design
- **Colored Terminal Output**: Rich visual effects using ANSI color codes
- **Icon Integration**: Each function has corresponding emoji icons
- **Gradient Effects**: Supports RGB gradient text display
- **Loading Animations**: Progress bars and spinning cursor animations

### 📊 Information Display
- **Real-time Status**: Shows current time, active attack count
- **Wisdom Quotes**: Random display of network security-related quotes
- **System Information**: Python version, operating system information
- **Logging System**: Level-based log output, supports debug mode

### 🎮 Interaction Experience
- **Menu Navigation**: Clear numeric and alphabetic options
- **Input Validation**: Comprehensive parameter checking and error handling
- **Hotkey Support**: Supports keyboard shortcut operations
- **Batch Operations**: Supports simultaneous multi-target operations

---

## 🚀 Quick Start

### Environment Requirements
- **Python Version**: 3.8+
- **Operating System**: Linux / macOS / Windows (Linux recommended)
- **Permission Requirements**: Root privileges required (some functions)

### Installation Steps

1. **Clone Repository**
```bash
git clone https://github.com/kalirok/-network-attacktool.git
cd network-attacktool
```

2. **Install Dependencies**
```bash
# Most systems already contain required dependencies
# For additional dependencies, refer to requirements.txt
```

3. **Run Program**
```bash
# Requires root privileges
sudo python3 netattack.py
```

### 🎯 Usage Examples

```bash
# 1. Start program
sudo python3 netattack.py

# 2. Display startup animation and wisdom quotes
# 3. Select corresponding function number
# 4. Enter parameters as prompted
# 5. Start attack/testing
# 6. Press Enter to stop attack
# 7. Select 0 to safely exit
```

---

## ⚠️ Disclaimer

### 🛡️ Legal Notice

**Important Notice**: This tool is only for:
- 🔒 **Authorized security testing**
- 📚 **Network security teaching and research**
- 🛡️ **Personal network environment testing**

**Prohibited for**:
- ❌ **Unauthorized network attacks**
- ❌ **Illegal intrusion into others' systems**
- ❌ **Any illegal activities**

### 🔒 Usage Guidelines
1. **Authorized Testing Only**: Use only with explicit authorization
2. **Compliance with Laws**: Strictly comply with local network security laws and regulations
3. **User Responsibility**: Users bear full responsibility for their actions
4. **Educational Purpose**: Recommended for learning and research purposes

---

## 🛠️ Technical Architecture

### 📁 Core Modules

```python
# Main class structure
class LANAttackSuite:          # Main program class
class AttackManager:           # Attack management
class Logger:                  # Logging system
class Color:                   # Color management
class StartupAnimation:        # Startup animation
class WisdomQuotes:            # Wisdom quotes
class NetworkUtils:            # Network utilities
class NetworkDiagnosis:        # Network diagnosis
```

### 🔧 Technical Features
- **Multi-threading Support**: Supports concurrent attack operations
- **Exception Handling**: Comprehensive error handling and resource cleanup
- **Configuration Management**: Configurable log levels and parameters
- **Modularity**: Easy to extend with new attack modules

---

## 🤝 Contribution Guidelines

We welcome community contributions! Please follow these steps:

1. **Fork the Project**
2. **Create Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit Changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to Branch** (`git push origin feature/AmazingFeature`)
5. **Create Pull Request**

### 📋 Contribution Standards
- Follow PEP 8 code standards
- Add appropriate comments and documentation
- Test new feature compatibility
- Update README documentation

---

## 📄 License

This project uses **MIT License** - see [LICENSE](LICENSE) file for details

---

## 📞 Contact Us

For questions or suggestions, please contact:

- 📧 **Email**: 3993053612@qq.com
- 💬 **Issues**: [GitHub Issues](https://github.com/your-username/network-attacktool/issues)
- 📚 **Documentation**: This project documentation

---

## ⭐ Acknowledgments

Thanks to all developers contributing to the network security community!

---

<div align="center">

**⚠️ Reminder: Please use this tool responsibly!**

**Network Security, Everyone's Responsibility** 🔒

</div>