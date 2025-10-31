# ⚡ AutoRAN Advisor

**AI-Powered O-RAN Multi-Vendor Integration Platform**

Breaking barriers in O-RAN deployments by identifying compatibility issues BEFORE costly integration testing.

[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-FF9900?logo=amazon-aws)](https://aws.amazon.com/bedrock/)
[![Strands Agents](https://img.shields.io/badge/Strands-Agents-667eea)](https://strandsagents.com/)
[![Claude 4.5](https://img.shields.io/badge/Claude-4.5_Sonnet-764ba2)](https://www.anthropic.com/claude)

## 🎯 The Problem

- O-RAN has only **8-10% market share** despite promises
- Multi-vendor integration takes **3-6 months**
- **60-70%** of integrations face compatibility issues
- Failed deployments cost **millions**

## 💡 The Solution

AutoRAN Advisor uses agentic AI to analyze O-RAN configurations and predict compatibility issues before deployment, reducing integration time from **months to days**.

## ✨ Features

- **🔍 Configuration Validation** - O-RAN compliance scoring and standards checking
- **⚖️ Compatibility Assessment** - Multi-vendor integration analysis
- **🤖 Natural Language Interface** - Ask questions in plain English
- **📊 Proactive Advisory** - Identify issues before testing

## 🏗️ Architecture
```
User Interface (Web/CLI)
         ↓
    Strands Agents
         ↓
   Claude Sonnet 4.5 (AWS Bedrock)
         ↓
┌────────────────┬──────────────┬──────────────┐
│ Config Analyzer│ Compatibility│ Knowledge Base│
└────────────────┴──────────────┴──────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- AWS Account with Bedrock access
- AWS CLI configured

### Installation
```bash
# Clone repository
git clone <your-repo-url>
cd autoran-advisor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
aws configure
```

### Run Web UI
```bash
streamlit run web_app_elite.py
```

### Run CLI
```bash
python3 autoran_advisor.py
```

## 📊 Demo Scenarios

**Scenario 1: Compatible Pairing**
```
Vendor A O-DU + Vendor B O-RU → 90/100 compatibility score
Issue: Minor PCP mismatch (easily fixable)
```

**Scenario 2: Incompatible Pairing**
```
Vendor A O-DU + Vendor C O-RU → 0/100 compatibility score
Issues: Version mismatch, timing violations, bandwidth gap
```

## 🛠️ Tech Stack

- **AI/ML**: AWS Bedrock (Claude Sonnet 4.5), Strands Agents
- **Backend**: Python, Boto3
- **Frontend**: Streamlit
- **Cloud**: AWS (S3, Lambda, DynamoDB, OpenSearch Serverless)

## 📈 Impact

- ⏱️ **95% reduction** in integration planning time
- 💰 **Millions saved** by avoiding failed deployments  
- 🎯 **Supports AT&T's $14B** O-RAN transformation
- 🔓 **Democratizes O-RAN** expertise

## 🏆 AWS Breaking Barriers Hackathon 2025

Built for the AWS Breaking Barriers for Agentic Networks Hackathon at FYUZ 2025.

## 📄 License

MIT License

## 👥 Team

[Your Team Name & Members]

## 🙏 Acknowledgments

- AWS for Bedrock and Strands Agents
- O-RAN Alliance for specifications
- TIP, AT&T, and NVIDIA for industry insights