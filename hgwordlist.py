from  hgbasic import get_backword_string

from hgchartype import get_keyword_type_num__scripts
from hgchartype import HGGetKeywordList
from hgchartype import get_scripts
from hgchartype import get_script_list

def GetKeywordList_File(filename, encoding='utf-8', PrintTextFlag = False):
    # old: GetWordTok_File
    KeywordList = []

    if filename.is_file():
        if filename.exists():pass
        else: return KeywordList
    else:
        print("file not found: %s" %filename)
        return KeywordList

    file = open(filename, 'r', encoding=encoding)

    while True:
        line = file.readline()
        if not line: break

        if(PrintTextFlag == True): print(line)
        
        word_tok = HGGetKeywordList(line)
        if(word_tok != None): KeywordList.extend(word_tok)
    file.close()
    return KeywordList


def PrintWordList(WordList, FilterLen = 0, FilterCharType = None, OneLine=False, PrintIndex=False, BackwardFlag=False):
    if(WordList == None): return
    
    wordlist_len = len(WordList)
    FilterCnt = 0
    for i in range(0, wordlist_len):
        Word = WordList[i]
        wordlen = len(Word)
    
        # filter
        if(FilterLen > 0):
            if(FilterLen != wordlen):
                continue
        if(FilterCharType != None):
            WordCharType = get_scripts(Word)
            if(len(FilterCharType) == 1):
                if(FilterCharType != WordCharType):
                    continue
            #else:
            #    if(FilterCharType == 'keyword'):
            #        if(get_keyword_type_num__scripts(WordCharType) >= 1)
            #        continue
        FilterCnt += 1
        
        if(OneLine == True):
            pass
        else:
            if(FilterCnt == 1):
                print("[", end='')
            elif(FilterCnt > 1):
                print(", ", end='')
            print("'", end='')

        if(PrintIndex == True):
            print('%i: ' %FilterCnt, end='')

        #
        if(BackwardFlag == True):
            backword = get_backword_string(Word)
            print(backword, end='')
        else:
            print(Word, end='')

        #        
        if(OneLine == True):
            print('')
        else:
            print("'", end='')

    if(OneLine == False):
        if(wordlist_len > 0):
            if(FilterCnt > 0):
                print("]", end='')
    print("")
    

def GetWordDictList_WordList(WordList, EraseNonKeyword=False):
    WordDictList = [];
    if(WordList == None): return WordDictList
    WordList_Sort = sorted(WordList)
    #PrintWordList(WordList_Sort, PrintIndex=True)
    #PrintWordList(WordList_Sort, OneLine=True, PrintIndex=True)
    #print ('')

    #==============================================
    ## WordItem = {
    ##     'word': '', 
    ##     'freq':0, 
    ##     'len': 0, 
    ##     'script_num':0
    ## }
    #==============================================

    PreWord = None
    for word in WordList_Sort:
        #
        if(EraseNonKeyword == True):
            char_type_string = get_scripts(word)            
            if(get_keyword_type_num__scripts(char_type_string) <= 0):
                continue
        #
        addflag = False
        if(PreWord == None):
            addflag = True
        else:
            if(PreWord['word'] == word):
                PreWord['freq'] += 1
            else:
                addflag = True
        if(addflag == True):
            string_char_type_list = get_script_list(word)
            #print('string_char_type_list: ', string_char_type_list)
            wordlen = len(word)
            WordItem = {'word': word, 'freq':1, 'len': wordlen, 'script_num':len(string_char_type_list)}
            WordDictList.append(WordItem)
            PreWord = WordItem
        
    return WordDictList


def GetWordDictList_String(string, EraseNonKeyword=False):
    WordDictList = []
    if(string == None): return WordDictList

    #KeywordList = string.split()
    KeywordList = HGGetKeywordList(string)
    #print (KeywordList)

    WordDictList = GetWordDictList_WordList(KeywordList, EraseNonKeyword)
    #print(WordDictList)

    return WordDictList


def GetWordDictList_File(filename, encoding='utf-8', PrintTextFlag = False, EraseNonKeyword=False):
    KeywordList = GetKeywordList_File(filename, encoding, PrintTextFlag)
    WordDictList = GetWordDictList_WordList(KeywordList, EraseNonKeyword)
    return WordDictList


