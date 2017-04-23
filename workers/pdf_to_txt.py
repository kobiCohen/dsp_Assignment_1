import PyPDF2
from setting import download_pdf_dic, convert_pdf_dic


def pdf_to_txt(pdf_name):
    pdf_path = '{0}/{1}.pdf'.format(download_pdf_dic, pdf_name)
    txt_path = '{0}/{1}.txt'.format(convert_pdf_dic, pdf_name)
    pdf_txt = None
    # rb == open in binary mode
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        page_obj = pdf_reader.getPage(0)
        pdf_txt = page_obj.extractText()

    with open(txt_path, 'w+') as txt_file:
        txt_file.write(pdf_txt)

