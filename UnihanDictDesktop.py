import sys
from UnihanDict import UnihanDict 
import simplejson as json

default_unihan_location = u"public/data_tables/unihan.txt"
default_pinyin_location = u"public/data_tables/pinyin_tr_table.txt"
default_unihan_cache_location = u"public/pickle/unihan_pickle.data"
default_pinyin_table_json_location = u"public/pickle/pinyin_tr_table.json"


class UnihanDictDesktop(UnihanDict):
    def load(self):
        self.load_from_file()

    def load_json(self, url, method='file'):
        json_data = None
        if method is 'file':
            with open(url) as f:
                json_str = f.read()
                json_data = json.loads(json_str)
        return json_data
    
    def write_json(self, json_data, url, method='file'):
        if method is 'file':
            with open(url, 'wb') as f:
                f.write(json.dumps(json_data))
        

    def load_from_file(self, unihan_location = default_unihan_location, pinyin_location=default_pinyin_location, unihan_cache_location = default_unihan_cache_location, pinyin_table_json_location = default_pinyin_table_json_location):
        # set file locations
        self.unihan_location = unihan_location
        self.pinyin_location = pinyin_location
        self.unihan_cache_location = unihan_cache_location
        self.pinyin_table_json_location = pinyin_table_json_location
        self.pinyin_dict = self.load_translit_table_from_file() # load pinyin dictionary
        self.unihan_dict = self.load_unihan_from_file()         # load unihan dictionary    



    
    def load_unihan_from_file(self):
        
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
            print 'loading unihan from json file...'
            unihan_json = unihan_json_f.read()
            unihan_dict = json.loads(unihan_json)
            #print unihan_json
            #print unihan_dict

        # if we can't find the pickle then we need to generate the info from unihan
                
        if unihan_dict is None:
                print "opening unihan flat file"
                unihan_dict = self.parse_unihan_db(self.unihan_location)
                unihan_pickle_f = open(self.unihan_cache_location, "wb")
                pickle.dump(unihan_dict,unihan_pickle_f)

        if unihan_json_f is None:
            unihan_json = self.serialize(mode = 'json')
            unihan_pickle_f = open(self.unihan_cache_location + '.json', "wb")
            unihan_pickle_f.write(unihan_json)
            unihan_pickle_f.close()
            
        return unihan_dict
                
        
     
    def load_translit_table_from_file(self):
            json_pinyin_f = None
            py_dict = None
            try:
                print "opening pinyin table to read json..."
                py_dict = self.load_json(self.pinyin_table_json_location)
            except IOError:
                if self.isDesktop:
                    print "could not find pinyin table to read json...loading from flat file"
                    table_f = open(self.pinyin_location,"r")
                    py_dict = {}
                    for line in table_f:
                            line = line.decode('utf-8') # we need to make sure each line is unicode before we start
                            line_elms = line.split(u"\t")
                            if line_elms:
                                    for i in xrange(0,len(line_elms)):
                                            line_elms[i] = line_elms[i].strip() # take off the white space if there is any
                        
                                    py_dict[line_elms[0].lower().strip()] = line_elms
                    table_f.close()

                    self.write_json(py_dict, self.pinyin_table_json_location)
            except:
                print "Unexpected error:", sys.exc_info()[0]
            return py_dict




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
