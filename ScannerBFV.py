import os
import re
import fitz

class ScannerBFV:

    def __init__(self, pdf_file: str):
        self.pdf_path = pdf_file
        self.tag = [os.path.basename(pdf_file).removesuffix(".pdf")]
        self.qa_pairs = []
    
    def get_tags(self) -> list:
        return self.tag
    
    def get_qa_pairs(self) -> list:
        return self.qa_pairs

    def _extract_text_with_colors(self):
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
                            
                            if "Regelfragen-Auszug" in text:
                                start_extracting = True
                                continue
                            
                            if start_extracting:
                                extracted_data.append((text, color))
        
        return extracted_data

    def parse_questions_and_answers(self):
        question = ""
        answer = ""
        black_color = 0 
        green_color = 65280
        
        is_question = False
        
        for text, color in self._extract_text_with_colors():
            if re.match(r"Frage \d+", text):
                if question and answer:
                    self.qa_pairs.append((question.strip(), answer.strip()))
                    question = ""
                    answer = ""
                is_question = True
                continue

            if color == green_color:
                is_question = False
            
            if is_question and color == black_color:
                question += text + " "
            elif not is_question and color == green_color:
                answer += text + " "
            
        if question and answer:
            self.qa_pairs.append((question.strip(), answer.strip()))
