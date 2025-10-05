import re
import streamlit as st

st.set_page_config(page_title="Coala Markdown Cleaner", layout="wide")

# --- Logo and title ---
st.image("coala.png", width=120)
st.title("🧹 Coala Markdown Cleaner")

# --- Clipboard JS helpers ---
copy_script = """
<script>
async function copyText() {
  const text = document.querySelector('textarea[aria-label="Cleaned Output"]').value;
  await navigator.clipboard.writeText(text);
  alert("✅ Cleaned text copied to clipboard!");
}
</script>
"""

paste_script = """
<script>
async function pasteText() {
  const text = await navigator.clipboard.readText();
  const streamlitInput = window.parent.document.querySelector('textarea[aria-label="Paste your Markdown here:"]');
  streamlitInput.value = text;
  streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
}
</script>
"""

st.markdown(copy_script, unsafe_allow_html=True)
st.markdown(paste_script, unsafe_allow_html=True)


# --- Cleaning logic ---
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
    text = re.sub(r'^(#+)[ \t]+', r'\\1 ', text, flags=re.MULTILINE)

    lines = []
    for line in text.splitlines():
        if line.strip().startswith("#"):
            line = re.sub(r"[ \\t\\u00A0]+", " ", line)
        lines.append(line)
    text = "\\n".join(lines)

    def bold_table_headers(md: str) -> str:
        lines = md.splitlines()
        out = []
        for i in range(len(lines)):
            line = lines[i]
            if line.strip().startswith("|") and i + 1 < len(lines) and re.match(r'^\\s*\\|[-: ]+\\|', lines[i + 1]):
                cols = [c.strip() for c in line.strip().strip('|').split('|')]
                bolded = "| " + " | ".join([f"**{c}**" if c else "" for c in cols]) + " |"
                out.append(bolded)
            else:
                out.append(line)
        return "\\n".join(out)

    return bold_table_headers(text).strip()


# --- Input area and buttons ---
st.markdown(
    """
    <div style="display:flex; gap:10px; margin-bottom:10px;">
      <button onclick="pasteText()">📋 Paste from clipboard</button>
      <button onclick="copyText()">🧽 Clean and copy to clipboard</button>
    </div>
    """,
    unsafe_allow_html=True,
)

input_text = st.text_area("Paste your Markdown here:", height=250, key="input_text")

# Clean immediately or when user presses Clean
if input_text.strip():
    cleaned = clean_text(input_text)

    # Show cleaned text
    st.text_area("Cleaned Output", cleaned, height=250)

    # --- WYSIWYG Markdown Preview ---
    st.markdown("---")
    st.subheader("🔍 Markdown Preview")
    st.markdown(cleaned, unsafe_allow_html=True)
else:
    st.info("Paste or type your Markdown text above.")
