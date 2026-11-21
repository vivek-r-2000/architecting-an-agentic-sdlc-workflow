import os
import win32com.client

def compile_pdf():
    docx_path = os.path.abspath(r"C:\Users\vivek\ASE\2019112020_AutoSE_A3\report.docx")
    pdf_path = os.path.abspath(r"C:\Users\vivek\ASE\2019112020_AutoSE_A3\report.pdf")
    
    if not os.path.exists(docx_path):
        print(f"Error: {docx_path} does not exist.")
        return
        
    print(f"Compiling {docx_path} -> {pdf_path} via Word COM...")
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(docx_path)
        # 17 = wdFormatPDF
        doc.SaveAs(pdf_path, FileFormat=17)
        page_count = doc.ComputeStatistics(2) # 2 = wdStatisticPages
        doc.Close()
        print(f"Successfully compiled PDF! Size: {os.path.getsize(pdf_path)} bytes, Pages: {page_count}")
        assert page_count <= 8, f"Warning: PDF exceeds 8 pages ({page_count} pages)!"
        print("Page count strictly complies with <= 8 pages constraint.")
    except Exception as e:
        print(f"Error compiling PDF: {e}")
    finally:
        word.Quit()

if __name__ == "__main__":
    compile_pdf()
