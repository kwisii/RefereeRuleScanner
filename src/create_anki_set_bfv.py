import os
import random
from ScannerBFV import ScannerBFV
import genanki


if __name__ == "__main__":

    # Generate Anki Deck
    deck = genanki.Deck(random.randrange(1 << 30, 1 << 31), 'Regelfragen aus dem Regeltool')

    # Set path to BFV pdfs
    current_directory = os.path.dirname(os.path.abspath(__file__))
    bfv_rule_set_dir = os.path.join(current_directory, "..", "pdfs_bfv")

    # Scan each file for question and ansers
    for filename in os.listdir(bfv_rule_set_dir):
        if filename.endswith(".pdf"):
            bfv_scanner = ScannerBFV(os.path.join(bfv_rule_set_dir, filename))
            bfv_scanner.parse_questions_and_answers()

        # Add each question answer pair into Anki Note and Deck
        for qa_pair in bfv_scanner.get_qa_pairs():
            deck.add_note(bfv_scanner.create_note(qa_pair))

    # Write Anki package
    genanki.Package(deck).write_to_file('Blaues_Buch.apkg')