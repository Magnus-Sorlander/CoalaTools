import re
import streamlit as st
from markdown import markdown as md_to_html
from streamlit.components.v1 import html as st_html

st.set_page_config(page_title="Coala Markdown Cleaner", layout="wide")

# --- Header and style ---
st.image("coala.png", width=120)
st.title("🧹 Coala Markdown Cleaner")

st.markdown("""
<style>
.toolbar { display:flex; gap:10px; margin: 10px 0; }
.md-preview table { border-collapse: collapse; width: 100%; margin-top: 10px; }
.md-preview th, .md-preview td { border: 1px solid #ccc; padding: 6px; }
.md-preview th { background-color: #f7f7f7; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# --- JS clipboard buttons ---
st.markdown("""
<script>
async function pasteFromClipboard() {
  try {
    const text = await navigator.clipboard.readText();
    const input = window.parent.document.querySelector('textarea[aria-label="Paste your Markdown here:"]');
    if (input) {
      input.value = text;
      input.dispatchEvent(new Event('input', { bubbles: true }));
    }
  } catch (e) { alert("Clipboard paste not allowed by browser."); }
}
async function copyCleaned() {
  const ta = document.querySelector('textarea[aria-label="Cleaned Output"]');
  if (!ta || !ta.value) { alert("Nothing to copy."); return; }
  try { await navigator.clipboard.writeText(ta.value); alert("✅ Copied cleaned Markdown!"); }
  catch (e) { alert("Clipboard copy not allowed by browser."); }
}
</script>
""", unsafe_allow_html=True)

# --- Markdown cleaner ---
def clean_text(text: str) -> str:
    # Remove Word cruft
    text = re.sub(r"<span[^>]*>", "", text)
    text = re.sub(r"</span>", "", text)
    text = re.sub(r"mso-[^:;]+:[^;\"']+;?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"font-[^:;]+:[^;\"']+;?", "", text, flags=re.IGNORECASE)
    text = re.sub(r' style="[^"]*"', "", text)

    # Replace Word bullets etc.
    text = text.replace("", "- ").replace("–", "- ")

    # Remove table control codes like @cols=2 etc.
    text = re.sub(r"@cols=\d+(:@rows=\d+)?[:：]?", "", text)
    text = re.sub(r"@rows=\d+[:：]?", "", text)

    # Normalize spaces in headings
    text = re.sub(r'^(#+)[ \t]+', r'\1 ', text, flags=re.MULTILINE)
    lines = []
    for line in text.splitlines():
        if line.strip().startswith("#"):
            line = re.sub(r"[ \t\u00A0]+", " ", line)
        lines.append(line)
    text = "\n".join(lines)

    # Bold header rows in Markdown tables (keep tables together)
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

    # Ensure single blank line between blocks (but keep tables intact)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()

# --- Toolbar ---
st.markdown("""
<div class="toolbar">
  <button onclick="pasteFromClipboard()">📋 Paste from clipboard</button>
  <button onclick="copyCleaned()">🧽 Clean and copy to clipboard</button>
</div>
""", unsafe_allow_html=True)

# --- Input area ---
input_text = st.text_area("Paste your Markdown here:", height=220)

if input_text.strip():
    cleaned = clean_text(input_text)

    # Show cleaned markdown text
    st.text_area("Cleaned Output", cleaned, height=220)

    # Render Markdown preview properly
    html = md_to_html(cleaned, extensions=["tables", "nl2br", "sane_lists"])
    st.markdown("---")
    st.subheader("🔍 Markdown Preview")
    st_html(f'<div class="md-preview">{html}</div>', height=500, scrolling=True)
else:
    st.info("Paste or type your Markdown text above.")
