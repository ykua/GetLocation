# イメージデータの位置情報を取得しCSV出力
# ©︎Yuichi Kageyama

import os
import glob
from PIL import Image
import PIL.ExifTags as ExifTags
import csv
from tqdm import tqdm


def get_location_data(file_name):
    im = Image.open(file_name)
    # EXIF情報を辞書型で取得
    exif = {
        ExifTags.TAGS[k]: v
        for k, v in im._getexif().items()
        if k in ExifTags.TAGS
    }
    # GPS情報を取得
    if 'GPSInfo' in exif:
        gps_tags = exif['GPSInfo']
        gps = {
            ExifTags.GPSTAGS.get(t, t): gps_tags[t]
            for t in gps_tags
        }

        # 緯度経度情報を取得
        def conv_deg(v):
            # 分数を度に変換
            d = float(v[0])
            m = float(v[1])
            s = float(v[2])
            return d + (m / 60.0) + (s / 3600.0)

        latitude = conv_deg(gps["GPSLatitude"])
        lat_ref = gps["GPSLatitudeRef"]
        # 北緯ではない場合はマイナス値
        if lat_ref != "N":
            latitude = 0 - latitude
        longitude = conv_deg(gps["GPSLongitude"])
        lon_ref = gps["GPSLongitudeRef"]
        # 東経ではない場合はマイナス値
        if lon_ref != "E":
            longitude = 0 - longitude
        location_data = str(latitude) + ', ' + str(longitude)

        return location_data, latitude, longitude

    else:
        location_data = 'No Data'
        return location_data, None, None


if __name__ == '__main__':
    print('Get location information from photo files.' + '\n')
    # CSV作成用配列
    export_data = [['File name', 'Location data', 'Latitude', 'Longitude']]
    # 指定ディレクトリにあるファイルの取得
    files_path = './Images/'
    files = glob.glob(files_path + '*.jpg')

    for file in tqdm(files, desc='Photo files: '):
        # 写真の位置情報を取得
        location = get_location_data(file)
        # 配列にファイル名と位置データを追加　File name, Location data, Latitude, Longitude
        export_data.append([os.path.basename(file), location[0], location[1], location[2]])

    # CSVファイル生成
    with open('./LocationData.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(export_data)

    print('\n' + 'Process Done!')
