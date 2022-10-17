#-------------------------------
#-------------------------------
import inspect


#-------------------------------
#-------------------------------
__debug_print_on__ = False

#-------------------------------
#-------------------------------
#frame = inspect.currentframe()
# __FILE__ = inspect.currentframe().f_code.co_filename
__LINE__ = fileNo = inspect.currentframe().f_lineno
__FUNCTION__ = inspect.stack()[0][3]

def _func_line_():
  callerframerecord = inspect.stack()[1]    # 0 represents this line
                                            # 1 represents line at caller
  frame = callerframerecord[0]
  info = inspect.getframeinfo(frame)
  #print(info.filename)                      # __FILE__     -> Test.py
  #print(info.function)                      # __FUNCTION__ -> Caller
  #print(info.lineno)                        # __LINE__     -> 13
  print(info.lineno, 'line', 'at', info.function, '[', info.filename, ']')


#-------------------------------
#-------------------------------
__HG_SYL_NUM__ = 11172  # (ord('힣') - ord('가') + 1)
__HG_SYL_LEADING_DEC__ = 44032 # ord('가')
__HG_CHO_NUM__ = 19 # 초성 개수
__HG_JUNG_NUM__ = 21 # 중성 개수
__HG_JONG_NUM__ = 28 # 종성 개수[종성( 27 + 채움(1)]

__HG_JUNG_X_JONG_NUM__ = (__HG_JUNG_NUM__ * __HG_JONG_NUM__) # 중성 개수 x 종성 개수 = 588

#-------------------------------
#-------------------------------
def debug_print_on():
    global __debug_print_on__
    __debug_print_on__ = True

def debug_print_off():
    global __debug_print_on__
    __debug_print_on__ = False

def get_backword_string(str):
    #backword_str = ''
    #hglen = len(str)
    #for i in range(hglen, 0, -1):
    #    backword_str += str[i - 1]
    backword_str = str[::-1]  # slicing 가장 빠르다. 다른 것에 비해 5 ~ 12배 빠름
    return backword_str

def get_char_code_value_string3(char1, decFlag=True, hexFlag=True, sep=' '):
    char_code_value_string = ''
    if(len(char1) != 1):
        print('logic error :', '(len(char1) != 1)', __FUNCTION__, __name__)
        return char_code_value_string
    char_code_value_string = char1
    if(decFlag == True):
        char_code_value_string += sep
        char_code_value_string += str(ord(char1))
    if(hexFlag == True):
        char_code_value_string += sep
        hexchar1 = hexUpper(ord(char1))
        char_code_value_string += hexchar1
    return char_code_value_string

def get_hangul_syllable_index(cho_i, jung_i, jong_i, SyllableFalg=True):
    syllable_index = (-1)
    #print(cho_i, jung_i, jong_i,)

    #
    if((cho_i < 0) or (cho_i >= __HG_CHO_NUM__)): # 초성 범위
        return syllable_index
    if((jung_i < 0) or (jung_i >= __HG_JUNG_NUM__)): # 중성 범위
        return syllable_index
    if((jong_i < 0) or (jong_i >= __HG_JONG_NUM__)): # 종성 범위
        return syllable_index
    #
    syllable_index = (cho_i * __HG_JUNG_X_JONG_NUM__) + (jung_i * __HG_JONG_NUM__) + jong_i
    if(SyllableFalg == True):  # 한글 음절을 돌려준다
        syllable = chr(syllable_index + __HG_SYL_LEADING_DEC__)
        return syllable
    else: # 한글 음절 인덱스를 돌려준다.
        return syllable_index

def PrintCodeValueBlock_Num(beginVal, charNum, decFlag=True, hexFlag=True, sep=' '):
    for i in range(0, charNum):
        char1 = chr(i + beginVal)
        char_code_value_string3 = get_char_code_value_string3(char1, decFlag=decFlag, hexFlag=hexFlag, sep=sep)
        print('%i :' %(i+1), sep, char_code_value_string3)
    print('total :', charNum)
    print()

    for i in range(0, charNum):
        print(chr(i + beginVal), end='')
    print()

def PrintCodeValueBlock_Value(beginVal, endVal):
    if(isinstance(beginVal, int) != True):
        print('logic error :', '(type(beginVal) != int) at',  __FUNCTION__)
        return
    if(isinstance(endVal, int) != True):
        print('logic error :', '(type(endVal) != int) at',  __FUNCTION__)
        return
    charnum = (endVal - beginVal) + 1
    PrintCodeValueBlock_Num(beginVal, charnum)

def PrintCodeValueBlock_Char(beginChar, endChar):
    if((len(beginChar) != 1) or (len(endChar) != 1)):
        print('logic error :', '((len(beginChar) != 1) or (len(endChar) != 0))')
        return
    #
    beginVal = ord(beginChar)
    endVal = ord(endChar)
    PrintCodeValueBlock_Value(beginVal, endVal)

def PrintCodeValue_String(String, sep=' '):
    hglen = len(String)
    tmpStr = ''
    for i in range(0, hglen):
        char1 = String[i]
        char_code_value_string3 = get_char_code_value_string3(char1, sep=sep)

        # print('%i :' %(i+1), sep, char_code_value_string3) # 너무 느려서 바꾼다.
        tmpStr += str(i + 1)
        tmpStr += sep
        tmpStr += char_code_value_string3
        tmpStr += '\n'
        if((i % 100) == 1):
            print(tmpStr, end='')
            tmpStr = ''
    print(tmpStr, end='')

