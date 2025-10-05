import re
import pyperclip
import streamlit as st
from streamlit_markdown import markdown

st.set_page_config(page_title="Coala Markdown Cleaner", layout="wide")

# --- Header ---
st.image("coala.png", width=120)
st.title("🧹 Coala Markdown Cleaner")

# --- Helper: clean Markdown ---
def clean_text(text: str) -> str:
    text = re.sub(r"<span[^>]*>", "", text)
    text = re.sub(r"</span>", "", text)
    text = re.sub(r"mso-[^:;]+:[^;\"']+;?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"font-[^:;]+:[^;\"']+;?", "", text, flags=re.IGNORECASE)
    text = re.sub(r' style="[^"]*"', "", text)
    text = text.replace("", "- ").replace("–", "- ")
    text = re.sub(r"@cols=\d+(:@rows=\d+)?[:：]?", "", text)
    text = re.sub(r"@rows=\d+[:：]?", "", text)
    text = re.sub(r"^(#+)[ \t]+", r"\1 ", text, flags=re.MULTILINE)
    lines = []
    for line in text.splitlines():
        if line.strip().startswith("#"):
            line = re.sub(r"[ \t\u00A0]+", " ", line)
        lines.append(line)
    text = "\n".join(lines)

    # Bold first row of Markdown tables
    def bold_table_headers(md_in: str) -> str:
        lines = md_in.splitlines()
        out = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.strip().startswith("|") and i + 1 < len(lines):
                next_line = lines[i + 1]
                if re.match(r'^\s*\|[-: ]+\|', next_line):
                    cols = [c.strip() for c in line.strip().strip("|").split("|")]
                    bolded = "| " + " | ".join([f"**{c}**" if c else "" for c in cols]) + " |"
                    out.append(bolded)
                    out.append(next_line)
                    i += 2
                    continue
            out.append(line)
            i += 1
        return "\n".join(out)

    text = bold_table_headers(text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# --- UI ---
input_text = st.text_area("Paste your Markdown here:", height=240)
cleaned_text = st.session_state.get("cleaned_text", "")

col1, col2 = st.columns(2)
with col1:
    if st.button("🧽 Clean"):
        st.session_state.cleaned_text = clean_text(input_text)
        st.experimental_rerun()

with col2:
    if st.button("📋 Copy"):
        if st.session_state.get("cleaned_text"):
            pyperclip.copy(st.session_state.cleaned_text)
            st.success("✅ Cleaned Markdown copied to clipboard")
        else:
            st.warning("No cleaned text available to copy yet.")

# --- Output ---
if st.session_state.get("cleaned_text"):
    cleaned = st.session_state.cleaned_text
    st.text_area("Cleaned Output", cleaned, height=240)
    st.markdown("---")
    st.subheader("🔍 Markdown Preview")
    markdown(cleaned)
else:
    st.info("Paste your text and click **Clean** to start.")
