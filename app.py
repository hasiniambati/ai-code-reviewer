import streamlit as st
from agent import CodeReviewAgentGraph

st.set_page_config(
    page_title="Autonomous Code Review & Bug Remediation Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Autonomous Code Review & Bug Remediation Agent")
st.caption("LangGraph Multi-Agent Static Analysis & Automated Refactoring Pipeline")
st.markdown("---")

page = st.sidebar.radio("Navigation", ["Submit Code Review", "System Architecture"])

if page == "Submit Code Review":
    st.subheader("Source Code Audit & Vulnerability Scanner")

    sample_code = """def calculate_total(user_input):
    try:
        result = eval(user_input)
        return result
    except:
        return None"""

    code_input = st.text_area("Source Code Input", value=sample_code, height=180)

    if st.button("Run Multi-Agent Review"):
        if not code_input.strip():
            st.warning("Please provide code to review.")
        else:
            with st.spinner("Analyzing AST and security patterns..."):
                result = CodeReviewAgentGraph.audit_code(code_input)

            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Audit Status:** {result['status']}")
            with col2:
                st.success(f"**Confidence:** {result['confidence']}")

            st.markdown("### 🔍 Identified Vulnerabilities & Issues")
            for issue in result["issues"]:
                st.markdown(f"- {issue}")

            st.markdown("### 💡 Recommended Fixes")
            for sug in result["suggestions"]:
                st.markdown(f"- {sug}")

            st.markdown("### ✨ Automated Refactored Patch")
            st.code(result["refactored_code"], language="python")

elif page == "System Architecture":
    st.subheader("LangGraph Multi-Agent Workflow")
    st.markdown("1. **AST Parser Node:** Inspects syntax trees and scoping rules.")
    st.markdown("2. **Security Vulnerability Scanner:** Detects dangerous execution sinks like `eval()`.")
    st.markdown("3. **Refactoring Node:** Applies automated fixes and secure code replacements.")