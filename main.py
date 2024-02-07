import argparse
from translate import Translator 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bibtex", type=str, help="BibTex file including all references")
    parser.add_argument("text_file", type=str, help="Text file containing the Bibliography from Word")
    parser.add_argument("input_file", type=str, help="Input text file containing MS Word text with IEEE reference style e.g., [0]")
    parser.add_argument("output_file", type=str, help="Output text file containing text with latex compatible citation e.g., \cite{mueller2022}")
  
    args = parser.parse_args()
    bibtex = args.bibtex
    text_file = args.text_file
    input_file = args.input_file
    output_file = args.output_file

    Translator(bibtex_file_path=bibtex, word_bib_file_path=text_file).write_to_file(input_file, output_file)
