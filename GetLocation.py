# https://note.com/uranus_xii_jp/n/n859fc74f6c82　を修正して使用
# イメージデータの位置情報を取得しCSV出力
import os
import glob
from PIL import Image
import PIL.ExifTags as ExifTags
import csv


def get_location_data(fname):
    # 画像ファイルの EXIF タグから GPS の緯度経度を返す
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
    location_data = ''
    latitude = ''
    longitude = ''
    if 'GPSInfo' in exif:
        # EXIF情報から 位置情報を取得
        gps_tags = exif['GPSInfo']
        # 位置情報を辞書に格納
        gps = {
            ExifTags.GPSTAGS.get(t, t): gps_tags[t]
            for t in gps_tags
        }

        # 位置情報がある場合は取得して変換処理
        is_lat = 'GPSLatitude' in gps
        is_lat_ref = 'GPSLatitudeRef' in gps
        is_lon = 'GPSLongitude' in gps
        is_lon_ref = 'GPSLongitudeRef' in gps

        if is_lat and is_lat_ref and is_lon and is_lon_ref:
            # 緯度情報を取得
            lat = gps['GPSLatitude']
            lat_ref = gps['GPSLatitudeRef']
            # 北緯の場合プラス、南緯の場合マイナスを設定
            if lat_ref == 'N':
                lat_sign = 1.0
            elif lat_ref == 'S':
                lat_sign = -1.0
            else:
                lat_sign = 0
            # 緯度情報を取得
            lon = gps['GPSLongitude']
            lon_ref = gps['GPSLongitudeRef']
            # 東経の場合プラス、西経の場合マイナスを設定
            if lon_ref == 'E':
                lon_sign = 1.0
            elif lon_ref == 'W':
                lon_sign = -1.0
            else:
                lon_sign = 0

            # 緯度または経度の値が不正な場合の処理
            if lat_sign == 0 or lon_sign == 0:
                location_data_error = 'Location data error'
                print(location_data_error + fname)
                return location_data_error
            else:
                # 度分秒を十進経緯度 に変換する
                latitude = lat_sign * lat[0] + lat[1] / 60 + lat[2] / 3600
                longitude = lon_sign * lon[0] + lon[1] / 60 + lon[2] / 3600
                # カンマ区切りの文字列に変換
                location_data = str(latitude) + ', ' + str(longitude)
    else:
        location_data = 'No data'

    return location_data, latitude, longitude


if __name__ == '__main__':
    # CSV作成用配列
    export_data = []
    export_data.append(['File name', 'Location data', 'Latitude', 'Longitude'])
    # Imagesディレクトリにあるファイルの取得
    files = glob.glob('./Images/*.jpg')

    for file in files:
        # 写真の位置情報を取得
        location = get_location_data(file)
        # 配列にファイル名と位置データを追加　File name, Location data, Latitude, Longitude
        export_data.append([os.path.basename(file), location[0], location[1], location[2]])

    # CSVファイル生成
    with open('./LocationData.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(export_data)

    print('Process Done!')
