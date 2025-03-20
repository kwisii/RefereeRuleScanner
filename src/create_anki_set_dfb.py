import os
import random
from Scanner.ScannerDFB import ScannerDFB
import genanki


if __name__ == "__main__":

    # Generate Anki Deck
    deck = genanki.Deck(random.randrange(1 << 30, 1 << 31), 'Regelfragen aus den DFB-Magazinen')

    # Set path to DFB magazine pdfs
    current_directory = os.path.dirname(os.path.abspath(__file__))
    dfb_rule_set_dir = os.path.join(current_directory, "..", "pdfs_dfb")

    # Scan each file for question and ansers
    for filename in os.listdir(dfb_rule_set_dir):
        if filename.endswith(".pdf"):
            dfb_scanner = ScannerDFB(os.path.join(dfb_rule_set_dir, filename))
            dfb_scanner.parse_situations_and_answers()

        # Add each question answer pair into Anki Note and Deck
        for qa_pair in dfb_scanner.get_qa_pairs():
            deck.add_note(dfb_scanner.create_note(qa_pair))

    # Write Anki package
    genanki.Package(deck).write_to_file('DFB_Fragen.apkg')