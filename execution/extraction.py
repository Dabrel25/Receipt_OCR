from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("/Users/darrelong/Downloads/CaseStudy_Narrative.pdf")
document = result.document
# document format
md_result = document.export_to_markdown()

def extract_text(document):
    return document.export_to_markdown()

# Multiple files
result_files = converter.convert_all(["/Users/darrelong/Downloads/CaseStudy_Narrative.pdf", "/Users/darrelong/Downloads/CaseStudy_Narrative.pdf"])
docs = []
for result in result_files:
    if result.document:
        document = result.document
        docs.append(document)