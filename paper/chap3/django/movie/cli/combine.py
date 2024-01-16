#ライブラリインポート
import cv2
movie_list=['test1.mp4','test2.mp4']
size=(1000,1000)
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
save = cv2.VideoWriter('concat_movie.mp4',fourcc,fps=20,frameSize=size,isColor=False)


#動画の結合処理
for movie in movie_list:
    rmovie=cv2.VideoCapture(movie)
    nframe=int(rmovie.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in range(nframe):
        ret,frame=rmovie.read()
        frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if ret==True:
            save.write(frame)
save.release()