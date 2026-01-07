import subprocess
import os
from pypdf import PdfWriter
from PIL import Image

def convert_odt_to_pdf(soffice_exe_path, odt_path, output_dir):
    print(f"Generating rules pdf from {odt_path}")
    command = [
        soffice_exe_path,
        "--headless",
        "--convert-to", "pdf",
        "--outdir", output_dir,
        odt_path
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        base_name = os.path.splitext(os.path.basename(odt_path))[0]
        output_pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
        print(f"Success")
        return output_pdf_path
    except subprocess.CalledProcessError as e:
        print("Failure")
        print(e.stderr)
        return None

def convert_image_to_pdf(image_path, output_path):
    print(f"Convert image to pdf {image_path}")
    img = Image.open(image_path)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.save(output_path, "PDF", resolution=300.0)
    print("Success")

def generate_nandeck_pdf(nandeck_exe_path, nde_script_path, output_pdf_name):
    print(f"Generating nandeck {nde_script_path}")
    command = [
        nandeck_exe_path,
        nde_script_path,
        "/createpdf",
        f"/output={output_pdf_name}",
        "/nopdfdiag"
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Success")
    except subprocess.CalledProcessError as e:
        print(f"Failure")
        print(e.stderr)
        raise

def merge_pdfs(output_filename, input_files):
    print(f"Merging PDFs to {output_filename}")
    merger = PdfWriter()
    for pdf in input_files:
        if os.path.exists(pdf):
            merger.append(pdf)
    merger.write(output_filename)
    merger.close()
    print("Success")

if __name__ == "__main__":
    nandeck_exe = r"D:\bin\board-game\nandeck\nandeck.exe"
    soffice_exe = r"D:\bin\office\LibreOffice\program\soffice.exe"

    disney_pnp_pdf = "./export/Disney Villainous - Solo Mode - Waltina.pdf"
    if os.path.exists(disney_pnp_pdf):
        os.remove(disney_pnp_pdf)
    disney_rules_odt = './print-and-play/disney/disney-rules.odt'
    disney_board_image = './print-and-play/disney/image/Automa Track.png'
    disney_board_pdf = './export/disney-board.pdf'
    disney_deck = "./print-and-play/disney/villains.nde"
    disney_deck_pdf = os.path.abspath("./export/disney-deck.pdf")

    os.makedirs('./export',exist_ok=True)

    disney_rules_pdf = convert_odt_to_pdf(soffice_exe,disney_rules_odt,'./export')
    convert_image_to_pdf(disney_board_image,disney_board_pdf)
    generate_nandeck_pdf(nandeck_exe, disney_deck, disney_deck_pdf)
    files_to_merge = [disney_rules_pdf, disney_board_pdf, disney_deck_pdf]
    merge_pdfs(disney_pnp_pdf, files_to_merge)
    os.remove(disney_rules_pdf)
    os.remove(disney_board_pdf)
    os.remove(disney_deck_pdf)