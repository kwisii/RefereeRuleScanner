import os
import re
import fitz

class ScannerDFB:

    def __init__(self, pdf_file: str):
        self.pdf_path = pdf_file
        self.tag = [os.path.basename(pdf_file).removesuffix(".pdf")]
        self.qa_pairs = []
    
    def get_tags(self) -> list:
        return self.tag
    
    def get_qa_pairs(self) -> list:
        return self.qa_pairs

    def _extract_text_with_colors(self):
        """Extracts text and color information from a PDF file."""
        doc = fitz.open(self.pdf_path)
        extracted_data = []
        
        start_extracting = False
        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            color = span["color"]
                            
                            if "R E G E L-T E S T" in text:
                                start_extracting = True

                            if start_extracting:
                                extracted_data.append((text, color))

        return extracted_data

    def parse_situations_and_answers(self):
        """Parses situations and answers based on color and structure."""
        current_situation = ""
        current_question = ""
        answers = {}
        black_color = [1578774, 2301728]
        green_color = [1947530, 2403968]
        parsing_answers = False
        found_first_separator = False
        current_answer = ""
        current_situation_number = None

        for text, color in self._extract_text_with_colors():
            if "So werden die 15" in text:
                found_first_separator = True
                continue

            if found_first_separator and "richtig gelöst:" in text:
                parsing_answers = True
                self.qa_pairs.append((current_question.strip(), "", current_situation))
                continue

            if not parsing_answers:
                situation_match = re.match(r"S\s*I\s*T\s*U\s*A\s*T\s*I\s*O\s*N\s*(1[0-5]|[1-9])", text)
                if situation_match:
                    if current_question:
                        self.qa_pairs.append((current_question.strip(), "", current_situation))
                    current_situation = text.replace(" ", "")
                    current_question = ""
                    continue

                if black_color[0] <= color <= black_color[1] and current_situation:
                    current_question += " " + text
            else:
                match = re.match(r"(\d+):", text)
                if match:
                    if current_situation_number is not None and current_answer:
                        for idx, (question, answer, situation) in enumerate(self.qa_pairs):
                            situation_number_match = re.search(r"\d+", situation)
                            if situation_number_match and situation_number_match.group() == current_situation_number:
                                self.qa_pairs[idx] = (question, current_answer.strip(), situation)
                    current_situation_number = match.group(1)
                    current_answer = text[len(match.group(0)):].strip()
                elif green_color[0] <= color <= green_color[1]:
                    current_answer += " " + text.strip()

        if current_situation_number and current_answer:
            for idx, (question, answer, situation) in enumerate(self.qa_pairs):
                if situation.endswith(current_situation_number):
                    self.qa_pairs[idx] = (question, current_answer.strip(), situation)
                    