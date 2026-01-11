from .utils import clean_text
from .indexing import index_text_file
from .storage import save_index, load_index

__all__ = ["clean_text", "index_text_file", "save_index", "load_index"]

def hello_world():
    return "rag_service OK"

