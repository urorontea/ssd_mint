from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import NameForm, URLForm_1, URLForm_2, URLForm_3



import yt_dlp
from yt_dlp.utils import download_range_func

import cv2
import glob
import os
import csv
import subprocess
from DownloadVideoProject.settings import BASE_DIR

# Create your views here.
def download(request):
    return render(request, "DownloadApp/download.html", {})


#フォームのテスト
def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, "DownloadApp/base.html", {"form": form})


def input_urls_1(request):
    count = 0
    form = URLForm_1(request.POST)
    if form.is_valid():
    # フォームが妥当な場合の処理
        type = form.cleaned_data["type"]
        url_1 = form.cleaned_data['url_1']
        start = form.cleaned_data["start_1"]
        end = form.cleaned_data["end_1"]

    # ここでURLを使用して必要な処理を行う
        DLmovie(url_1, type, start, end, count)
        save_info(url_1,type, start, end)
        #count += 1
    else:
        form = URLForm_1()
    return render(request, 'DownloadApp/input_urls_1.html', {'form': form})

def input_urls_2(request):
    count  = 0
    form = URLForm_2(request.POST)
    if form.is_valid():
    # フォームが妥当な場合の処理
        type = form.cleaned_data["type"]
        url_1 = form.cleaned_data['url_1']
        start_1 = form.cleaned_data["start_1"]
        end_1= form.cleaned_data["end_1"]

        url_2 = form.cleaned_data['url_2']
        start_2 = form.cleaned_data["start_2"]
        end_2 = form.cleaned_data["end_2"]

    # ここでURLを使用して必要な処理を行う
        DLmovie(url_1, type, start_1, end_1, count)
        save_info(url_1, type, start_1, end_1)
        count += 1

        DLmovie(url_2, type, start_2, end_2, count)
        save_info(url_2, type, start_2, end_2)
        count += 1

    #サブプロセスを呼び出して保存した動画を連結する。
        ff_concat("filelist.txt", type, f"{type}_con.webm")
        remove_filelist(type)
    else:
        form = URLForm_2()
    return render(request, 'DownloadApp/input_urls_2.html', {'form': form})

def input_urls_3(request):
    count = 0
    form = URLForm_3(request.POST)
    if form.is_valid():
    # フォームが妥当な場合の処理
        type = form.cleaned_data["type"]
        url_1 = form.cleaned_data['url_1']
        start_1 = form.cleaned_data["start_1"]
        end_1= form.cleaned_data["end_1"]

        url_2 = form.cleaned_data['url_2']
        start_2 = form.cleaned_data["start_2"]
        end_2 = form.cleaned_data["end_2"]

        url_3 = form.cleaned_data['url_3']
        start_3 = form.cleaned_data["start_3"]
        end_3 = form.cleaned_data["end_3"]

    # ここでURLを使用して必要な処理を行う
        DLmovie(url_1, type, start_1, end_1, count)
        save_info(url_1, type, start_1, end_1)
        count += 1

        DLmovie(url_2, type, start_2, end_2, count)
        save_info(url_2, type, start_2, end_2)
        count += 1

        DLmovie(url_3, type, start_3, end_3, count)
        save_info(url_3, type, start_3, end_3)
        count += 1

    #サブプロセスを呼び出して保存した動画を連結する。
        ff_concat("filelist.txt", type, f"{type}_con.webm")
        remove_filelist(type)
    else:
        form = URLForm_3()
   
    return render(request, 'DownloadApp/input_urls_3.html', {'form': form})


def DLmovie(url, type, start, end, count):
    ydl_opts = {
            #'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'format' : 'bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]' ,
            'outtmpl': f'DownloadApp/movie/shinkansen/{type}/{type}_{count}.%(ext)s',
            'download_ranges': download_range_func(None, [(start, end)]),
            'force_keyframes_at_cuts': True,
            #'external_downloader': 'ffmpeg',
            #"external_downloader_args": {"ffmpeg_i": ["-ss", str(start), "-to", str(end)]},
        }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = get_file_name_from_path(ydl.prepare_filename(info_dict))
        #保存した動画を連結させるためのfilelist.txtを作成する
        save_filelist(type, filename)
    
def comb_movie(movie_files,out_path):

    # 形式はmp4
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v') 

    # 動画情報の取得
    movie = cv2.VideoCapture(movie_files[0])
    fps = movie.get(cv2.CAP_PROP_FPS)
    height = movie.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = movie.get(cv2.CAP_PROP_FRAME_WIDTH)


    # 出力先のファイルを開く
    out = cv2.VideoWriter(out_path, int(fourcc), fps, (int(width), int(height)))


    for movies in (movie_files):
        print(movies + "/")

        # 動画ファイルの読み込み，引数はビデオファイルのパス
        movie = cv2.VideoCapture(movies)

        # 正常に動画ファイルを読み込めたか確認
        if movie.isOpened(): 
            # read():1コマ分のキャプチャ画像データを読み込む
            ret, frame = movie.read() 
        else:
            ret = False

        while ret:
            # 読み込んだフレームを書き込み
            out.write(frame)
            # 次のフレーム読み込み
            ret, frame = movie.read()
                # 動画ファイルを閉じる

    print("combined!!")

def save_info(url, type, start, end):
    with open(f"DownloadApp/movie/shinkansen/{type}/info.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow((type, url, start, end))

# ファイルパスからファイル名のみを取得する関数
def get_file_name_from_path(file_path):
    return os.path.basename(file_path)

def save_filelist(type, filename):
    with open(f"DownloadApp/movie/shinkansen/{type}/filelist.txt", "a") as f:
        f.write(f"file \'{filename}\'\n")

def remove_filelist(type):
    os.remove(f"DownloadApp/movie/{type}/filelist.txt")
    
#djangoでffmpegコマンドを使用するためにサブプロセスを呼び出しているよ
def ff_concat(filelist, type, moviename):
    #subprocess.call("pwd\n")
    print(f"pwd = {os.getcwd()}\n")
    #TextPath = f"{os.getcwd()}\movie\{type}\{filelist}"
    subprocess.call(f"ffmpeg -f concat -i DownloadApp/movie/shinkansen/{type}/{filelist} -c copy DownloadApp/movie/shinkansen/{type}/{moviename}")