def print_debug_msg(msg):
    if(__debug_print_on__ == True):
        print(msg)

def print_debug_msg_line(msg):
    if(__debug_print_on__ == True):
        print(__file__, __FUNCTION__, __LINE__, '\n', msg)

def find_mismatch_pos(str1, str2, match_len=0, state_print=False, print_len = 10):
    len1 = len(str1)
    len2 = len(str2)
    pos = 0
    while(pos < len1):
        char1 = str1[pos]
        char2 = str2[pos]
        if(char1 != char2):
            if(state_print == True):
                print('mis-match: ', pos)
                print('[a]', str1[pos:pos+print_len])
                print('[b]', str2[pos:pos+print_len])
                print()
            return pos
        pos += 1
        if(match_len > 0): # 비교 길이가 있으면 확인
            if(pos >= match_len):
                break
    return (-1)

def find_mismatch_pos_list(baseStr, compStr, mismatch_control_len = 5):
    # mismatch_control_len = 5 # 일치하지 않는 부분이 발견되면 '5'글자까지만 조정해본다
    mismatch_pos_list = []

    #
    base_mismatch_pos_total = 0
    comp_mismatch_pos_total = 0
    mismatch_cnt = 1
    while(1):
        mismatch_pos = find_mismatch_pos(baseStr, compStr)
        if(mismatch_pos < 0):
            break
        #-----------
        #-----------
        ##print('[%i]위치:' %mismatch_cnt, mismatch_pos_total, '(',mismatch_pos,')')
        ##print(baseStr[mismatch_pos:mismatch_pos+10])
        ##print(compStr[mismatch_pos:mismatch_pos+10])
        mismatch_cnt += 1

        base_mismatch_pos_total += mismatch_pos
        comp_mismatch_pos_total += mismatch_pos
        mismatch_pos_item = {'base':base_mismatch_pos_total, 'comp':comp_mismatch_pos_total}
        mismatch_pos_list.append(mismatch_pos_item)

        #-----------
        # 새로운 위치를 찾아본다.
        #-----------
        baseStr_new = baseStr[mismatch_pos:]
        compStr_new = compStr[mismatch_pos:]

        # check first1
        new_base_pos = 0
        new_comp_pos = 0
        new_mismatch_pos = 0
        while(1):
            if(new_base_pos >= mismatch_control_len):
                break
            
            new_mismatch_pos = 0
            new_comp_pos = 0
            while(1):
                #print(new_base_pos, new_comp_pos)
                #print(baseStr_new[new_base_pos:20])
                #print(compStr_new[new_comp_pos:20])
                if(new_comp_pos >= mismatch_control_len):
                    break
                new_mismatch_pos = find_mismatch_pos(baseStr_new[new_base_pos:], compStr_new[new_comp_pos:], match_len=mismatch_control_len)
                #print('new_mismatch_pos:',new_mismatch_pos)
                if(new_mismatch_pos >= 0):
                    new_comp_pos += 1
                    continue
                elif(new_mismatch_pos < 0): # match
                    break
            if(new_mismatch_pos < 0): # match
                break
            new_base_pos += 1
        if(new_mismatch_pos < 0): # match
            baseStr = baseStr_new[new_base_pos:]
            compStr = compStr_new[new_comp_pos:]
            #print('---새로운 일치---')
            #print(baseStr[:20])
            #print(compStr[:20])

            base_mismatch_pos_total += new_base_pos
            comp_mismatch_pos_total += new_comp_pos

            continue
        break
    return mismatch_pos_list

def hexUpper(curVal):
    if(isinstance(curVal, int) == False):
        return ''
    curHex = hex(curVal)
    curHex = curHex[2:]
    curHex = curHex.upper()
    curHex = '0x' + curHex
    return curHex


def PrintList_ByLine(List, NumInLine=1, ShowIndex=True, SepInLine='\t'): 
    i = 0
    for x in List:
        if(ShowIndex==True):
            print(i, ': ', end='')
        print(x, end='')
        if(NumInLine <= 1): # 한줄에 1개 출력
            print()
        else: # 한줄에 여러 개 출력
            print(SepInLine, end='')
            if(((i + 1) % NumInLine) == 0): # 한 줄당 몇개 출력
                if(i != 0): # 맨처음은 출력하면 안 된다.
                    print()
            
        i += 1

def PrintDictList_ByLine(DictList, ShowIndex=True): 
    i = 0
    for x in DictList:
        if(ShowIndex==True):
            print('%i' %i, ':', end='')
        print(x)
        i += 1


def GetCharDictList_CharList(charlist):
    char_dict_list = []

    charlist_sort = charlist.copy()
    charlist_sort.sort() # by abc

    i = 0
    pre_c = None
    for c in charlist_sort:
        #print(i)
        append_flag = False
        if(i == 0):
            append_flag = True
        else:
            if(pre_c['char'] == c):
                freq = pre_c['freq']
                freq += 1
                pre_c['freq'] = freq
                c = pre_c
            else:
                append_flag = True

        if(append_flag == True):
            char_dict = {'char': c, 'freq': 1, 'code': ord(c), 'hex': hex(ord(c))}
            char_dict_list.append(char_dict)
            pre_c = char_dict
        else:
            pre_c = c
        # next
        i += 1
        #print(pre_c)

    return char_dict_list

def GetCharDictList_String(string):
    charlist = [char for char in string]
    char_dict_list = GetCharDictList_CharList(charlist)
    return char_dict_list


