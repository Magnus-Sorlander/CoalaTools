import re
import streamlit as st

st.set_page_config(page_title="Markdown Cleaner", layout="wide")
st.title("🧹 Markdown Cleaner")

def clean_text(text: str) -> str:
    text = re.sub(r"<span[^>]*>", "", text)
    text = re.sub(r"</span>", "", text)
    text = re.sub(r"mso-[^:;]+:[^;\"']+;?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"font-[^:;]+:[^;\"']+;?", "", text, flags=re.IGNORECASE)
    text = re.sub(r" style=\"[^\"]*\"", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = text.replace("", "- ").replace("–", "- ")
    text = re.sub(r"@cols=\d+(:@rows=\d+)?[:：]?", "", text)
    text = re.sub(r"@rows=\d+[:：]?", "", text)
    text = re.sub(r'^(#+)[ \t]+', r'\1 ', text, flags=re.MULTILINE)
    lines = []
    for line in text.splitlines():
        if line.strip().startswith("#"):
            line = re.sub(r"[ \t\u00A0]+", " ", line)
        lines.append(line)
    text = "\n".join(lines)
    def bold_table_headers(md: str) -> str:
        lines = md.splitlines()
        out = []
        for i in range(len(lines)):
            line = lines[i]
            if line.strip().startswith("|") and i+1 < len(lines) and re.match(r'^\s*\|[-: ]+\|', lines[i+1]):
                cols = [c.strip() for c in line.strip().strip('|').split('|')]
                bolded = "| " + " | ".join([f"**{c}**" if c else "" for c in cols]) + " |"
                out.append(bolded)
            else:
                out.append(line)
        return "\n".join(out)
    return bold_table_headers(text).strip()

input_text = st.text_area("Paste your Markdown here:", height=300)
if st.button("🧽 Clean Markdown"):
    if input_text.strip():
        cleaned = clean_text(input_text)
        st.text_area("✅ Cleaned Output:", cleaned, height=300)
        st.download_button("💾 Download cleaned file", cleaned, "cleaned.md")
    else:
        st.warning("Please paste some text first.")
