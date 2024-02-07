from pybtex.database import parse_file
import traceback
import re

class Translator:

    def __init__(self, bibtex_file_path, word_bib_file_path):
        # maps the word index of a reference (e.g., "[0]") to a latex bibtex key
        # latex bibtex key to be used as e.g., "\cite{mueller2020}"
        # where "mueller2020" is the latex bibtex key
        self.map = {}
        # bibtex data from bibtex.Parser()
        self.bibdata = {}
        # copy of bibtex data to edit the title to a "clean" title
        # title stripped by everything that is not a-z and set to lowercase
        self.bibdata_clean = {}
        # bibliography from MS Word as string
        self.bib_word_str = ""
        # mapping MS Word's bibliography index (IEEE style e.g., [0]) to bib_id
        # bib_id is a unique identifier of the corresponding BibTex entry/reference
        self.bib_word_map_clean = {}

        self.init_bibtex(bibtex_file_path)
        self.init_word(word_bib_file_path)

        self.find_all()
        return

    def write_to_file(self, input_file_path: str, output_file_path: str):
        txt = self.replace_all(input_file_path)
        Translator.write_file(file_path=output_file_path, content=txt)

    def init_bibtex(self, file_path):
        self.read_bibtex(file_path)
        self.generate_clean_bibtex_titles()

    def init_word(self, file_path: str):
        self.bib_word_str = Translator.read_file(file_path)
        self.generate_word_map(self.bib_word_str)    

    def read_bibtex(self, file_path: str):
        self.bibdata = parse_file(file_path)
       
    def generate_clean_bibtex_titles(self):
        print("cleaning BibTex titles..")
        #loop through the individual references
        for bib_id in self.bibdata.entries:
            b = self.bibdata.entries[bib_id].fields
            try:
                print(b["title"])
                clean_title = Translator.clean_string(b["title"])
                print(clean_title)
                self.bibdata_clean[bib_id] = { 
                        "title": clean_title,
                        "bib_id": bib_id
                }

            # field may not exist for a reference
            except KeyError:
                #continue
                traceback.print_exc()

    @staticmethod
    def clean_string(mystr: str) -> str:
        # lowercase
        # remove everything except letters
        return re.sub(r'[^a-z]+', '', mystr.lower())
 
    @staticmethod
    def remove_whitespace(mystr: str) -> str:
        return re.sub(r'\s+', '', mystr) 

    def find_bibtex_entry(self, title_clean: str) -> str:    
        #loop through the individual references
        for bib_id in self.bibdata.entries:
            b = self.bibdata.entries[bib_id].fields
            
            if title_clean == self.bibdata_clean[bib_id]["title"]: 
                return bib_id
        
    @staticmethod
    def read_file(file_path) -> str:
        print(f"Reading file {file_path}...")
        with open(file_path, 'r') as content_file:
            content = content_file.read()
        return content

    @staticmethod
    def write_file(file_path: str, content: str):
        print(f"Writing file {file_path}...")
        with open(file_path, 'w') as content_file:
            content_file.write(content)

    def generate_word_map(self, bibliography: str):
        # better safe than sorry, remove any whitespace
        no_whitespace = Translator.remove_whitespace(self.bib_word_str)

        splits = re.split("\[\d+\]", no_whitespace)
        # remove first element, as it's empty
        splits.pop(0)

        for i, split in enumerate(splits):
            # get the title which is enclosed by these quotation marks
            result = re.search('“(.*)”', split)
            title_dirty = result.group(1) # group(0) contains the strange quotation marks
            self.bib_word_map_clean[i+1] = Translator.clean_string(title_dirty) 

    def find_all(self):
        for word_index, title_clean in self.bib_word_map_clean.items():
            self.map[word_index] = self.find_bibtex_entry(title_clean) 

    def replace_all(self, text_file_path: str) -> str:
        txt_latex = Translator.read_file(text_file_path)
        for word_index, bibtex_key in self.map.items():
            txt_latex = txt_latex.replace(f"[{word_index}]", f"\cite{{{bibtex_key}}}")
        return txt_latex   
