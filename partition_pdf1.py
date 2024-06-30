import argparse
import os
from unstructured.partition.pdf import partition_pdf
from unstructured.ingest.v2.processes.connectors.astra import (
    AstraUploaderConfig,
    AstraConnectionConfig,
    AstraAccessConfig,
    AstraUploadStagerConfig,
)

def partition_and_upload(filepath, astra_uploader):
    # Partition the PDF document into elements
    elements = partition_pdf(filename=filepath, strategy='hi_res')

    # Print out the elements to see the structure
    for element in elements:
        print(f"File: {filepath}")
        print(element)

    # Assuming elements need to be uploaded to Astra
    astra_uploader.upload(elements)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Partition PDFs in a folder and upload to Astra.')
    parser.add_argument('folder', type=str, help='The path to the folder containing PDF files to be processed.')

    args = parser.parse_args()
    folder_path = args.folder

    # Check if the folder exists
    if not os.path.isdir(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return

    # Configure Astra connection
    # Configure Astra connection
    astra_connection_config = AstraConnectionConfig(
        access_config=AstraAccessConfig(
            token=os.getenv("ASTRA_DB_TOKEN"), 
            api_endpoint=os.getenv("ASTRA_DB_ENDPOINT")
        )
    )
    
    astra_stager_config = AstraUploadStagerConfig()
    
    astra_uploader = AstraUploaderConfig(
        collection_name=os.getenv("COLLECTION_NAME"),
        embedding_dimension=int(os.getenv("EMBEDDING_DIMENSION")),
        requested_indexing_policy={"deny": ["metadata"]},
    )


    # Process each PDF file in the folder
    for filename in os.listdir(folder_path):
        print(filename)
        if filename.endswith('.pdf'):
            filepath = os.path.join(folder_path, filename)
            partition_and_upload(filepath, astra_uploader)

if __name__ == "__main__":
    main()

