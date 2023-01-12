import requests,json,os,datetime
import urllib.request
from PIL import Image
import os

def combine_imgs_pdf(folder_path, pdf_file_path):
    """
    合成文件夹下的所有图片为pdf
    Args:
        folder_path (str): 源文件夹
        pdf_file_path (str): 输出路径
    """
    print('图片合成pdf文件中...')
    files = os.listdir(folder_path)
    png_files = []
    sources = []
    for file in files:
        if 'png' in file or 'jpg' in file:
            png_files.append(folder_path + '\\' + file)
    png_files.sort()
    output = Image.open(png_files[0])
    png_files.pop(0)
    for file in png_files:
        png_file = Image.open(file)
        sources.append(png_file)
    output.save(pdf_file_path, "pdf", save_all=True, append_images=sources)
    if os.path.exists(pdf_file_path):
        for png_file in png_files:
            if png_file.endswith('.png'):
               os.remove(png_file)

def gUrl(reportID):
    pngUrl=[]
    pageIndex = 1

    while True:
        # 获取img链接
        payload=reportID+"&"+"index="+str(pageIndex)
        headers={'Content-Type':'application/x-www-form-urlencoded'}
        response=requests.request("POST",APIurl,headers=headers,data=payload)
        jsonRes = json.loads(response.text) # str数据转为json(dict)
        resUrl = jsonRes["data"]["url"]
        imgUrl = rootWeb+resUrl

        # 验证img链接是否有效
        try:
            imgRes = urllib.request.urlopen(imgUrl)
            print("INFO",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"正在获取...第%d页url"%(pageIndex))
        except Exception as err:
            print(err)
            break
        pageIndex += 1 # 循环获取报告全部页数
        pngUrl.append(imgUrl) # 保存img链接数据
    return pngUrl

def downloadPNG(imgUrl,i):
    # 创建png保存路径
    saveDir="./png"
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
        print("INFO","创建文件夹")
    imgRes = urllib.request.urlopen(imgUrl)
    print("正在下载",i,imgUrl)
    with open(saveDir+"/%s.png"%(str(10+i)), 'wb') as f:
        f.write(imgRes.read()) # 保存图片

if __name__ == "__main__":
    rootWeb = "https://kd.nsfc.gov.cn"
    reportURL = "https://kd.nsfc.gov.cn/finalDetails?id=c0c594edb4d7bd226e3bc670f5b47a91"   # 第一处修改，替换为结题报告网址
    APIurl = "https://kd.nsfc.gov.cn/api/baseQuery/completeProjectReport"  # 默认值
    try:
        reportID = reportURL.split("?")[-1]
    except:
        print("ERROR", "请检查报告url是否有id关键字")
    # print(reportID)

    res = gUrl(reportID)
    for ind,resU in enumerate(res):
        downloadPNG(resU,ind+1)
    folder = r"\temp\png"                                                        # 第二处修改，替换为保存路径
    pdfFile = r"\temp\png\面向冲突情境意识的安全驾驶时序性特征识别研究.pdf"             # 第三处修改，替换为结题报告名称
    combine_imgs_pdf(folder, pdfFile)

