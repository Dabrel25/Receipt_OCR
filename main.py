from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import shutil
import csv
from converter import parse_receipt_with_gpt


from docling.document_converter import DocumentConverter

app = FastAPI()
converter = DocumentConverter()
UPLOAD_DIR = "uploaded_files"
CSV_OUTPUT = "output.csv"
os.makedirs(UPLOAD_DIR, exist_ok=True)



@app.post("/upload")
async def upload_receipt(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # Save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Docling extraction
        result = converter.convert(file_path)
        document = result.document
        text = document.export_to_markdown()

        # Print extracted text
        print("📄 Extracted Text:\n", text)

        # Step 3: Parse with GPT
        receipt_data = parse_receipt_with_gpt(text)

        # Print parsed JSON
        print("🤖 Parsed Receipt:\n", receipt_data)

        with open(CSV_OUTPUT, mode='a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["merchant", "date", "item", "amount"])

            if not os.path.exists(CSV_OUTPUT):
                writer.writeheader()

            writer.writerow(receipt_data)


        return FileResponse(CSV_OUTPUT, media_type='text/csv', filename="receipt_output.csv")

    except Exception as e:
        return {"error": str(e)}
