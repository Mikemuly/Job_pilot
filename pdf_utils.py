from fpdf import FPDF

REPLACEMENTS = {
    "\u2011": "-", "\u2010": "-", "\u2013": "-", "\u2014": "-",
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u202f": " ", "\u00a0": " ",
}


def clean(text: str) -> str:
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    return text.encode("latin-1", "replace").decode("latin-1")


def letter_to_pdf(text: str, name: str = "", email: str = "") -> bytes:
    pdf = FPDF()
    pdf.add_page()

    if name:
        pdf.set_font("Times", style="B", size=14)
        pdf.cell(0, 8, clean(name), new_x="LMARGIN", new_y="NEXT")
    if email:
        pdf.set_font("Times", size=11)
        pdf.cell(0, 6, clean(email), new_x="LMARGIN", new_y="NEXT")
    if name or email:
        pdf.ln(8)

    pdf.set_font("Times", size=12)
    pdf.multi_cell(0, 7, clean(text), new_x="LMARGIN", new_y="NEXT")
    return bytes(pdf.output())