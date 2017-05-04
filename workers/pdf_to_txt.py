from subprocess import check_call
from global_setting.setting import download_pdf_dic, convert_pdf_dic


def pdf_to_txt(pdf_name):
    """
    convert pdf to txt file
    :param pdf_name: string -> the loc of the pdf 
    :return: string -> the loc you can find the txt file
    """
    pdf_path = '{0}/{1}.pdf'.format(download_pdf_dic, pdf_name)
    txt_path = '{0}/{1}.txt'.format(convert_pdf_dic, pdf_name)
    check_call('pdftotext -l 1 {0} {1}'.format(pdf_path, txt_path), shell=True)
    return txt_path



