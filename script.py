import textract
import re
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine


def anonymize_document(pdf_path, isPdf=True):
    textstring = ""

    if isPdf:
        textstring = read_pdf(pdf_path)
    else:
        textstring = read_text(pdf_path)

    print(textstring)

    print("=====================================")
    print("Anonymizing sensitive data in the PDF")
    print("=====================================\n\n")

    return anonymize_text(textstring)


def read_pdf(file_path):
    text = textract.process(pdf_path, method="pdfminer")

    # Remove null characters
    textstring = text.decode("utf-8")
    textstring = textstring.replace("\0", "")
    textstring = textstring.replace("_", " ")

    # Remove non-printable characters
    textstring = re.sub(r"[^\x20-\x7e]", "", textstring)

    return textstring


def read_text(file_path):
    with open(file_path, "r") as file:
        text = file.read()
    return text


def anonymize_text(text):
    # Initialize Presidio analyzer and anonymizer
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()

    # Analyze the text to identify sensitive data
    analyzer_results = analyzer.analyze(text=text, entities=["PERSON"], language="en")

    # Anonymize the sensitive data
    anonymized_text = anonymizer.anonymize(text=text, analyzer_results=analyzer_results)

    return anonymized_text


# Example usage
pdf_path = "PARTNERSHIP_AGREEMENT.pdf"
txt_path = "NonCompeteText.txt"
# anonymized_text = anonymize_document(pdf_path)
anonymized_text = anonymize_document(txt_path, False)
print(anonymized_text)
