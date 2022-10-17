import inspect

import hgbasic
import hgchartype
##----------
##----------

### define
__chosung_char_list__ = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ' # Hangul Compatibility Jamo (0x3131-ex314E)(ksc5601: 0xA4A1~0xA4BE)
__jungsung_char_list__ = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ' # Hangul Compatibility Jamo (0x314F-0x3163)(ksc5601:0xA4BF~0xA4D3)
__jongsung_char_list__ = 'ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ' # Hangul Compatibility Jamo (ksc5601 0xA4A1 ~ 0xA4BE <= 종성부용초성)


__chosung_jamo_code_list__ = [0x1100,0x1101,0x1102,0x1103,0x1104,0x1105,0x1106,0x1107,0x1108,
                            0x1109,0x110a,0x110b,0x110c,0x110d,0x110e,0x110f,0x1110,0x1111,0x1112] 
__jungsung_jamo_code_list__ = [0x1161,0x1162,0x1163,0x1164,0x1165,0x1166,0x1167,0x1168, 0x1169, 0x116a,
                            0x116b,0x116c,0x116d,0x116e,0x116f,0x1170,0x1171,0x1172, 0x1173, 0x1174,0x1175] 
__jongsung_jamo_code_list__ = [0x11a8, 0x11a9, 0x11aa,0x11ab,0x11ac,0x11ad,0x11ae,0x11af, 0x11b0,
                            0x11b1,0x11b2, 0x11b3, 0x11b4, 0x11b5, 0x11b6, 0x11b7, 0x11b8, 0x11b9, 
                            0x11ba, 0x11bb, 0x11bc, 0x11bd, 0x11be, 0x11bf, 0x11c0, 0x11c1, 0x11c2] 

__chosung_jamo_string__ = 'ᄀᄁᄂᄃᄄᄅᄆᄇᄈᄉᄊᄋᄌᄍᄎᄏᄐᄑᄒ'  # Hangul Jamo (0x1110-0x1112)
__jungsung_jamo_string__ = 'ᅡᅢᅣᅤᅥᅦᅧᅨᅩᅪᅫᅬᅭᅮᅯᅰᅱᅲᅳᅴᅵ'  # Hangul Jamo (0x1161-0x1175)
__jongsung_jamo_string__ = 'ᆨᆩᆪᆫᆬᆭᆮᆯᆰᆱᆲᆳᆴᆵᆶᆷᆸᆹᆺᆻᆼᆽᆾᆿᇀᇁᇂ' # Hangul Jamo (0x11A8-0x11C2)

__SingleDotBangjeom = '〮' # 0x302E 	HANGUL SINGLE DOT TONE MARK
__DoubleDotBangjeom = '〯' # 0x302F 	HANGUL DOUBLE DOT TONE MARK

__HANGUL_CHOSEONG_FILLER_v__ = int('115F', 16)   # 'ᅟ'  (화면에 안 보임)
__HANGUL_CHOSEONG_FILLER__ =  'ᅟ' # 4447  0x115F # (화면에 안 보임)
__HANGUL_JUNGSEONG_FILLER_v__ = int('1160', 16) # 'ᅠ' (화면에 안 보임)
__HANGUL_JUNGSEONG_FILLER__ = 'ᅠ' # 4448  0x1160 # (화면에 안 보임)
#---------------------------------------------
#---------------------------------------------

def __HG_CHO_CHAR(chosung_inx, jamo=True):
    chosung_jamo = 0
    if((chosung_inx < 0) or (chosung_inx >= hgbasic.__HG_CHO_NUM__)): 
        return chosung_jamo  # logic error
    if(jamo==True):
        return __chosung_jamo_string__[chosung_inx]
    else:
        return __chosung_char_list__[chosung_inx]

def __HG_JUNG_CHAR(jungsung_inx, jamo=True):
    jungsung_jamo = 0
    if((jungsung_inx < 0) or (jungsung_inx >= hgbasic.__HG_JUNG_NUM__)): 
        return jungsung_jamo  # logic error
    if(jamo==True):
        return __jungsung_jamo_string__[jungsung_inx]
    else:
        return __jungsung_char_list__[jungsung_inx]

def __HG_JONG_CHAR(jongsung_inx, jamo=True):
    jongsung_jamo = 0
    if((jongsung_inx < 0) or ((jongsung_inx + 1) > hgbasic.__HG_JONG_NUM__)): 
        return jongsung_jamo  # logic error
    if(jongsung_inx == 0): return jongsung_jamo # fill-state
    if(jamo==True):
        return __jongsung_jamo_string__[jongsung_inx - 1]
    else:
        return __jongsung_char_list__[jongsung_inx - 1]

