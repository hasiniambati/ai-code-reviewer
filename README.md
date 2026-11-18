# 🤖 Autonomous Code Review & Bug Remediation Agent

An advanced multi-agent static analysis system built with Python, LangGraph concepts, and Streamlit. It inspects source code via Abstract Syntax Tree (AST) parsing, scans for security vulnerabilities and runtime scope errors, and generates automated, clean code refactoring patches.

🌐 **Live Demo:** [View Live Streamlit Cloud Application](https://ai-code-reviewer1.streamlit.app/)

---

## 🎯 Project Overview

Standard code reviews often miss subtle runtime scoping issues or dangerous execution sinks. The **Autonomous Code Review & Bug Remediation Agent** acts as an intelligent developer assistant that automatically parses code structure, highlights missing variable initializations, detects security flaws like `eval()`, and provides immediate refactoring solutions through an interactive dashboard.

---

## 🏗️ Core Architecture & Agentic Workflow

1. **AST Parser & Syntax Inspector (`agent.py`)**
   * Parses incoming source code into an Abstract Syntax Tree.
   * Catches syntax errors, bare `except:` clauses, and global variable anti-patterns.

2. **Runtime Scope & Logic Auditor (`agent.py`)**
   * Performs local scope analysis to identify undefined variables used before initialization (e.g., missing queue or visited definitions).
   * Flags logical anomalies like loops lacking return statements.

3. **Security Vulnerability Scanner (`agent.py`)**
   * Scans for dangerous execution sinks such as `eval()` and `exec()`.

---

## 📂 Project Structure

```text
ai-code-reviewer/
│
├── agent.py             # Multi-agent AST inspector, scope auditor & refactoring logic
├── app.py               # Streamlit user interface dashboard
├── requirements.txt     # Python package dependencies
├── .gitignore           # Git ignore configuration
└── README.md            # Project documentation
