# -*- coding: utf-8 -*-
import re


# define some variables here for the 5 types of pinyin we can use for transliteration
# These are the order they exist in the pinyin transliteration table. ()
tr_pinyin = 0  # Hanyu Pinyin (Standard in Mainland China and now in Taiwan)
tr_zhuyin = 1  # Zhuyin Fuhao (Standard in Taiwan)
tr_wg = 2      # Wade-Giles (former standard--common in Taiwan)
tr_tongyu = 5  # Tongyu Pinyin ([former]Taiwanese standard)
tr_gwoyu = 6   # Gwoyeu Romatzyh (old R.O.C. standard)

# indicate here what forms of translieration we would like the program to output
default_output_tr = [tr_zhuyin, tr_pinyin, tr_wg, tr_gwoyu]

class UnihanDict:




    def __init__(self, output_tr = default_output_tr):
        self.output_tr = output_tr

            

    # input: int val of the unicode chr
    # output: key of chr to use with unicode_dict
    def make_key(self, chr_int):
        return 'u' + hex(chr_int)[2:].lower()

    def convert(self, name):
        prons = [self.unihan_dict.get(self.make_key(ord(n)),u'?') for n in name] # apply the "get" function of the associative array to each name in our array.  Convert the chinese character to it's unicode form (integer)
        prons_arr = []
        # for each kind of pinyin output we wish to use.
        # concatenate them with "tab"s 
        for tr in self.output_tr:
                prons_arr.append(  self.format_pron_of_name(prons, tr)  )
        prons_uni = u'\t'.join(prons_arr)
        return name + u'\t' + prons_uni # add the original Chinese name to the front.

#pinyin = 0  # Hanyu Pinyin
#zhuyin = 1  # Zhuyin Fuhao
#wg = 2      # Wade-Giles
#tongyu = 5  # Tongyu Pinyin ([former]Taiwanese standard)
#gwoyu = 6   # Gwoyeu Romatzyh (old R.O.C. standard)           
    def set_pinyin_type(self, pinyin = 0, zhuyin = 0, wg = 0, tongyu = 0, gwoyu = 0):
        tr_opts_request = [pinyin, zhuyin, wg, tongyu, gwoyu]
        tr_defs = [tr_pinyin, tr_zhuyin, tr_wg, tr_tongyu, tr_gwoyu]
        tr_opts = map(lambda i, j: i if j else None, tr_defs, tr_opts_request)
        tr_opts = filter(lambda i: True if i is not None else False, tr_opts)
        self.output_tr = tr_opts


# convert a single phoneme from Hanyu Pinyin to another format
    def convert_pinyin(self, pinyin_in, enc):
        number = pinyin_in[-1]
        pinyin_phones = pinyin_in.split(u" ")
        pinyin = ''
        pinyin_arr = []
        zhuyin_accents = (u'', u'ˊ',u'ˇ',u'ˋ')
        for p in pinyin_phones:
            p=p.strip()
            number = p[-1]
            if number in (u'1',u'2',u'3',u'4',u'5'):
                pinyin = p[:-1]
                if(enc<6):
                    #phonetic_lookup = pinyin_dict.get(pinyin.lower(),(u"?",u"?",u"?",u"?",u"?"))
                    phonetic_lookup = self.pinyin_dict.get(pinyin.lower(),u'?')
                    if phonetic_lookup != u'?':

                        if enc == tr_zhuyin:
                                if(number == u'5'):
                                        number = u'1'
                                n = int(number)
                                accent = zhuyin_accents[n-1]
                                pinyin_arr.append( phonetic_lookup[enc] +accent)
                        else:
                                pinyin_arr.append( phonetic_lookup[enc] +number)
                    else:
                        pinyin_arr.append(u"?")
                else: #gwoyuluomatsih
                    if(number == u'5'):
                            pinyin_arr.append( self.pinyin_dict.get(pinyin.lower(),("?","?","?","?","?","?","?","?","?"))[enc]+u'.' )
                    else:
                            pinyin_arr.append( self.pinyin_dict.get(pinyin.lower(),("?","?","?","?","?","?","?","?","?"))[enc+int(number)-1])
        return u''.join(pinyin_arr)  


# input: array of pinyin strings separated by a single space
# output: a string of another pinyin style.
#         If there is more than one phoneme in an array, it means that there is more than one
#         proununciation.  So in that case, we put them in parenthesis and add a dash to separate them.
#         Finally, the phonemes are concatonated together and returned.
# For the options for enc, see function convert_pinyin
    def format_pron_of_name(self, pron_of_chars_arr, enc):
        #each element is of the format u'pron1 pron2 pron3 etc'
        #pron_double_arr = [] # <-- unused
        output_arr = []
        
        # for each string in the array
        # split the string on space " " to get individual pinyin phonemes
        # then convert each phoneme to another format using convert_pinyin
        for p in pron_of_chars_arr:
                p_arr = []
                if len(p)>0:
                        p_arr = p.split(u' ')
                        p_arr = [self.convert_pinyin(phone, enc) for phone in p_arr] # apply convert_pinyin to all elements in the array
                        #pron_double_arr.append(p_arr) #<-- unused

                        # if the array is longer than one, there is more than one possible pronunciation.  Put them in parenthises and concatenate with a dash.
                        if len(p_arr) > 1:
                              output_arr.append(   u'(' + u'-'.join(p_arr) + u')'   )
                        else:
                              output_arr.append(p_arr[0])
        return u' '.join(output_arr)


    



        
