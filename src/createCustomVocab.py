import argparse
import re
import sys

# custom vocab dictionaly
new_vocab = []

# Vocab path
## input Vocab path
MecapVocab_path = "rsc/my_conf/hangul_vocab.txt"
EnglishVocab_path = "rsc/my_conf/ices_eng_vocab_1000.txt"

## output Vocab path
CustomVocab_path = "rsc/my_conf/ices_custom_vocab_v2.txt"

## 입력 text가 한글인지 아닌지 판단.
def isHangul(text):
    if text[:2] == "##": text = text[2:]
    #Check the Python Version
    pyVer3 =  sys.version_info >= (3, 0)

    if pyVer3 : # for Ver 3 or later
        encText = text
    else: # for Ver 2.x
        if type(text) is not unicode:
            encText = text.decode('utf-8')
        else:
            encText = text

    hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', encText))
    return hanCount > 0


def add_korean():
    # 전체 글에서 추출한 vocab dictionaly
    f = open(MecapVocab_path, 'r')
    lines = f.readlines()
    print("Total Mecab Vocab size : ", len(lines))
    f.close()

    count = 0
    for i in lines:
        if isHangul(i[:-1]):
            new_vocab.append(i)
            count += 1
    
    print("Number of Hangul vocab : {}".format(count))
    print("Current new_vocab size : {} (한글단어 추가)".format(len(new_vocab)))
    
    
def add_english():
    f = open(EnglishVocab_path, 'r')
    eng_lines = f.readlines()
    print("Total English Vocab size : ", len(eng_lines))
    f.close()
    
    count = 0
    for i in eng_lines[5:]:
        new_vocab.append(i)
        count += 1
        
    print("Number of english vocab : {}".format(len(eng_lines[5:])))
    print("Current new_vocab size : {} (영어 추가)".format(len(new_vocab)))
    
    
def add_seperater():
    new_vocab.insert(0,'[MASK]\n')
    new_vocab.insert(0,'[SEP]\n')
    new_vocab.insert(0,'[CLS]\n')
    new_vocab.insert(0,'[UNK]\n')
    new_vocab.insert(0,'[PAD]\n')
    
    print("Number of seperater : 5")
    print("Current new_vocab size : {} (Seperater 추가)".format(len(new_vocab)))
    
def add_number():
    count = 0
    for i in range(10):
        new_vocab.append(str(i)+'\n')
        new_vocab.append("##{}\n".format(i))
        count += 2
        
    print("Number of type of number : {}".format(count))
    print("Current new_vocab size : {} (숫자 추가)".format(len(new_vocab)))
    

def add_special_char():
    used_Special_Char = "+-/*÷=×±∓∘∙∩∪≅∀√%∄∃θπσ≠<>≤≥≡∼≈≢∝≪≫∈∋∉⊂⊃⊆⊇⋈∑∫∏∞x().,%#{}"
    count = 0
    for c in used_Special_Char:
        new_vocab.append(c+'\n')
        new_vocab.append("##{}\n".format(c))
        count+=2
        
    print("Number of Special Characters : {}".format(count))
    print("Current new_vocab size : {} (숫자 추가)".format(len(new_vocab)))
    
    
def merge_all_vocab():
    f = open(CustomVocab_path, 'w')
    f.write("".join(new_vocab))
    f.close()
    
def compare_shap_word():
    # ##붙은것과 안붙은 것 갯수 비교
    f = open(CustomVocab_path, 'r')
    test = f.readlines()
    f.close()
    count = 0
    count2 = 0
    
    for i in test[5:]:
        if i[:2] == '##': count += 1
        else: count2 += 1
    print("## 붙은 것 : ", count)
    print("## 안 붙은 것 : ", count2)
    
def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process korean spelling check')

    parser.add_argument('Mecab', help='Path of file Mecab vocab')
    parser.add_argument('english_only', help='Path of file english vocab')
    parser.add_argument('--custom', default="rsc/my_conf/ices_custom_vocab_v2.txt", help='Path of file final custom vocab')
    parser.add_argument('--check_word', type=str2bool, default="true", help='check ##word and word')
    
    args = parser.parse_args()
    
    ## input Vocab path
    MecapVocab_path = args.Mecab
    EnglishVocab_path = args.english_only

    ## output Vocab path
    CustomVocab_path = args.custom
    
    add_korean()
    add_english()
    add_seperater()
    add_number()
    add_special_char()
    merge_all_vocab()
    
    if (args.check_word):
        compare_shap_word()