def GetWordDictItem_String(WordDictItem, OneLine = False, PrintingIndex = -1, BackwardFlag = False, SimpleFormat=False):
    WordDictItem_String = ''

    if(WordDictItem == None): WordDictItem_String

    # {'word': '터부일내…위추강', 'freq': 1, 'len': 8, 'script_num':WordCharType}
    # 1: {'word': '터부일내…위추강', 'freq': 1, 'len': 8, 'script_num':WordCharType}

    disp_word = WordDictItem['word']
    if(BackwardFlag == True):
        disp_word = get_backword_string(WordDictItem['word'])

    #
    if(SimpleFormat == True):
        if(PrintingIndex > -1):
            print('%i:\t' %PrintingIndex, end='')

        WordDictItem_String += disp_word
        WordDictItem_String += "\t("
        WordDictItem_String += str(WordDictItem['freq'])
        WordDictItem_String += ")"
    else:
        if(PrintingIndex > -1):
            print('%i: ' %PrintingIndex, end='')

        #
        WordDictItem_String += "{"
    
        #
        WordDictItem_String += "'word': '"
        WordDictItem_String += disp_word
        WordDictItem_String += "'"
    
        #
        WordDictItem_String += ", 'freq': "
        WordDictItem_String += str(WordDictItem['freq'])
    
        #
        WordDictItem_String += ", 'len': "
        WordDictItem_String += str(WordDictItem['len'])

        #
        WordDictItem_String += ", 'script_num': "
        WordDictItem_String += str(WordDictItem['script_num'])

        #
        WordDictItem_String += "}"

    return WordDictItem_String

def PrintWordDictList(WordDictList, FilterLen = 0, FilterCharType = None, FilterFreq = 0, OneLine=False, PrintIndex=False, BackwardFlag=False, SimpleFormat=False):
    if(WordDictList == None): return
    
    WordDictList_len = len(WordDictList)
    FilterCnt = 0
    for i in range(0, WordDictList_len):
        WordDictItem = WordDictList[i]
        #WordLen = WordDictItem['len']
        WordLen = len(WordDictItem['word'])
    
        # filter
        if(FilterLen > 0):
            if(FilterLen != WordLen):
                continue
        if(FilterCharType != None):
            WordCharType = get_scripts(WordDictItem)
            if(len(FilterCharType) == 1):
                if(FilterCharType != WordCharType):
                    continue
            #else:
            #    if(FilterCharType == 'keyword'):
            #        if(get_keyword_type_num__scripts(WordCharType) >= 1)
            #        continue
        if(FilterFreq > 0): # 빈도 필터
            if(FilterFreq != WordDictItem['freq']):
                continue

        ###            
        FilterCnt += 1
        
        if(OneLine == True):
            pass
        else:
            if(FilterCnt == 1):
                print("[", end='')
            elif(FilterCnt > 1):
                print(", ", end='')

        PrintingIndex = -1
        if(PrintIndex == True):
            PrintingIndex = FilterCnt

        #
        #print(WordDictItem, end='')
        WordDictItem_String = GetWordDictItem_String(WordDictItem, OneLine, PrintingIndex, BackwardFlag, SimpleFormat)
        print(WordDictItem_String, end='')

        if(OneLine == True):
            print("")

    if(OneLine == False):
        if(WordDictList_len > 0):
            if(FilterCnt > 0):
                print("]", end='')
    print("")


def GetWordDictList_TotalFreq(WordDictList, FilterLen = 0, FilterCharType = None, FilterFreq = 0):
    TotalFreq = 0

    if(WordDictList == None): return TotalFreq
    
    WordDictList_len = len(WordDictList)
    FilterCnt = 0
    for i in range(0, WordDictList_len):
        WordItem = WordDictList[i]
        #WordItemLen = len(WordItem['word'])
    
        ### filter
        if(FilterLen > 0):
            if(FilterLen != WordItem['len']):
                continue
        
        if(FilterCharType != None):
            WordCharType = get_scripts(WordItem['word'])
            if(len(FilterCharType) == 1):
                if(FilterCharType != WordCharType):
                    continue
            #else:
            #    if(FilterCharType == 'keyword'):
            #        if(get_keyword_type_num__scripts(WordCharType) >= 1)
            #        continue

        if(FilterFreq > 0): # 빈도 필터
            if(FilterFreq != WordItem['freq']):
                continue

        ###            
        FilterCnt += 1
        TotalFreq += WordItem['freq']
    
    return TotalFreq

def GetWordDictList_FreqListInfo(WordDictList, FilterLen = 0, FilterCharType = None):
    #
    FreqListInfo = []
    
    TotalFreq = 0

    if(WordDictList == None): 
        return FreqListInfo

    # sort by freq
    WordDictList_Sort = WordDictList.copy();
    WordDictList_Sort.sort(key = lambda wd: (wd['freq'], wd['word'])) # by freq low, abc

    WordDictList_len = len(WordDictList_Sort)
    FilterCnt = 0
    FreqList = []
    FreqListItem = None
    for i in range(0, WordDictList_len):
        WordItem = WordDictList_Sort[i]
        #WordItemLen = len(WordItem['word'])
    
        ### filter
        if(FilterLen > 0):
            if(FilterLen != WordItem['len']):
                continue
        
        if(FilterCharType != None):
            WordCharType = get_scripts(WordItem['word'])
            if(len(FilterCharType) == 1):
                if(FilterCharType != WordCharType):
                    continue
            #else:
            #    if(FilterCharType == 'keyword'):
            #        if(get_keyword_type_num__scripts(WordCharType) >= 1)
            #        continue

        ###            
        FilterCnt += 1
        TotalFreq += WordItem['freq']

        AddFalg = False
        if(FreqListItem == None):
            AddFalg = True
        else:
            if(FreqListItem['freq'] == WordItem['freq']):
                FreqListItem['count'] += 1
            else:
                AddFalg = True

        if(AddFalg == True):
             FreqListItem = {'freq': WordItem['freq'], 'count': 1}
             FreqList.append(FreqListItem)

    FreqListInfo = {'TotalFreq':TotalFreq, 'ListSum':FilterCnt, 'FilterLen':FilterLen, 'List':FreqList}
    return FreqListInfo


