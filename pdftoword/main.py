from aip import AipOcr
from docx import Document
import pdfkit
import fitz
import os

""" 你的 APPID AK SK """
APP_ID = '24021012'
API_KEY = 'T8oEPkt9eLbl09i6hTCeGMER'
SECRET_KEY = 'Z7UuZfCE9E49IVbpDbpbHnEDbeb1aLlr'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

pdfpath = 'E:\PYWorkSpaces\pdftoword'
pdfname = '广发智慧园区技术需求书202107060843.pdf'


image_path = pdfpath + os.sep + "images"
if not os.path.exists(image_path):
    os.mkdir(image_path)
image_path = image_path + os.sep + "JPEG"
if not os.path.exists(image_path):
    os.mkdir(image_path)
image_path = image_path + os.sep + pdfname[:-4]
if not os.path.exists(image_path):
    os.mkdir(image_path)


# 将每页pdf转为png格式图片
def pdf_image():
    pdf = fitz.open(pdfpath + os.sep + pdfname)
    for pg in range(0, pdf.pageCount):
        # 获得每一页的对象
        page = pdf[pg]
        trans = fitz.Matrix(1.0, 1.0).preRotate(0)
        # 获得每一页的流对象
        pm = page.getPixmap(matrix=trans, alpha=False)
        # 保存图片
        pm.writeImage(image_path + os.sep + pdfname[:-4] + '_' + '{:0>3d}.jpeg'.format(pg + 1))
    page_range = range(pdf.pageCount)
    pdf.close()
    return page_range


# 将图片中的文字转换为字符串
def read_png_str(page_range):
    # 读取本地图片的函数
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    allPngStr = []
    image_list = []
    for page_num in range(0,page_range):
        # 读取本地图片
        if os.path.exists(image_path + os.sep + r'{}_{}.jpeg'.format(pdfname[:-4], '%03d' % (page_num + 1))):
            image = get_file_content(image_path + os.sep + r'{}_{}.jpeg'.format(pdfname[:-4], '%03d' % (page_num + 1)))
            print(image)
            image_list.append(image)

    # 新建一个AipOcr
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    """ 如果有可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"

    for image in image_list:
        # 通用文字识别,得到的是一个dict
        pngjson = client.basicGeneral(image, options)
        pngstr = ''
        for x in pngjson['words_result']:
            pngstr = pngstr + x['words'] + '\n'
        print('正在调用百度接口：第{}个，共{}个'.format(len(allPngStr), len(image_list)))
        allPngStr.append(pngstr)
    return allPngStr


def str2word(allPngStr):
    document = Document()
    for i in allPngStr:
        document.add_paragraph(
            i, style='List Bullet'
        )
        if not os.path.exists(pdfpath + os.sep + "docs"):
            os.mkdir(pdfpath + os.sep + "docs")
        document.save(pdfpath + os.sep + "docs" + os.sep + pdfname[:-4] + '.docx')
    print('处理完成')


range_count = pdf_image()
allPngStr = read_png_str(60)
str2word(allPngStr)