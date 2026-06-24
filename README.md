\# Multi-Agent Prompt Factory



一个基于 CrewAI 的多 Agent Prompt 生成器。（使用了gpt5.5进行code）



\## 功能



\- 分析用户需求

\- 生成 Prompt 初稿

\- 审查 Prompt 问题

\- 输出最终优化版 Prompt

\- 支持 Docker 运行
## Windows 版本下载

前往 Releases 页面下载最新版本：

https://github.com/opsasa/multi-agent-prompt-factory/releases
不需要安装 Python
不需要安装 Docker
需要自己配置 .env 和 API Key

## Windows 无 Docker 运行

如果你没有 Docker，也可以直接用 Python 运行。

### 1. 安装 Python

请安装 Python 3.10 或以上版本。

### 2. 下载项目

点击 GitHub 页面右上角：

Code → Download ZIP

3. 配置 API Key

复制 .env.example，重命名为 .env。

然后填写：

DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
MODEL=deepseek/deepseek-chat
TEMPERATURE=0.5
4. 安装依赖

双击：

setup_windows.bat
5. 运行程序

双击：

run_windows.bat

运行完成后，结果会保存到：

output/final_prompt.md

\## 技术栈
```text


\- Python

\- CrewAI

\- LiteLLM

\- Docker

\- python-dotenv



\## 项目结构



```text

.

├─ app.py

├─ requirements.txt

├─ Dockerfile

├─ docker-compose.yml

├─ .env.example

└─ README.md
