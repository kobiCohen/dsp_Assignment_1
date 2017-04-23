from setting import download_pdf_dic, convert_pdf_dic
from subprocess import check_call


def pdf_to_html(pdf_name):
    pdf_path = '{0}/{1}.pdf'.format(download_pdf_dic, pdf_name)
    html_path = '{0}/{1}'.format(convert_pdf_dic, pdf_name)
    tar_name = '{0}.tar.gz'.format(convert_pdf_dic, pdf_name)
    tar_path = '{0}/{1}'.format(convert_pdf_dic, tar_name)
    check_call(['pdftohtml', '-l 1', pdf_path, html_path])
    check_call(['tar', '-cvf', tar_path, '{0}/*'.format(convert_pdf_dic)])
    return tar_path



