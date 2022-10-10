# https://note.com/uranus_xii_jp/n/n859fc74f6c82　を修正して使用
# イメージデータの位置情報を取得しCSV出力
import os
import glob
from PIL import Image
import PIL.ExifTags as ExifTags
import csv


def GetLocationData(fname):
    # 画像ファイルの EXIF タグから GPS の緯度経度を返す
    LocationData = ''
    im = Image.open(fname)
    # EXIF情報を取得
    exif = im._getexif()
    # EXIF情報を辞書に格納する
    exif = {
        ExifTags.TAGS[MyKey]: MyValue
        for MyKey, MyValue in exif.items()
        if MyKey in ExifTags.TAGS
    }
    # EXIF情報 に GPSInfo タグが含まれているときの処理
    if 'GPSInfo' in exif:
        # EXIF情報から GPS情報を取得
        gps_tags = exif['GPSInfo']
        # GPS情報を辞書に格納
        gps = {
            ExifTags.GPSTAGS.get(t, t): gps_tags[t]
            for t in gps_tags
        }
        # 目的のタグがあることを確認した上で処理する
        # 長くなるので、まず有り無し用の変数に入れる
        is_lat = 'GPSLatitude' in gps
        is_lat_ref = 'GPSLatitudeRef' in gps
        is_lon = 'GPSLongitude' in gps
        is_lon_ref = 'GPSLongitudeRef' in gps
        if is_lat and is_lat_ref and is_lon and is_lon_ref:
            # GPS情報から緯度に関する情報を取り出す
            lat = gps['GPSLatitude']
            lat_ref = gps['GPSLatitudeRef']
            # 北緯の場合プラス、南緯の場合マイナスを設定
            if lat_ref == 'N':
                lat_sign = 1.0
            elif lat_ref == 'S':
                lat_sign = -1.0
            # GPS情報から経度に関する情報を取り出す
            lon = gps['GPSLongitude']
            lon_ref = gps['GPSLongitudeRef']
            # 東経の場合プラス、西経の場合マイナスを設定
            if lon_ref == 'E':
                lon_sign = 1.0
            elif lon_ref == 'W':
                lon_sign = -1.0
            # 度分秒 を 十進経緯度 に変換する
            lat_ang0 = lat_sign * lat[0] + lat[1] / 60 + lat[2] / 3600
            lon_ang0 = lon_sign * lon[0] + lon[1] / 60 + lon[2] / 3600
            # コンマ区切りで１つにまとめる
            LocationData = str(lat_ang0) + ', ' + str(lon_ang0)
    return LocationData


if __name__ == '__main__':
    # CSV作成用配列
    ExportData = []
    # Imagesディレクトリにあるファイルの取得
    Files = glob.glob('./Images/*.jpg')
    for File in Files:
        # 写真の位置情報を取得
        Location = GetLocationData(File)
        # 配列にファイル名と位置データを追加
        ExportData.append([os.path.basename(File), Location])

    # CSVファイルの作成
    with open('./LocationData.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(ExportData)

    print('Process Done!')
