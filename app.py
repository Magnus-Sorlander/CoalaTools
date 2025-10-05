import re
import streamlit as st
import pyperclip

st.set_page_config(page_title="Coala Markdown Cleaner", layout="wide")

# ---------- Header ----------
st.image("coala.png", width=120)
st.title("🧹 Coala Markdown Cleaner")

# ---------- Markdown Cleaner ----------
def clean_text(text: str) -> str:
    text = re.sub(r"<span[^>]*>", "", text)
    text = re.sub(r"</span>", "", text)
    text = re.sub(r"mso-[^:;]+:[^;\"']+;?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"font-[^:;]+:[^;\"']+;?", "", text, flags=re.IGNORECASE)
    text = re.sub(r' style="[^"]*"', "", text)
    text = text.replace("", "- ").replace("–", "- ")
    text = re.sub(r"@cols=\d+(:@rows=\d+)?[:：]?", "", text)
    text = re.sub(r"@rows=\d+[:：]?", "", text)
    text = re.sub(r'^(#+)[ \t]+', r'\1 ', text, flags=re.MULTILINE)

    # Clean headings
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

# ---------- Interface ----------
input_text = st.text_area("Paste your Markdown here:", height=220)

if "cleaned_text" not in st.session_state:
    st.session_state.cleaned_text = ""

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧽 Clean"):
        st.session_state.cleaned_text = clean_text(input_text)

with col2:
    if st.button("📋 Copy"):
        if st.session_state.cleaned_text:
            try:
                pyperclip.copy(st.session_state.cleaned_text)
                st.success("✅ Copied to clipboard")
            except Exception:
                st.warning("⚠️ Clipboard not available in browser — copy manually below.")
        else:
            st.warning("No cleaned text yet.")

with col3:
    if st.session_state.cleaned_text:
        st.download_button(
            label="💾 Download Cleaned File",
            data=st.session_state.cleaned_text,
            file_name="cleaned.md",
            mime="text/markdown",
        )

# ---------- Output ----------
if st.session_state.cleaned_text:
    cleaned = st.session_state.cleaned_text
    st.text_area("Cleaned Markdown", cleaned, height=240)
    st.markdown("---")
    st.subheader("🔍 Markdown Preview (basic Streamlit renderer)")

    # Light table styling for visibility
    st.markdown("""
        <style>
        table {border-collapse: collapse; width: 100%; margin: 8px 0;}
        th, td {border: 1px solid #ccc; padding: 6px 8px; text-align: left;}
        th {background: #f6f8fa;}
        </style>
    """, unsafe_allow_html=True)
    st.markdown(cleaned, unsafe_allow_html=True)
else:
    st.info("Paste text and click **Clean** to start.")
