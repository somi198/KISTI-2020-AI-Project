from hanspell import spell_checker
import argparse

# INPUT PATH
SPELL_UNCHECKED_FILE_PATH = ""
# OUTPUT PATH
SPELL_CHECKED_FILE_PATH = ""


def string_cutting():
    unchecked_file = open(SPELL_UNCHECKED_FILE_PATH, 'r')

    lines = unchecked_file.readlines()

    temp_str = ""
    ready_list = []

    # 띄어쓰기가 심각하게 되어있지않는 데이터(500자 이상)
    max_iter=1000
    debug = 0
    flag = True
    fuckData = []

    # 맞춤범 검사를 하기 위해 길이가 500이하 문자열로 자르기
    for i, line in enumerate(lines):
        if i % 100 == 0: print("Processing line num : ", i)
        while(len(line) > 500):
            debug += 1
            if debug > max_iter:
                print("Funking Data!! please check index : {}".format(i))
                fuckData.append(i)
                break

            end = line[:500].rfind(" ")
            temp_str = line[:end]
            ready_list.append(temp_str)
            line = line[end:]

        ready_list.append(line)
        debug = 0

    print("Finish preprocess for spelling check (Cut string under 500 length)")
    print("Total preprocessed list length : {}".format(len(ready_list)))

    unchecked_file.close()
    
    return ready_list


def spelling_check(ready_list):
    # 맞춤법 검사 진행
    # 맞춤법 검사 false 경우 검사되지 않은 문자열 입력(error Message 출력)

    spellchecked_li = [] # 검사된 문자열을 담는 리스트
    # error 방지 parametr
    error = False
    error_index = []

    for i, line in enumerate(ready_list):
        try:
            result = spell_checker.check(line)
        except Exception as e:
            error = True
            error_index.append(i)
            print(e)
            print("Just insert no checked string")
            print("### Error Check This ###\n",line)
            spellchecked_li.append(line)
            continue
        print("processing index num : {}, processing time : {}".format(i, round(result.as_dict()['time'],3)), end='\r',flush=True)
        # drop error 발생시 stop
        if result.as_dict()['result'] == False:
            error = True
            error_index.append(i)
            print("DROP ERROR : error index is {}".format(i))
            print("Just insert no checked string")
            print("### Error Check This ###\n",line)
            spellchecked_li.append(line)
            continue
        spellchecked_li.append(result.as_dict()["checked"])

    if error: print("\nPlese check error\nerror index numbers : {}".format("\t".join((map(str, error_index)))))
    else:
        print("\nThere is no error")

    print("Start file writing")
    for i, data in enumerate(spellchecked_li):
        if data == '':
            spellchecked_li[i] = '\n\n'

    checked_list_backup = open("spellchecked_li_backup", 'w')
    checked_list_backup.write(str(checked_list_backup))
    checked_list_backup.close()

    full_text = "".join(spellchecked_li)

    checked_file = open(SPELL_CHECKED_FILE_PATH, 'w')
    checked_file.write(full_text)
    checked_file.close()
    print("Complete task : create spell checked text file : {}".format(SPELL_CHECKED_FILE_PATH))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process korean spelling check')

    parser.add_argument('unchecked_file', help='Path of file unchecked korean spelling')

    parser.add_argument('--checked_file', default='rsc/training_data/final_text_Kospell_check.txt', help='Path of file checked korean spelling')

    args = parser.parse_args()
    
    SPELL_UNCHECKED_FILE_PATH = args.unchecked_file
    SPELL_CHECKED_FILE_PATH = args.checked_file
    
    spelling_check(string_cutting())