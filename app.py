import re
import json
import streamlit as st
import markdown as md
from streamlit.components.v1 import html as st_html

st.set_page_config(page_title="Coala Markdown Cleaner", layout="wide")

# ---------- Styling ----------
st.markdown("""
<style>
.toolbar { display:flex; gap:12px; margin: 6px 0 12px 0; }
.md-preview { font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,Arial,sans-serif; line-height:1.45 }
.md-preview table { border-collapse: collapse; width: 100%; margin: 8px 0; }
.md-preview th, .md-preview td { border: 1px solid #ddd; padding: 6px; vertical-align: top; }
.md-preview th { background: #f6f8fa; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.image("coala.png", width=120)
st.title("🧹 Coala Markdown Cleaner")

# ---------- Clipboard helpers (client-side) ----------
st.markdown("""
<script>
async function pasteFromClipboard() {
  try {
    const text = await navigator.clipboard.readText();
    const ta = window.parent.document.querySelector('textarea[aria-label="Paste your Markdown here:"]');
    if (ta) { ta.value = text; ta.dispatchEvent(new Event('input', {bubbles:true})); }
  } catch (e) { alert("Clipboard paste not permitted by the browser."); }
}
async function copyCleaned() {
  const ta = document.querySelector('textarea[aria-label="Cleaned Output"]');
  if (!ta || !ta.value) { alert("Nothing to copy yet."); return; }
  try { await navigator.clipboard.writeText(ta.value); alert("✅ Cleaned Markdown copied!"); }
  catch (e) { alert("Clipboard copy not permitted by the browser."); }
}
</script>
""", unsafe_allow_html=True)

# ---------- Cleaning logic ----------
def clean_text(text: str) -> str:
    # Remove Word/HTML cruft (keep Markdown)
    text = re.sub(r"<span[^>]*>", "", text)
    text = re.sub(r"</span>", "", text)
    text = re.sub(r"mso-[^:;]+:[^;\"']+;?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"font-[^:;]+:[^;\"']+;?", "", text, flags=re.IGNORECASE)
    text = re.sub(r' style="[^"]*"', "", text)

    # Collapse tabs/spaces (preserves newlines)
    text = re.sub(r"[ \t]+", " ", text)

    # Word bullets → Markdown bullets
    text = text.replace("", "- ").replace("–", "- ")

    # Remove table control codes like @cols=2, @rows=3
    text = re.sub(r"@cols=\d+(:@rows=\d+)?[:：]?", "", text)
    text = re.sub(r"@rows=\d+[:：]?", "", text)

    # Normalize Markdown headings spacing
    text = re.sub(r"^(#+)[ \t]+", r"\1 ", text, flags=re.MULTILINE)

    # Collapse multiple spaces/tabs/nbsp inside heading lines
    lines = []
    for line in text.splitlines():
        if line.strip().startswith("#"):
            line = re.sub(r"[ \t\u00A0]+", " ", line)
        lines.append(line)
    text = "\n".join(lines)

    # Bold table headers (first row before the --- separator row)
    def bold_table_headers(md_in: str) -> str:
        L = md_in.splitlines()
        out = []
        i = 0
        while i < len(L):
            line = L[i]
            if line.strip().startswith("|") and (i + 1) < len(L):
                sep = L[i + 1]
                if re.match(r'^\s*\|(?:\s*:?-+:?\s*\|)+\s*$', sep):
                    cols = [c.strip() for c in line.strip().strip("|").split("|")]
                    bolded = "| " + " | ".join([f"**{c}**" if c else "" for c in cols]) + " |"
                    out.append(bolded)
                    i += 1  # keep the separator row untouched
                    out.append(sep)
                    i += 1
                    continue
            out.append(line)
            i += 1
        return "\n".join(out)

    text = bold_table_headers(text)

    # Ensure a blank line before any table for robust rendering
    def ensure_blank_before_tables(md_in: str) -> str:
        L = md_in.splitlines()
        out = []
        for i, line in enumerate(L):
            if line.strip().startswith("|") and (i == 0 or L[i-1].strip() != ""):
                out.append("")  # insert blank line
            out.append(line)
        return "\n".join(out)

    text = ensure_blank_before_tables(text)

    return text.strip()

# ---------- Toolbar (top) ----------
st.markdown(
    '<div class="toolbar">'
    '<button onclick="pasteFromClipboard()">📋 Paste from clipboard</button>'
    '<button onclick="copyCleaned()">🧽 Clean and copy to clipboard</button>'
    '</div>',
    unsafe_allow_html=True
)

# ---------- Input ----------
raw = st.text_area("Paste your Markdown here:", height=220, key="input_md")

# ---------- Process & Output ----------
if raw.strip():
    cleaned = clean_text(raw)

    # The “code view” of cleaned MD
    st.text_area("Cleaned Output", cleaned, height=220)

    # Robust WYSIWYG Preview using Python-Markdown w/ tables
    html_body = md.markdown(
        cleaned,
        extensions=["tables", "sane_lists", "nl2br", "toc", "smarty", "admonition"]
    )
    st.markdown("—")
    st.subheader("🔍 Markdown Preview")
    st_html(f'<div class="md-preview">{html_body}</div>', height=500, scrolling=True)

else:
    st.info("Paste or type your Markdown text above.")
