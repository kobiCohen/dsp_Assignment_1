import PyPDF2
from setting import pdf_default_name, download_pdf_dic


def pdf_to_txt(pdf_name):
    pdf_path = '{0}/{1}'.format(download_pdf_dic, pdf_default_name)
    txt_path = '{0}/{1}'
    pdf_txt = None
    # rb == open in binary mode
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        page_obj = pdf_reader.getPage(0)
        pdf_txt = page_obj.extractText()

    with open(txt_path, 'w+') as txt_file:
        txt_file.write(pdf_txt)

