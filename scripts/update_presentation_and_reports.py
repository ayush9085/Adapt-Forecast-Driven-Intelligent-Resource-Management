import os
import pptx
import subprocess

def update_pptx():
    template_path = "/Users/ayush9085/.gemini/antigravity/brain/0a826adc-34e8-4f09-a627-953a94f9c6fb/.user_uploaded/media_1795797762594_d71fc693.pptx"
    out_desktop = "/Users/ayush9085/Desktop/Adapt_OS_PBL_Presentation.pptx"
    out_docs = "docs/Adapt_OS_PBL_Presentation.pptx"

    prs = pptx.Presentation(template_path)
    replaced_count = 0

    for slide_idx, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        if "590025211" in run.text:
                            run.text = run.text.replace("590025211", "590025443")
                            replaced_count += 1
                            print(f"[✓] Replaced SAP ID in Slide {slide_idx+1}: {run.text.strip()}")

    prs.save(out_desktop)
    prs.save(out_docs)
    print(f"[✓] Successfully saved PPTX to:\n  - {out_desktop}\n  - {out_docs} (Replaced occurrences: {replaced_count})")

def update_report_files():
    files_to_update = [
        "scripts/build_pbl_report.py",
        "scripts/build_professional_thesis.py",
        "docs/ADAPT_PBL_REPORT.md",
        "docs/ADAPT_THESIS_REPORT.md",
        "docs/ADAPT_PBL_REPORT.html",
        "docs/ADAPT_THESIS_REPORT.html"
    ]

    for file_path in files_to_update:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "590025211" in content:
                new_content = content.replace("590025211", "590025443")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"[✓] Updated SAP ID to 590025443 in {file_path}")

if __name__ == "__main__":
    update_pptx()
    update_report_files()
