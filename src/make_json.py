import json
import pandas as pd
from collections import OrderedDict
import re
import argparse

def QA_make_json(QA_file_path, Paper_file_path):
    
    a = pd.read_csv(QA_file_path)
    b = pd.read_csv(Paper_file_path)
    print(a)
    paper_id = list(a['논문제어번호'].drop_duplicates())

    paper = OrderedDict()
    err = 0
    data = []
    for i in range(len(paper_id)):
        #print(i)
        paragraphs = []
        Q_A = a[a.논문제어번호==paper_id[i]]
        doc = b[b.LIST_SEQ==paper_id[i]]['PAPER_FULL_TXT'].values[0]
        if re.search('<p><h1>', doc):
            p_list = re.split('</p>|</h1>', doc)
        else:
            p_list = re.split('</p>', doc)
        t_end = doc[27:].index('<')  # title의 종료 index

        for j in range(len(Q_A)):
            p_index = Q_A.iloc[j]['응답의 단락 위치'] # 응답의 단락 index
            try:
                p_start = p_list[p_index].index('<p>')
                context = p_list[p_index][p_start+3:]
                p_start = re.search('\w', context).start()
                context = context[p_start:]
            except:
                p_start = re.search('<p([^>]+)>', p_list[p_index]).end()
                context = p_list[p_index][p_start:]


            context = re.sub('&middot;', '·', context)
            context = re.sub('&nbsp;', '\xa0', context)
            context = re.sub('&\D+?;', ' ', context)
            context = re.sub('(<([^>]+)>)', '', context).replace('\n', ' ')


            start = Q_A.iloc[j]['응답의 시작 index'] # 응답의 시작 index
            end = Q_A.iloc[j]['응답의 종료 index']   # 응답의 끝 index
            answer = context[start:end+1]
            text_answer = Q_A.iloc[j]['응답'].replace('\r\n', ' ')



            if  Q_A.iloc[j]['응답'].replace('\r\n', ' ') not in answer:
                err += 1
                #print('논문번호:', i)
                #print('질문번호: ', j)

            #print(context[start:end+1])
            #print(Q_A.iloc[j]['응답'].replace('\r\n', ' '))

            qas = {
                "answers" : [
                    {
                        "text" : Q_A.iloc[j]['응답'].replace('\r\n', ' '),
                        "answer_start" : int(start),
                        "answer_end" : int(end)
                    }
                ],
                "id" : paper_id[i]+'-'+str(j),
                "question" : Q_A.iloc[j]['질문'],
            }
            paragraph = {
                'qas': [qas],
                'context': context
            }
            paragraphs.append(paragraph)


        paper_data = {
            "paragraphs" : paragraphs,
            "title" : doc[27:27+t_end]
        }
        data.append(paper_data)

    paper['version'] = 'ICES_test'
    paper['data'] = data
    print(err)
    
    # make json file
    with open('./QA_test.json', 'w', encoding='utf-8') as makefile:
        json.dump(paper, makefile, ensure_ascii=False, indent="\t")

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='make QA json dataset')

    parser.add_argument('--input_Paper_path', help='input Paper CSV file path')
    parser.add_argument('--input_QA_path', help='input QA CSV file path')
    args = parser.parse_args()
    
    QA_make_json(QA_file_path = args.input_QA_path, Paper_file_path = args.input_Paper_path)