from setting import download_pdf_dic, convert_pdf_dic
from subprocess import check_call


def pdf_to_png(pdf_name):
    pdf_path = '{0}/{1}.pdf'.format(download_pdf_dic, pdf_name)
    png_path = '{0}/{1}'.format(convert_pdf_dic, pdf_name)
    check_call(['pdftoppm', '-l 1', '-png', pdf_path, png_path])
    return png_path