def hgGetChosungInx_Char(hgchar):
    chosung_inx = (-1)
    hglen = len(hgchar)
    if(hglen != 1): 
        return chosung_inx
    
    syllable_inx = hgGetSyllable_inx(hgchar)
    jongsung_inx = hgGetJongsungInx_Char(hgchar)
    jungsung_inx = hgGetJungsungInx_Char(hgchar)
    if((syllable_inx < 0) or (jongsung_inx < 0) or (jungsung_inx < 0)):
        return chosung_inx
    
    syl_jong_div_jong_inx = int((syllable_inx - jongsung_inx) / hgbasic.__HG_JONG_NUM__)
    xxx_minus_jung_inx = syl_jong_div_jong_inx - jungsung_inx
    chosung_inx = int(xxx_minus_jung_inx / hgbasic.__HG_JUNG_NUM__)
    return chosung_inx

def hgGetJungsungInx_Char(hgchar):
    jungsung_inx = (-1)
    hglen = len(hgchar)
    if(hglen != 1): 
        return jungsung_inx
    
    syllable_inx = hgGetSyllable_inx(hgchar)
    jongsung_inx = hgGetJongsungInx_Char(hgchar)
    if((syllable_inx < 0) or (jongsung_inx < 0)):
        return jungsung_inx
    
    syl_jong_div_jong_inx = int((syllable_inx - jongsung_inx) / hgbasic.__HG_JONG_NUM__)
    jungsung_inx = syl_jong_div_jong_inx % hgbasic.__HG_JUNG_NUM__
    return jungsung_inx

def hgGetJongsungInx_Char(hgchar):
    jongsung_inx = (-1)
    hglen = len(hgchar)
    if(hglen != 1): 
        return jongsung_inx

    syllable_inx = hgGetSyllable_inx(hgchar)
    if(syllable_inx < 0):
        return jongsung_inx

    jongsung_inx = syllable_inx % hgbasic.__HG_JONG_NUM__
    return jongsung_inx

def _hgGetJongsungInx_Hginx_del_think(syllable_inx):
    if((syllable_inx < 0) or (syllable_inx >= hgbasic.__HG_SYL_NUM__)): return (-1)
    jongsung_inx = syllable_inx % hgbasic.__HG_JONG_NUM__
    return jongsung_inx

def hgGetSyllable_inx(hgchar):
    syllable_inx = (-1)
    hglen = len(hgchar)
    if(hglen != 1): return syllable_inx
    dec_char = ord(hgchar)
    syllable_inx = dec_char - hgbasic.__HG_SYL_LEADING_DEC__
    if(syllable_inx >= hgbasic.__HG_SYL_NUM__): # 한글 음절 범위 초과
        syllable_inx = (-1)
    return syllable_inx


def hgGetChoJungJongInx_Char(hgchar):
    ChoJungJongInx = {}
    hglen = len(hgchar)
    if(hglen != 1): 
        return ChoJungJongInx

    chosung_inx = hgGetChosungInx_Char(hgchar)
    jungsung_inx = hgGetJungsungInx_Char(hgchar)
    jongsung_inx = hgGetJongsungInx_Char(hgchar)
    if((chosung_inx < 0) or (jungsung_inx < 0) or (jongsung_inx < 0)): 
        return ChoJungJongInx
    ChoJungJongInx = {'cho': chosung_inx, 'jung': jungsung_inx, 'jong':jongsung_inx}
    return ChoJungJongInx

def hgGetChoJungJongString_Inx(ChoJungJongInx, jamo=True):
    ChoJungJongString = '';
    if(ChoJungJongInx == None): 
        return ChoJungJongString
    if(len(ChoJungJongInx) <= 0):
        return ChoJungJongString
    if ChoJungJongInx['cho'] != None:
        if(ChoJungJongInx['cho'] >= 0): 
            ChoJungJongString += __HG_CHO_CHAR(ChoJungJongInx['cho'], jamo)
    if ChoJungJongInx['jung'] != None:
        if(ChoJungJongInx['jung'] >= 0): 
            ChoJungJongString += __HG_JUNG_CHAR(ChoJungJongInx['jung'], jamo)
    if ChoJungJongInx['jong'] != None:
        if(ChoJungJongInx['jong'] >= 1):  # 0-inx, fill-code
            ChoJungJongString += __HG_JONG_CHAR(ChoJungJongInx['jong'], jamo)
    return ChoJungJongString

def hgGetChoJungJongString_Char(hgchar, jamo=True):
    ChoJungJongString = ''
    ChoJungJongInx = hgGetChoJungJongInx_Char(hgchar)
    if(len(ChoJungJongInx) >= 1):
        ChoJungJongString = hgGetChoJungJongString_Inx(ChoJungJongInx, jamo)
    return ChoJungJongString

