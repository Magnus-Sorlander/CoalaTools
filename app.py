import re
import pyperclip
import streamlit as st
from markdown import markdown as md_to_html
from streamlit.components.v1 import html as st_html

st.set_page_config(page_title="Coala Markdown Cleaner", layout="wide")

# ---------- Header ----------
st.image("coala.png", width=120)
st.title("🧹 Coala Markdown Cleaner")

# ---------- Cleaner ----------
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

    lines = []
    for line in text.splitlines():
        if line.strip().startswith("#"):
            line = re.sub(r"[ \t\u00A0]+", " ", line)
        lines.append(line)
    text = "\n".join(lines)

    # Bold first row in tables (safe)
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

# ---------- Layout ----------
input_text = st.text_area("Paste your Markdown here:", height=220)
if "cleaned_text" not in st.session_state:
    st.session_state.cleaned_text = ""

col1, col2 = st.columns(2)
with col1:
    if st.button("🧽 Clean"):
        st.session_state.cleaned_text = clean_text(input_text)
with col2:
    if st.button("📋 Copy"):
        if st.session_state.cleaned_text:
            try:
                pyperclip.copy(st.session_state.cleaned_text)
                st.success("✅ Copied cleaned Markdown to clipboard")
            except Exception:
                st.warning("⚠️ Clipboard copy not supported here. Copy manually below.")
        else:
            st.warning("Nothing to copy yet.")

# ---------- Output ----------
if st.session_state.cleaned_text:
    cleaned = st.session_state.cleaned_text
    st.text_area("Cleaned Output", cleaned, height=240)

    st.markdown("---")
    st.subheader("🔍 Markdown Preview")

    # Use full GFM renderer for accurate preview
    html_body = md_to_html(
        cleaned,
        extensions=["tables", "sane_lists", "nl2br"]
    )

    st_html(
        f"""
        <style>
        body, .md-preview {{ font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Inter,Arial,sans-serif; }}
        table {{ border-collapse: collapse; width: 100%; margin: 8px 0; }}
        th, td {{ border: 1px solid #ccc; padding: 6px 8px; vertical-align: top; }}
        th {{ background: #f6f8fa; font-weight: 600; }}
        </style>
        <div class="md-preview">{html_body}</div>
        """,
        height=550,
        scrolling=True,
    )
else:
    st.info("Paste text and click **Clean** to begin.")
