import os
import random
from ScannerBFV import ScannerBFV
import genanki


if __name__ == "__main__":

    deck = genanki.Deck(
        random.randrange(1 << 30, 1 << 31),
        'Regelfragen aus dem Regeltool')

    qa_pairs = []
    current_directory = os.path.dirname(os.path.abspath(__file__))
    bfv_rule_set_dir = os.path.join(current_directory, "pdfs_bfv")
    for filename in os.listdir(bfv_rule_set_dir):
        if filename.endswith(".pdf"):
            bfv_scanner = ScannerBFV(os.path.join(bfv_rule_set_dir, filename))
            bfv_scanner.parse_questions_and_answers()

        for qa_pair in bfv_scanner.get_qa_pairs():
            note = genanki.Note(
                model = genanki.Model(
                    random.randrange(1 << 30, 1 << 31),
                    'Simple Model',
                    fields=[
                        {'name': 'Question'},
                        {'name': 'Answer'},
                    ],
                    templates=[
                        {
                        'name': 'Card 1',
                        'qfmt': '{{Question}}',
                        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
                        },
                    ]),
                fields=qa_pair,
                tags = bfv_scanner.get_tags())
            
            deck.add_note(note)

    genanki.Package(deck).write_to_file('Blaues_Buch.apkg')