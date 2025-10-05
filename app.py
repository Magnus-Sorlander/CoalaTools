import re
import streamlit as st

st.set_page_config(page_title="Coala Markdown Cleaner", layout="wide")

# --- Logo and title ---
st.image("coala.png", width=120)
st.title("🧹 Coala Markdown Cleaner")

# --- JavaScript clipboard helpers ---
copy_script = """
<script>
async function copyText() {
  const text = document.querySelector('textarea[aria-label="Cleaned Output"]').value;
  await navigator.clipboard.writeText(text);
  alert("✅ Cleaned text copied to clipboard!");
}
async function pasteText() {
  const text = await navigator.clipboard.readText();
  const input = window.parent.document.querySelector('textarea[aria-label="Paste your Markdown here:"]');
  if (input) {
    input.value = text;
    input.dispatchEvent(new Event('input', { bubbles: true }));
  }
}
</script>
"""
st.markdown(copy_script, unsafe_allow_html=True)

# --- Cleaner function ---
def clean_text(text: str) -> str:
    # Remove Word cruft
    text = re.sub(r"<span[^>]*>", "", text)
    text = re.sub(r"</span>", "", text)
    text = re.sub(r"mso-[^:;]+:[^;\"']+;?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"font-[^:;]+:[^;\"']+;?", "", text, flags=re.IGNORECASE)
    text = re.sub(r" style=\"[^\"]*\"", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = text.replace("", "- ").replace("–", "- ")

    # Remove table control codes like @cols=2 etc.
    text = re.sub(r"@cols=\d+(:@rows=\d+)?[:：]?", "", text)
    text = re.sub(r"@rows=\d+[:：]?", "", text)

    # Fix heading spacing
    text = re.sub(r'^(#+)[ \t]+', r'\1 ', text, flags=re.MULTILINE)

    # Collapse multiple spaces/tabs in headings
    lines = []
    for line in text.splitlines():
        if line.strip().startswith("#"):
            line = re.sub(r"[ \t\u00A0]+", " ", line)
        lines.append(line)
    text = "\n".join(lines)

    # Bold table headers
    def bold_table_headers(md: str) -> str:
        lines = md.splitlines()
        out = []
        for i in range(len(lines)):
            line = lines[i]
            if line.strip().startswith("|") and i + 1 < len(lines) and re.match(r'^\s*\|[-: ]+\|', lines[i + 1]):
                cols = [c.strip() for c in line.strip().strip('|').split('|')]
                bolded = "| " + " | ".join([f"**{c}**" if c else "" for c in cols]) + " |"
                out.append(bolded)
            else:
                out.append(line)
        return "\n".join(out)

    text = bold_table_headers(text)
    return text.strip()

# --- Toolbar (top buttons) ---
st.markdown(
    """
    <div style="display:flex;gap:10px;margin-bottom:10px;">
      <button onclick="pasteText()">📋 Paste from clipboard</button>
      <button onclick="copyText()">🧽 Clean and copy to clipboard</button>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Input field ---
input_text = st.text_area("Paste your Markdown here:", height=250)

# --- Process ---
if input_text.strip():
    cleaned = clean_text(input_text)
    st.text_area("Cleaned Output", cleaned, height=250)
    st.markdown("---")
    st.subheader("🔍 Markdown Preview")
    st.markdown(cleaned)
else:
    st.info("Paste or type your Markdown text above.")
