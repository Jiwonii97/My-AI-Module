from custom_eda import *
from data_analysis import *

DATA_PATH = ""
TEXT_COLUMN = ""
TARGET_COLUMN = ""
SLEEP_TIME = 100


def main():
    '''
        데이터 분석
    '''
    check_classes(DATA_PATH, TARGET_COLUMN)     # target 데이터의 클래스 분포 확인
    check_data_length(DATA_PATH, TEXT_COLUMN)   # text 데이터의 길이 확인
    check_duplicate(DATA_PATH, TEXT_COLUMN)     # text 데이터의 중복 여부 확인
    check_special_words(DATA_PATH, TEXT_COLUMN) # text 데이터의 특정 단어 유무 확인

    '''
        데이터 전처리
    '''
    myhanspell(DATA_PATH, TEXT_COLUMN)
    mybacktranslation(DATA_PATH, TEXT_COLUMN)

if __name__ == "__main__":
    main()
