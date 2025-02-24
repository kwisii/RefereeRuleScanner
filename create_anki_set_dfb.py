import os
import random
from ScannerDFB import ScannerDFB
import genanki


if __name__ == "__main__":

    deck = genanki.Deck(
        random.randrange(1 << 30, 1 << 31),
        'Regelfragen aus den DFB-Magazinen')

    current_directory = os.path.dirname(os.path.abspath(__file__))
    dfb_rule_set_dir = os.path.join(current_directory, "pdfs_dfb")
    for filename in os.listdir(dfb_rule_set_dir):
        if filename.endswith(".pdf"):
            dfb_scanner = ScannerDFB(os.path.join(dfb_rule_set_dir, filename))
            dfb_scanner.parse_situations_and_answers()

        for qa_pair in dfb_scanner.get_qa_pairs():
            note = genanki.Note(
                model = genanki.Model(
                    random.randrange(1 << 30, 1 << 31),
                    'Simple Model',
                    fields=[
                        {'name': 'Question'},
                        {'name': 'Answer'}
                    ],
                    templates=[
                        {
                        'name': 'Card 1',
                        'qfmt': '{{Question}}',
                        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
                        },
                    ]),
                fields = [qa_pair[0], qa_pair[1]],  # 0: situation, 1: answer
                tags = dfb_scanner.get_tags())
            
            deck.add_note(note)

    genanki.Package(deck).write_to_file('DFB_Fragen.apkg')