import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns       # seaborn

from collections import Counter

import re

'''
    데이터의 클래스 분포를 확인하고 PIL.Image로 확인
'''
def check_classes(data_dir: str,
                  target_column: str) -> None:

    FILE_NAME = data_dir.split('/')[-1]
    df = pd.read_csv(data_dir)
    targets = df[target_column].value_counts()

    ax = sns.countplot(y='target', data=df, order=targets.index)

    for p in ax.patches:
        width = p.get_width()
        ax.text(width + 500, p.get_y() + p.get_height() /
                2., int(width), ha='center', size=10)
    ax.set_xlim(-5, 11000)

    plt.savefig(f'./classes_{FILE_NAME[:-4]}.png')


def check_data_length(data_dir: str,
                      text_column: str) -> None:

    FILE_NAME = data_dir.split('/')[-1]
    df = pd.read_csv(data_dir)
    texts = df[text_column].values

    texts_length = list(map(len, texts))
    s = pd.Series(texts_length)
    s.describe()

    
    data = Counter(texts_length).most_common()
    data_x, data_y = [x[0] for x in data], [x[1] for x in data]

    plt.bar(data_x, data_y)
    plt.savefig(f'./length_{FILE_NAME[:-4]}.png')

def check_duplicate(data_dir: str,
                    text_column: str) -> pd.Series:

    df = pd.read_csv(data_dir)
    texts = df[text_column]

    texts.duplicated(keep=False)
    dup_texts = df[texts.duplicated(keep=False)]

    return dup_texts

def check_special_words(data_dir: str,
                    text_column: str) -> None:
    FILE_NAME = data_dir.split('/')[-1]
    df = pd.read_csv(data_dir)
    texts = df[text_column].values

    # 한자 정보 확인
    ptn = '[一-龥]'
    hanja_texts = [(text != re.sub(pattern=ptn, repl='', string=text)) for text in texts]
    df[hanja_texts].to_csv(f"hanja-{FILE_NAME[:-4]}", index=False)

    # 일본어 정보 확인
    ptn = '[[ぁ-ゔ]+|[ァ-ヴー]+[々〆〤]]'
    japanese_texts = [(text != re.sub(pattern=ptn, repl='', string=text)) for text in texts]
    df[japanese_texts].to_csv(f"japanese-{FILE_NAME[:-4]}", index=False)

    # 특수문자 정보 확인
    ptn = '[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>.`\'…》]'
    specialtoken_texts = [(text != re.sub(pattern=ptn, repl='', string=text)) for text in texts]
    df[specialtoken_texts].to_csv(f"specialtoken_{FILE_NAME[:-4]}", index=False)
