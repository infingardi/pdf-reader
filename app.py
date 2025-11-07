import os, io, json, time, asyncio
from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pypdf import PdfReader
from openai import AsyncOpenAI
from dotenv import load_dotenv
import diskcache as dc
from extractors.regex_extractor import extract_with_regex
from extractors.llm_extractor import extract_with_llm

load_dotenv()
app = FastAPI(title="PDF Data Extractor")
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
cache = dc.Cache("./cache")

pages = Jinja2Templates(directory="pages")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return pages.TemplateResponse("index.html", {"request": request})

@app.post("/extract_dataset")
async def extract_dataset(files: list[UploadFile]):
    async def event_stream():
        dataset_file = next((f for f in files if f.filename.endswith("dataset.json")), None)
        if not dataset_file:
            yield "data: {\"erro\": \"Arquivo dataset.json não encontrado.\"}\n\n"
            return

        dataset = json.load(dataset_file.file)
        pdf_map = {os.path.basename(f.filename): f for f in files if f.filename.endswith(".pdf")}

        total = len(dataset)
        yield f"data: {{\"status\": \"Iniciando processamento de {total} PDFs\"}}\n\n"

        for i, entry in enumerate(dataset, start=1):
            label = entry["label"]
            schema = entry["extraction_schema"]
            pdf_path = entry["pdf_path"]

            start = time.time()
            if pdf_path not in pdf_map:
                yield f"data: {{\"arquivo\": \"{pdf_path}\", \"erro\": \"PDF não encontrado.\"}}\n\n"
                continue

            pdf = pdf_map[pdf_path]
            pdf_reader = PdfReader(io.BytesIO(await pdf.read()))
            text = pdf_reader.pages[0].extract_text()

            cache_key = f"{label}_{pdf.filename}_{hash(text)}_{hash(str(schema))}"
            if cache_key in cache:
                result = cache[cache_key]
            else:
                result = await extract_with_llm(client, text, schema)
                cache[cache_key] = result

            elapsed = round(time.time() - start, 2)
            payload = {
                "arquivo": pdf.filename,
                "resultado": result,
                "tempo_execucao": elapsed,
                "progresso": f"{i}/{total}"
            }
            yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
            await asyncio.sleep(0.1)

        yield "data: {\"status\": \"Processamento concluído\"}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
