#/home/nozaki/yt-dlp/pythonにある
#python save.py --img_sum 000 --type 000

import project_processing as pp
import argparse

# コマンドライン引数のパーサーを作成
parser = argparse.ArgumentParser(description="Process images and videos.")
parser.add_argument("--img_sum", type=int, help="Number of images to process")
parser.add_argument("--type", type=str, help="Type of processing")

def main():
    # コマンドライン引数をパース
    args = parser.parse_args()
    # 引数を取得
    img_sum = args.img_sum
    type = args.type
    pp_instance_den = pp.project_processing()

    #これから以下のフォルダに画像を保存する
    base_path = "/home/nozaki/yt-dlp/"
    video_path = base_path + f"concat/{type}_con.webm"
    #ランダム画像の保存先
    out_path = base_path + f"img/{type}/before/"
    pp_instance_den.get_random_frame(type, video_path, out_path, img_sum)
    #クロップ用の変数
    input_path = out_path
    output_path = base_path + f"img/{type}/"
    pp_instance_den.cropping(type, input_path, output_path)
    print(f"{output_path} に保存")

if __name__ == "__main__":
    main()
