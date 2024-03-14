from pathlib import Path

from dotenv import load_dotenv

from kotaemon.loaders import AdobeReader

input_file = Path(__file__).parent / "resources" / "multimodal.pdf"

load_dotenv()


def test_adobe_reader():
    reader = AdobeReader()
    documents = reader.load_data(input_file)
    table_docs = [doc for doc in documents if doc.metadata.get("type", "") == "table"]
    assert len(table_docs) == 2

    figure_docs = [doc for doc in documents if doc.metadata.get("type", "") == "image"]
    assert len(figure_docs) == 2