def hgGetChoJungJongJamo_Inx(ChoJungJongInx):
    ChoJungJongJamo = {}
    if(ChoJungJongInx == None): 
        return ChoJungJongJamo
    if(len(ChoJungJongInx) <= 0):
        return ChoJungJongJamo

    if ChoJungJongInx['cho'] != None:
        if(ChoJungJongInx['cho'] >= 0): 
            ChoJungJongJamo['cho'] = __HG_CHO_CHAR(ChoJungJongInx['cho'], jamo=True)
    if ChoJungJongInx['jung'] != None:
        if(ChoJungJongInx['jung'] >= 0): 
            ChoJungJongJamo['jung'] = __HG_JUNG_CHAR(ChoJungJongInx['jung'], jamo=True)
    if ChoJungJongInx['jong'] != None:
        if(ChoJungJongInx['jong'] >= 1):  # 0-inx, fill-code
            ChoJungJongJamo['jong'] = __HG_JONG_CHAR(ChoJungJongInx['jong'], jamo=True)
    return ChoJungJongJamo

def hgGetChoJungJongJamo_Char(hgchar):
    ChoJungJongJamo = {}
    ChoJungJongInx = hgGetChoJungJongInx_Char(hgchar)
    if(len(ChoJungJongInx) > 0):
        ChoJungJongJamo = hgGetChoJungJongJamo_Inx(ChoJungJongInx)
    return ChoJungJongJamo

def PrintChoJungJongChar_Inx(ChoJungJongInx, jamo=True):
    if(ChoJungJongInx == None): 
        return
    if(len(ChoJungJongInx) <= 0):
        return
    print('자모:', end='')
    ChoJungJongString = hgGetChoJungJongString_Inx(ChoJungJongInx, jamo)
    print(ChoJungJongString, end='')
    #print('')

def PrintChoJungJongChar(hgchar, jamo=True):
    ChoJungJongInx = hgGetChoJungJongInx_Char(hgchar)
    if(len(ChoJungJongInx) >= 1):
        PrintChoJungJongChar_Inx(ChoJungJongInx, jamo)

def hgGetChoJungJongString(string, jamo=True):
    #print(string)
    ChoJungJongString = '';
    hglen = len(string)
    for inx in range(0, hglen):
        hgchar = string[inx]
        ChoJungJongString_Cur = hgGetChoJungJongString_Char(hgchar, jamo)
        if(len(ChoJungJongString_Cur) <= 0):
            ChoJungJongString += hgchar
        else:
            ChoJungJongString += ChoJungJongString_Cur
    #print(ChoJungJongString)
    return ChoJungJongString

def getSyllableSound(hgchar):
    # {닿, 홀, ㄹ} = 닿(소리), 홀(소리), ㄹ(소리)
    SylSound = ''
    ChoJungJongJamo = hgGetChoJungJongJamo_Char(hgchar)
    if(len(ChoJungJongJamo) <= 0):
        return SylSound
    if('jong' in ChoJungJongJamo):
        if(len(ChoJungJongJamo['jong']) > 0):
            if(ChoJungJongJamo['jong'] == 'ᆯ'): # 종성_ㄹ = 'ᆯ' # 4527 0x11af
                SylSound = 'ㄹ' # 키보드 입력을 고려해서 한글 호환 자모 'ㄹ' 이다.
            else:
                SylSound = '닿'
        else:
            SylSound = '닿'
    elif(len(ChoJungJongJamo['jung']) > 0):
        SylSound = '홀'
    elif(len(ChoJungJongJamo['cho']) > 0):
        SylSound = '닿'
    else:
        pass
    return SylSound

def getVoulHarmony(hgchar):
    # {양, 음} = 양(성), 음(성)
    VoulHarmony = ''
    ChoJungJongJamo = hgGetChoJungJongJamo_Char(hgchar)
    if(len(ChoJungJongJamo) <= 0):
        return VoulHarmony
    if('jung' in ChoJungJongJamo):
        if(len(ChoJungJongJamo['jung']) > 0):
            if(ChoJungJongJamo['jung'] == 'ᅡ'): # 중성_ㅏ = 'ᅡ' # 4449 0x1161'
                VoulHarmony = '양'
            elif(ChoJungJongJamo['jung'] == 'ᅩ'): # 중성_ㅗ = 'ᅩ' # 4457 0x1169'
                VoulHarmony = '양'
            elif(ChoJungJongJamo['jung'] == 'ᅪ'): # 중성_ㅘ = 'ᅪ' # 4458 0x116a'
                VoulHarmony = '양'
            else:
                VoulHarmony = '음'
    return VoulHarmony

