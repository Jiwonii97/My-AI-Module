
'''
    hanspell : 맞춤법 검사
'''
import pandas as pd  # pandas
from hanspell import spell_checker  # git+https://github.com/jungin500/py-hanspell
import time

'''
    backtranslation : 역번역
'''
import urllib.request
import urllib
from googletrans import Translator  # googletrans==3.1.0a0

from tqdm import tqdm
from typing import List

TRANSLATED = 'translated'

'''
    Hanspell : 맞춤법 검사 전처리 모듈
'''
def myhanspell(data_dir : str,
               text_column : str,
               times : int = 100,
               replace : bool = False) -> None:
    
    FILE_NAME = data_dir.split('/')[-1]
    df = pd.read_csv(data_dir)

    texts = df[text_column].values.tolist()

    translated : List = []

    for idx, text in tqdm(enumerate(texts), total=len(texts)):
        try:
            if len(text) > 500:  # 500자 제한
                translated.append(text)
                continue
            
            # 맞춤법 검사 진행 ('&'의 경우, hanspell의 오류가 있어 전처리 진행)
            worked_text = spell_checker.check(text.replace('&',"")).checked
            
            # 전처리 진행한 데이터 추가
            translated.append(worked_text)
            
            # API를 통한 작업이 진행되는 만큼 통신을 원활하게 하기 위해 지연 진행
            if not idx % times:
                time.sleep(5)
            
        except:
            # 만약 오류가 발생한다면 오류 출력 후, 원본 데이터 추가
            translated.append(text)

    if replace:
        df[text_column] = translated
    else:
        df[TRANSLATED] = translated

    df.to_csv(f"hanspell-{FILE_NAME}", index=False)

'''
    Backtranslation : 역번역 전처리 모듈
'''
def google_trans(text: str,
                 src: str,
                 tgt: str) -> str:
    
    translator = Translator()
    target = translator.translate(text, src=src, dest=tgt)
    result = translator.translate(target.text, src=tgt, dest=src)
    
    return result.text

def mybacktranslation(data_dir : str,
                      text_column : str,
                      times : int = 100,
                      language : str = "english",
                      replace : bool = False) -> None:
    FILE_NAME = data_dir.split('/')[-1]
    languages = {"english":"en", "japanese":'ja'}

    df = pd.read_csv(data_dir)

    # 번역을 위해 제대로 언어 정보가 들어왔는지 확인
    assert language not in languages.keys(), '잘못된 언어 정보입니다.'

    texts = df[text_column].values.tolist()

    translated : List = []

    for idx, text in tqdm(enumerate(texts), total=len(texts)):
        try:
            trans = google_trans(text, "ko", language)
            translated.append(trans)
            
            # API를 통한 작업이 진행되는 만큼 통신을 원활하게 하기 위해 지연 진행
            if not idx % times:
                time.sleep(5)
            
        except:
            # 만약 오류가 발생한다면 오류 출력 후, 원본 데이터 추가
            translated.append(text)

    if replace:
        df[text_column] = translated
    else:
        df[TRANSLATED] = translated

    df.to_csv(f"hanspell-{FILE_NAME}", index=False)