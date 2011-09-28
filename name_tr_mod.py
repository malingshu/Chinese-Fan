# -*- coding: utf-8 -*-
import re
import sys
import pickle
import json

# define some variables here for the 5 types of pinyin we can use for transliteration
# These are the order they exist in the pinyin transliteration table. ()
tr_pinyin = 0  # Hanyu Pinyin
tr_zhuyin = 1  # Zhuyin Fuhao
tr_wg = 2      # Wade-Giles
tr_tongyu = 5  # Tongyu Pinyin ([former]Taiwanese standard)
tr_gwoyu = 6   # Gwoyeu Romatzyh (old R.O.C. standard)

# indicate here what forms of translieration we would like the program to output
default_output_tr = [tr_zhuyin, tr_pinyin, tr_wg, tr_gwoyu]

class UnihanDict:
    def __init__(self, unihan_location= u"data_tables/unihan.txt", pinyin_location=u"data_tables/pinyin_tr_table.txt", unihan_cache_location = u"pickle/unihan_pickle.data", output_tr = default_output_tr):
        self.unihan_location = unihan_location
        self.pinyin_location = pinyin_location
        self.unihan_cache_location = unihan_cache_location
        self.output_tr = output_tr

    def load(self):
        # pinyin_dict allows us to convert between the various versions of pinyin                      
        # pinyin_dict needs to be global because it is used in function convert_pinyin as a global variable
        # so we declare it here first
        self.pinyin_dict = self.load_translit_table(self.pinyin_location)
        # unihan_dict contains the values of the mandarin pronunciation for all chinese characters
        unihan_dict = None
        unihan_pickle_f = None
        unihan_json_f = None
        # if it the program has been run before on this system, then we can try to open the pickle of the database
        # this can save several seconds since the unihan file is very large
        try:
            unihan_pickle_f = open(self.unihan_cache_location)
        except:
            # if there is an error, do nothing and leave unihan_pickle_f as None
            pass
        try: 
            unihan_json_f = open(self.unihan_cache_location + '.json')
        except:
            print 'cannot open unihan json file: ' + self.unihan_cache_location + '.json'
            pass

        if unihan_json_f is not None:
            print 'json...'
            unihan_json = unihan_json_f.read()
            unihan_dict = json.loads(unihan_json)
            #print unihan_json
            #print unihan_dict

        # if we can't find the pickle then we need to generate the info from unihan
#        if(unihan_pickle_f is not None):
#                print "opening unihan pickle file"
#                unihan_dict = pickle.load(unihan_pickle_f)
#                unihan_pickle_f.close()
                
        if unihan_dict is None:
                print "opening unihan flat file"
                unihan_dict = self.parse_unihan_db(self.unihan_location)
                unihan_pickle_f = open(self.unihan_cache_location, "wb")
                pickle.dump(unihan_dict,unihan_pickle_f)
        self.unihan_dict = unihan_dict

        if unihan_json_f is None:
            unihan_json = self.serialize(mode = 'json')
            unihan_pickle_f = open(self.unihan_cache_location + '.json', "wb")
            unihan_pickle_f.write(unihan_json)
            unihan_pickle_f.close()
            

    def serialize(self, mode='json'):
        if mode is 'json':
            unihan_ser = json.dumps(self.unihan_dict)
        if mode is 'pickle':
            unihan_ser = pickle.dumps(unihan_dict)

        return unihan_ser

    # input: int val of the unicode chr
    # output: key of chr to use with unicode_dict
    def make_key(self, chr_int):
        return 'u' + hex(chr_int)[2:].lower()

    def convert(self, name):
        # because json.dumps saves the int in the key of the hash as a str
        # we are stuck with str
        #prons = [self.unihan_dict.get(str(ord(n)),u'?') for n in name] # apply the "get" function of the associative array to each name in our array.  Convert the chinese character to it's unicode form (integer)
        prons = [self.unihan_dict.get(self.make_key(ord(n)),u'?') for n in name] # apply the "get" function of the associative array to each name in our array.  Convert the chinese character to it's unicode form (integer)
        #prons = [self.unihan_dict.get(n, u'?') for n in name] # apply the "get" function of the associative array to each name in our array.  Convert the chinese character to it's unicode form (integer)


        

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
                
        
     
    def load_translit_table(self, table_file_location):
            table_f = open(table_file_location,"r")
            py_dict = {}
            for line in table_f:
                    line = line.decode('utf-8') # we need to make sure each line is unicode before we start
                    line_elms = line.split(u"\t")
                    if line_elms:
                            for i in xrange(0,len(line_elms)):
                                    line_elms[i] = line_elms[i].strip() # take off the white space if there is any
                
                            py_dict[line_elms[0].lower().strip()] = line_elms
            return py_dict


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




# find the pinyin pronunciation of each character in the unihan database
# and put them into an associative array.
# the key of the associative array is the unicode value (an integer)
# the value is the pronunciation (a string)
# some characters have multiple pronunciaitons, so each is separated by a space
    def parse_unihan_db(self, file_loc, field_name = u'kMandarin'):
        file_in = None
        try:
                file_in = open(file_loc)
        except:
                print "Cannot find the unihan file. Looking in: " + file_loc
                return None
                #import sys
                #sys.exit(1)
        db_dict = {}
        line_no = 0
        for line in file_in:
            # Skip the first line of the unihan file.  It makes us choke.
            if line_no == 0:
                    line_no = line_no +1
                    pass
            else:
                    # change to unicode and remove trailing whitespace
                    line = line.decode('utf-8').strip()

                    # split line on tabs to make array
                    line_arr = line.split(u"\t")
                    if(len(line_arr)>2):
                            # if the line gives the pronunication
                            if line_arr[1] == field_name:
                                    # first position of the array is the hex value
                                    # the first two chars are unneeded, so only take the chars after the first two
                                    # change to lowercase
                                    uni_hex_chars = "%s%s"% (u"0x",line_arr[0][2:].lower())

                                    # convert hex string to a native int value
                                    uni_int = int(uni_hex_chars,16)
                                    uni_key = self.make_key(uni_int)
                                    

                                    # save in our associative array
                                    # key: unicode value as an int, value: pronunciation in Mandarin as lowercase roman chars
                                    #db_dict[uni_int] = line_arr[2].lower()
                                    db_dict[uni_key] = line_arr[2].lower()
        return db_dict

# load the file with the names we want to translate into an array
# the file must be utf-8 (unicode) file
# one name on each line
    def load_name_file(self, name_file_location, file_enc = 'utf-8'):
        f = open(name_file_location)
        name_arr = []
        for line_str in f:
                l = line_str.decode(file_enc) # convert bytes to unicode
                name_arr.append(l.strip())    # add to the array, take off whitespace
        return name_arr


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
        
