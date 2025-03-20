# RefereeRuleScanner

This Python tool is helpful for football referees preparing for rule tests.
The Bavarian Football Association (BFV) continuously provides rule-related questions in its blue book.
This tool extracts these questions from the PDF files and converts them into a readable format for the flashcard tool Anki.
Additionally the questions from the dfb referee magazine will be extracted as well.

## Features

- Extracts rule-related questions and answers from PDFs ([BFV blue book](https://www.bfv.de/spielbetrieb-verbandsleben/schiedsrichter/schiedsrichter-regelwerk), [DFB referee magazine](https://www.dfb.de/training-service/schiedsrichterin/aktiver-schiedsrichter/schiedsrichter-zeitung))
- Stores the data in a Anki importable raw format (.apkg)
- Compatible with Anki for targeted learning using keywords

## Import learning cards into Anki

- Use the [GitHub Actions artefacts](https://github.com/kwisii/regelfragen/actions) to download the current question answer pairs and import it into Anki!

## Usage Maintainer

1. Clone this repository:
```
git clone https://github.com/kwisii/RefereeRuleScanner.git
cd RefereeRuleScanner
```

2. Install the required dependencies:
```
pip install pymupdf genanki
```

3. Simply execute the scripts:
```
python src/create_anki_set_bfv.py
python src/create_anki_set_dfb.py
```

This will generate ```Blaues_Buch.apkg``` and ```DFB_Fragen.apkg``` files containing all extracted questions and answers in a format ready for import into Anki.

## Future Features

- Additional export formats (e.g., GoodNotes)
- Direct Upload to Anki

Contributions and feature requests are welcome!