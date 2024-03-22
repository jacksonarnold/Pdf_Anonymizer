import textract
import re
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine


def anonymize_pdf(pdf_path):
    text = textract.process(pdf_path, method="pdfminer")

    # Remove null characters
    textstring = text.decode("utf-8")
    textstring = textstring.replace("\0", "")
    textstring = textstring.replace("_", " ")

    # Remove non-printable characters
    textstring = re.sub(r"[^\x20-\x7e]", "", textstring)

    print(textstring)

    print("=====================================")
    print("Anonymizing sensitive data in the PDF")
    print("=====================================\n\n")

    # Initialize Presidio analyzer and anonymizer
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()

    # Analyze the text to identify sensitive data
    analyzer_results = analyzer.analyze(text=textstring, language="en")

    # Anonymize the sensitive data
    anonymized_text = anonymizer.anonymize(
        text=textstring, analyzer_results=analyzer_results
    )

    return anonymized_text


# Example usage
pdf_path = "PARTNERSHIP_AGREEMENT.pdf"
anonymized_text = anonymize_pdf(pdf_path)
print(anonymized_text)
