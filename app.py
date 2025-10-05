import re
import pyperclip
import streamlit as st

st.set_page_config(page_title="Coala Markdown Cleaner", layout="wide")

# ---------- Header ----------
st.image("coala.png", width=120)
st.title("🧹 Coala Markdown Cleaner")

# ---------- Helper: Cleaning logic ----------
def clean_text(text: str) -> str:
    # Remove Word cruft
    text = re.sub(r"<span[^>]*>", "", text)
    text = re.sub(r"</span>", "", text)
    text = re.sub(r"mso-[^:;]+:[^;\"']+;?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"font-[^:;]+:[^;\"']+;?", "", text, flags=re.IGNORECASE)
    text = re.sub(r' style="[^"]*"', "", text)
    text = text.replace("", "- ").replace("–", "- ")

    # Remove table control codes like @cols=2 etc.
    text = re.sub(r"@cols=\d+(:@rows=\d+)?[:：]?", "", text)
    text = re.sub(r"@rows=\d+[:：]?", "", text)

    # Normalize heading spacing
    text = re.sub(r'^(#+)[ \t]+', r'\1 ', text, flags=re.MULTILINE)
    lines = []
    for line in text.splitlines():
        if line.strip().startswith("#"):
            line = re.sub(r"[ \t\u00A0]+", " ", line)
        lines.append(line)
    text = "\n".join(lines)

    # Bold table headers
    def bold_table_headers(md_in: str) -> str:
        lines = md_in.splitlines()
        out = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.strip().startswith("|") and i + 1 < len(lines):
                nxt = lines[i + 1]
                if re.match(r'^\s*\|[-: ]+\|', nxt):
                    cols = [c.strip() for c in line.strip().strip("|").split("|")]
                    bolded = "| " + " | ".join([f"**{c}**" if c else "" for c in cols]) + " |"
                    out.append(bolded)
                    out.append(nxt)
                    i += 2
                    continue
            out.append(line)
            i += 1
        return "\n".join(out)

    text = bold_table_headers(text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# ---------- UI ----------
input_text = st.text_area("Paste your Markdown here:", height=220)

col1, col2 = st.columns(2)
cleaned = st.session_state.get("cleaned_text", "")

with col1:
    if st.button("🧽 Clean"):
        st.session_state.cleaned_text = clean_text(input_text)
        st.experimental_rerun()

with col2:
    if st.button("📋 Copy"):
        if st.session_state.get("cleaned_text"):
            pyperclip.copy(st.session_state.cleaned_text)
            st.success("✅ Copied cleaned Markdown to clipboard")
        else:
            st.warning("No cleaned text available yet.")

# ---------- Output ----------
if st.session_state.get("cleaned_text"):
    cleaned = st.session_state.cleaned_text
    st.text_area("Cleaned Output", cleaned, height=220)

    st.markdown("---")
    st.subheader("🔍 Markdown Preview")

    # Simple CSS fix for table borders in built-in Markdown renderer
    st.markdown("""
        <style>
        table {border-collapse: collapse; width: 100%; margin: 8px 0;}
        th, td {border: 1px solid #ccc; padding: 6px 8px; text-align: left;}
        th {background: #f6f8fa;}
        </style>
    """, unsafe_allow_html=True)
    st.markdown(cleaned, unsafe_allow_html=True)
else:
    st.info("Paste text and click **Clean** to begin.")
