import argparse
import os
import shutil
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.schema.document import Document
from get_embedding_function import get_embedding_function
from langchain_community.vectorstores.chroma import Chroma

from luts import urls

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

CHROMA_PATH = "chroma"
DATA_PATH = "data"


def main():

    # Check if the database should be cleared (using the --clear flag).
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    documents = load_documents()
    # chunks = split_documents(documents)
    add_to_chroma(documents)


def load_documents():
    document_loader = DirectoryLoader(DATA_PATH, glob="**/*.csv", loader_cls=CSVLoader)
    return document_loader.load()


# def split_documents(documents):
#     headers_to_split_on = [
#         ("#", "Community"),
#         ("##", "Topic"),
#         ("###", "Subtopic"),
#     ]

#     text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on, strip_headers=True)
#     chunks = []
#     for doc in documents:
#         # split documents and add chunks to the list
#         chunks.extend(text_splitter.split_text(doc))

#     return chunks


def add_to_chroma(chunks: list[Document]):
    # load the existing database (or create a new one if it doesn't exist)
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    # add URLs
    chunks_with_ids = calculate_chunk_ids(chunks)

    db.add_documents(chunks_with_ids)
    db.persist()

    print("✅ Database populated!")

    # remove update functionality since we are not using unique IDs for each chunk

    # # Add or Update the documents.
    # existing_items = db.get(include=[])  # IDs are always included by default
    # existing_ids = set(existing_items["ids"])
    # print(f"Number of existing documents in DB: {len(existing_ids)}")

    # # Only add documents that don't exist in the DB.
    # new_chunks = []
    # for chunk in chunks_with_ids:
    #     if chunk.metadata["id"] not in existing_ids:
    #         new_chunks.append(chunk)

    # if len(new_chunks):
    #     print(f"👉 Adding new documents: {len(new_chunks)}")
    #     new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
    #     db.add_documents(new_chunks, ids=new_chunk_ids)
    #     db.persist()
    # else:
    #     print("✅ No new documents to add")


def calculate_chunk_ids(chunks):

    # This will add URLs to the metadata of each chunk.
    # These are not unique to each chunk, but that is OK - we just want to provide a reference to the source website.

    for chunk in chunks:
        # split the filename source to drop the "data/"prefix and " Temperature.csv" suffix
        loc_string = chunk.metadata["source"].split("/")[1].split(" Temp")[0]
        chunk.metadata["Location"] = loc_string
        chunk.metadata["URL"] = urls[loc_string]

    return chunks


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    main()
