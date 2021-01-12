import pandas as pd
import numpy as np
import argparse

PAPER_PATH = './Paper_text_dataset'
QnA_PATH = ""

def extract_paper_number(QnA_PATH):
    QnA_data_v2 = pd.read_csv(QnA_PATH)

    LIST_SEQs_duplicated = QnA_data_v2['논문제어번호']
    LIST_SEQs_duplicated = LIST_SEQs_duplicated.values
    LIST_SEQs = np.unique(LIST_SEQs_duplicated)
    LIST_SEQs = np.sort(LIST_SEQs)
    print('QnA 데이터의 논문 개수 : {}'.format(len(LIST_SEQs)))
    
    return LIST_SEQs

def paper_text_to_csv(LIST_SEQs):
    data = []

    for LIST_SEQ in LIST_SEQs:
        f = open(PAPER_PATH + "/{}.txt".format(LIST_SEQ), 'r', encoding='utf-8')
        p_text = f.read()
        data.append([LIST_SEQ, p_text])
        f.close()

    df = pd.DataFrame(data, columns=['LIST_SEQ', 'PAPER_FULL_TXT'])

    df.to_csv("paper.csv", mode='w')
    
    print("Complete Creating paper.csv")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='make QA json dataset')

    parser.add_argument('--input_Paper_path', help='input Paper CSV file path')
    parser.add_argument('--input_QA_path', help='input QA CSV file path')
    args = parser.parse_args()
    
    PAPER_PATH = args.input_Paper_path
    QnA_PATH = args.input_QA_path
    
    paper_text_to_csv(extract_paper_number(QnA_PATH))