def PrintWordDictListInfo(WordDictListInfo):
    if(WordDictListInfo == None): return
    print ('List Num:', len(WordDictListInfo['List']), 'List Sum:', WordDictListInfo['ListSum'])
    print ('Total Freq:', WordDictListInfo['TotalFreq'])
    if WordDictListInfo.get('FilterLen') != None:
        print ('Len Filter:', WordDictListInfo['FilterLen'])
    if WordDictListInfo.get('FilterFreq') != None:
        print ('Freq Filter:', WordDictListInfo['FilterFreq'])
    print (*WordDictListInfo['List'],sep='\n')

def GetWordDictList_LenListInfo(WordDictList, FilterFreq = 0, FilterCharType = None):
    #
    LenListInfo = []
    
    TotalFreq = 0

    if(WordDictList == None): 
        return LenListInfo

    # sort by freq
    WordDictList_Sort = WordDictList.copy();
    WordDictList_Sort.sort(key = lambda wd: (wd['len'], wd['word'])) # by len low, abc

    WordDictList_len = len(WordDictList_Sort)
    FilterCnt = 0
    LenList = []
    LenListItem = None
    for i in range(0, WordDictList_len):
        WordItem = WordDictList_Sort[i]
        #WordItemLen = len(WordItem['word'])
    
        ### filter
        #if(FilterLen > 0):
        #    if(FilterLen != WordItem['len']):
        #        continue
        
        if(FilterCharType != None):
            WordCharType = get_scripts(WordItem['word'])
            if(len(FilterCharType) == 1):
                if(FilterCharType != WordCharType):
                    continue
            #else:
            #    if(FilterCharType == 'keyword'):
            #        if(get_keyword_type_num__scripts(WordCharType) >= 1)
            #        continue

        if(FilterFreq > 0):
            if(FilterFreq != WordItem['freq']):
                continue

        ###            
        FilterCnt += 1
        TotalFreq += WordItem['freq']

        AddFalg = False
        if(LenListItem == None):
            AddFalg = True
        else:
            if(LenListItem['len'] == WordItem['len']):
                LenListItem['count'] += 1
            else:
                AddFalg = True

        if(AddFalg == True):
             LenListItem = {'len': WordItem['len'], 'count': 1}
             LenList.append(LenListItem)

    LenListInfo = {'TotalFreq':TotalFreq, 'ListSum':FilterCnt, 'FilterFreq':FilterFreq, 'List':LenList}
    return LenListInfo


def GetBackWordDictList__DictList(WordDictList, FilterLen = 0, FilterCharType = None, FilterFreq = 0):
    #
    BackWordDictList = []
    #
    if(WordDictList == None): return
    
    WordDictList_len = len(WordDictList)
    FilterCnt = 0
    for i in range(0, WordDictList_len):
        WordItem = WordDictList[i]
        #WordItemLen = WordItem['len']
        WordItemLen = len(WordItem['word'])
    
        # filter
        if(FilterLen > 0):
            if(FilterLen != WordItemLen):
                continue
        if(FilterCharType != None):
            WordCharType = get_scripts(WordItem)
            if(len(FilterCharType) == 1):
                if(FilterCharType != WordCharType):
                    continue
            #else:
            #    if(FilterCharType == 'keyword'):
            #        if(get_keyword_type_num__scripts(WordCharType) >= 1)
            #        continue
        if(FilterFreq > 0): # 빈도 필터
            if(FilterFreq != WordItem['freq']):
                continue

        ###            
        FilterCnt += 1

        BackWordItem  = dict(WordItem)
        BackWordItem['word'] = get_backword_string(WordItem['word'])
        BackWordDictList.append(BackWordItem)
    
    return BackWordDictList
        
def GetBackWordDictList__List(WordList, FilterLen = 0, FilterCharType = None, FilterFreq = 0):
    BackWordDictList = []
    WordDictList = GetWordDictList_WordList(WordList)
    if(len(WordDictList) > 0):
        BackWordDictList = GetBackWordDictList__DictList(WordDictList, FilterLen, FilterCharType, FilterFreq)
    return BackWordDictList


def SortWordDictList_CharTypeNum(WordList, EraseNonKeyword=False):
    WordDictList = []
    if(WordList == None): return WordDictList

    WordDictList = GetWordDictList_WordList(WordList, EraseNonKeyword)
    #print(WordDictList)
    WordDictList_Sort = WordDictList.copy();
    WordDictList_Sort.sort(key = lambda wd: wd['script_num']) # by char-type-num
    #PrintWordDictList(WordDictList_Sort, OneLine=True, PrintIndex=True, SimpleFormat=True)
    return WordDictList_Sort

