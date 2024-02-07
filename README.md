# WordBibLinker - Translating references from MS Word to latex

## The situation

A report written in MS Word might include citations and a bibliography similar to the following:
```
Lorem ipsum dolor sit amet [1], consectetur adipiscing elit. Morbi quis bibendum massa, vel volutpat quam. Aliquam tristique velit non arcu euismod tempus. Nullam placerat porttitor arcu, a venenatis augue malesuada vel [2]. Pellentesque interdum felis at eros suscipit, vel molestie lectus tempus.

...

References

[1] S. Sung, “Extending High-Level Tooling for Task-Parallel Somethings” in 29th IEEE on Something proceedings, 2021.
[2] C. Mueller, “This could be your paper title”, 2023.
```

We also have a [BibTex file](example/references.bib):
```
@inproceedings{bibtex2021,
   abstract = {Imagine this was an abstract.},
   author = {Sung, Sam},
   journal = {29th IEEE on Something proceedings},
   title = {Extending High-Level Tooling for Task-Parallel Somethings},
   year = {2021},
}
@article{mueller2023,
   author = {Mueller, Christoph},
   title = {This could be your paper title},
   year = {2023},
}
```

## The problem

While we can export bespoke `references.bib` file from our favourite reference manager, we cannot translate the IEEE citation style used in MS Word to latex compatible citations.

## The solution

We match each reference in the MS Word bibliography to the correct BibTex entry in our `references.bib` file. For this, we parse the MS Word bibliography and compare titles to titles from the `references.bib` file until we have found the corresponding `bib_id` which is a unique identifier for BibTex entries.

### Caveats

Every BibTex entry requires 
* a `title` as we match these between MS Word and BibTex, and 
* a `bib_id` (the unique identifier used with `\cite{}` e.g., `\cite{mueller2021}` where `mueller2021` is the `bib_id`)
* the text input from word is provided as .txt file

## What do we need? 

* [A BibTex bibliography](example/references.bib)
* [A Bibliography from MS Word](example/word_bib.txt)
* [An MS Word document as text file](example/word.txt)

## Usage

### Installation

Clone this repository, go to the directory and install the Python with `pip` in a virtual environment:
```
python -m venv path/to/my/virtualenv
source path/to/my/virtualenv/bin/activate

python -m pip install -r requirements.txt
```

### Running

To run the translation from MS Word to latex citations with an [example](example):
```
python main.py example/references.bib example/word_bib.txt example/word.txt example/latex.tex
```

For help:
```
python main.py -h
usage: main.py [-h] bibtex text_file input_file output_file

positional arguments:
  bibtex       BibTex file including all references
  text_file    Text file containing the Bibliography from Word
  input_file   Input text file containing MS Word text with IEEE reference style e.g., [0]
  output_file  Output text file containing text with latex compatible citation e.g., \cite{mueller2022}

optional arguments:
  -h, --help   show this help message and exit
```

## Output

The output file is written to the user-provided location. The example from above generates the following text file:
```
Lorem ipsum dolor sit amet \cite{bibtex2021}, consectetur adipiscing elit. Morbi quis bibendum massa, vel volutpat quam. Aliquam tristique velit non arcu euismod tempus. Nullam placerat porttitor arcu, a venenatis augue malesuada vel \cite{mueller2023}. Pellentesque interdum felis at eros suscipit, vel molestie lectus tempus. Vivamus in varius lorem, ut interdum lacus. Morbi hendrerit mi et lacinia varius. Nam et auctor magna. Suspendisse sed metus leo. Pellentesque eleifend ligula arcu, ac luctus nisi euismod malesuada. Nam porta ex id diam dapibus finibus. Etiam vel tellus lacus. Curabitur rhoncus neque iaculis erat ullamcorper, sed venenatis neque egestas. Cras lobortis elit a metus aliquet feugiat.
```
