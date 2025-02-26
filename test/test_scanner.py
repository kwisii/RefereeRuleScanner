import os
import unittest
import genanki
from parameterized import parameterized

from src.Scanner.ScannerBFV import ScannerBFV
from src.Scanner.ScannerDFB import ScannerDFB

class TestScanner(unittest.TestCase):

    def setUp(self):
        self.deck = genanki.Deck(1, 'Tests')
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.bfv_rule_set_dir = os.path.join(current_directory, "test_pdfs_bfv")
        self.dfb_rule_set_dir = os.path.join(current_directory, "test_pdfs_dfb")

    @parameterized.expand([
        ["Regel+1.pdf", 11],
        ["Regel+2.pdf", 6],
        ["Regel+3.pdf", 50],
        ["Regel+4.pdf", 27],
        ["Regel+5.pdf", 61],
        ["Regel+6.pdf", 35],
        ["Regel+7.pdf", 15],
        ["Regel+8.pdf", 15],
        ["Regel+9.pdf", 12],
        ["Regel+10.pdf", 11],
        ["Regel+11.pdf", 41],
        ["Regel+12.pdf", 110],
    ])
    def test_bfv_verify_qa_number(self, filename, expected_number) -> None:
        """ This test verifies whether the number of generated question-answer pairs matches the expected count"""
        bfv_scanner = ScannerBFV(os.path.join(self.bfv_rule_set_dir, filename))
        bfv_scanner.parse_questions_and_answers()
        assert len(bfv_scanner.get_qa_pairs()) == expected_number

    @parameterized.expand([
        ["dfb_01_2024.pdf", 15],
        ["dfb_02_2024.pdf", 15],
        ["dfb_03_2024.pdf", 15],
        ["dfb_04_2024.pdf", 15],
        ["dfb_05_2024.pdf", 15],
        ["dfb_06_2024.pdf", 15],
        ["dfb_01_2025.pdf", 15],
        ["dfb_02_2025.pdf", 15],
    ])
    def test_bfv_verify_qa_number(self, filename, expected_number) -> None:
        """ This test verifies whether the number of generated question-answer pairs matches the expected count"""
        dfb_scanner = ScannerDFB(os.path.join(self.dfb_rule_set_dir, filename))
        dfb_scanner.parse_situations_and_answers()
        assert len(dfb_scanner.get_qa_pairs()) == expected_number