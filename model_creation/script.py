import os
from os.path import isfile

import pandas as pd
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def get_directories_in(path='.'):
    directories = []
    files = os.listdir(path)
    for file in files:
        if not isfile(file) and not file.startswith('.'):
            directories.append(f"{path}/{file}")
    return directories


def get_images_in(directory):
    img_list = []
    files = os.listdir(directory)
    for file in files:
        img_list.append(f"{directory}/{file}")
    return img_list


def get_all_image(path='.'):
    directories = get_directories_in(path)
    images = []
    for directory in directories:
        if not isfile(directory):
            images.extend(get_images_in(directory))
        else:
            images.append(directory)
    return images


def convert(value):
    return ord(value)


def put_in_dataframe(data, image):
    name = image
    img = Image.open(name, 'r')
    img = img.resize((28, 28))
    info = name.split('/')[-1].split('_')[0]
    row = [convert(info[0])]
    row.extend(list(img.getdata()))
    img.close()
    return pd.concat([data, pd.DataFrame([row], columns=data.columns)], ignore_index=True)


def build_dataframe(img_path='.'):
    columns = ['0']
    columns.extend([f"0.{x}" for x in range(1, 785)])
    data = pd.DataFrame(columns=columns)
    images = get_all_image(img_path)
    i = 0
    for img in images:
        if i % 32000 == 0:
            print(i)
        data = put_in_dataframe(data, img)
        i += 1
    return data


df1 = build_dataframe("./data/CompleteImages/All data (Compressed)")

df1.to_parquet('data.parquet')

model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=0)
print(accuracy_score)
