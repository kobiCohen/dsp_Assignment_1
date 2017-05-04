from subprocess import check_call
from global_setting.setting import download_pdf_dic, convert_pdf_dic


def pdf_to_html(pdf_name):
    """
    convert pdf to html file
    :param pdf_name: string -> the loc of the pdf 
    :return: string -> the loc you can find the html file
    """
    pdf_path = '{0}/{1}.pdf'.format(download_pdf_dic, pdf_name)
    html_path = '{0}/{1}.html'.format(convert_pdf_dic, pdf_name)
    tar_name = '{0}.tar.gz'.format(pdf_name)
    tar_path = '{0}/{1}'.format(convert_pdf_dic, tar_name)
    check_call('pdftohtml -c -s -noframes -l 1 {0} {1}'.format(pdf_path, html_path), shell=True)
    return tar_path



