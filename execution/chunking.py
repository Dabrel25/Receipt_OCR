import os

from docling.chunking import HybridChunker
from dotenv import load_dotenv
from openai import OpenAI
from tokenizer import OpenAITokenizerWrapper

from extraction import result

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tokenizer = OpenAITokenizerWrapper()
MAX_TOKENS = 8191

chunker = HybridChunker(
    tokenizer = tokenizer,
    max_tokens = MAX_TOKENS,
    merge_peers = True
)

chunk_iter = chunker.chunk(dl_doc = result.document)
chunks = list(chunk_iter)
