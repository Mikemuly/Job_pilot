from fpdf import FPDF

REPLACEMENTS = {
    "\u2011": "-", "\u2010": "-", "\u2013": "-", "\u2014": "-",
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u202f": " ", "\u00a0": " ",
}

def letter_to_pdf(text: str) -> bytes:
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    text = text.encode("latin-1", "replace").decode("latin-1")
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=12)
    pdf.multi_cell(0,7,text,new_x = "LMARGIN", new_y="NEXT")
    return bytes(pdf.output())