from flask import Flask,request,send_file,make_response
import os,json,threading,shutil
from moviepy.editor import *
from md5random import sjs

app = Flask(__name__)

@app.route("/file",methods=['POST'])
def test():

    #获取文件
    files =  request.files
    #合成队列
    videoL = []
    #随机字符串
    dirs = sjs()
    #生成文件夹
    os.mkdir(dirs)
    #保存文件并添加至合成队列
    for file in files.values():
        print(file)
        dst = dirs + "/" + file.name + ".mp4"
        file.save(dst)
        video = VideoFileClip(dirs + "/" + file.name + ".mp4")
        videoL.append(video)

    #拼接视频
    final = concatenate_videoclips(videoL)
    #文件路径
    fileName = dirs + "/" +"{}.mp4".format(sjs())
    #生成视频
    final.to_videofile(fileName)

    #销毁文件夹
    def sc():
        shutil.rmtree(dirs)

    #30秒后销毁文件夹
    timer = threading.Timer(30, sc)
    timer.start()

    # 返回文件路径
    return fileName


@app.route("/getvoi",methods=['GET'])
def getImg():
    #获取文件名
    ss = request.args['name']
    #文件加至返回响应
    response = make_response(
        send_file(ss))

    #删除文件
    def sc():
        os.remove(ss)

    #30秒后删除文件
    timer = threading.Timer(30, sc)
    timer.start()

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8087)