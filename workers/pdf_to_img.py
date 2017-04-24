from subprocess import check_call

from global_setting.setting import download_pdf_dic, convert_pdf_dic


def pdf_to_png(pdf_name):
    pdf_path = '{0}/{1}.pdf'.format(download_pdf_dic, pdf_name)
    png_path = '{0}/{1}'.format(convert_pdf_dic, pdf_name)
    check_call('pdftoppm -l 1 -png {0} {1}'.format(pdf_path, png_path), shell=True)
    return png_path




