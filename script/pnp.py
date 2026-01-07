import subprocess
import os
from pypdf import PdfWriter

def generate_nandeck_pdf(nandeck_exe_path, nde_script_path, output_pdf_name):
    command = [
        nandeck_exe_path,
        nde_script_path,
        "/createpdf",
        f"/output={output_pdf_name}",
        "/nopdfdiag"
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        raise

def convert_odt_to_pdf(odt_path, output_dir, soffice_path):
    command = [
        soffice_path,
        "--headless",
        "--convert-to", "pdf",
        "--outdir", output_dir,
        odt_path
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        base_name = os.path.splitext(os.path.basename(odt_path))[0]
        output_pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
        print(f"Conversion successful: {output_pdf_path}")
        return output_pdf_path
    except subprocess.CalledProcessError as e:
        print("Error converting ODT:")
        print(e.stderr)
        return None

def merge_pdfs(output_filename, input_files):
    merger = PdfWriter()

    for pdf in input_files:
        if os.path.exists(pdf):
            merger.append(pdf)

    merger.write(output_filename)
    merger.close()

if __name__ == "__main__":
    nandeck_exe = r"D:\bin\board-game\nandeck\nandeck.exe"
    soffice_exe = r"D:\bin\office\LibreOffice\program\soffice.exe"

    disney_deck = "./print-and-play/disney/villains.nde"
    disney_deck_pdf = "./export/disney-deck.pdf"
    disney_rules_odt = './print-and-play/disney/disney-rules.odt'
    disney_pnp_pdf = "./export/Disney Villainous - Solo Mode - Waltina.pdf"

    os.makedirs('./export',exist_ok=True)

    disney_rules_pdf = convert_odt_to_pdf(disney_rules_odt,'./export')
    generate_nandeck_pdf(nandeck_exe, disney_deck, disney_deck_pdf)
    files_to_merge = [disney_rules_pdf, disney_deck_pdf]
    merge_pdfs(disney_pnp_pdf, files_to_merge)