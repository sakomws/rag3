import argparse
from unstructured.partition.pdf import partition_pdf

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Partition a PDF using Unstructured.')
    parser.add_argument('filename', type=str, help='The path to the PDF file to be processed.')
    
    args = parser.parse_args()
    
    # Partition the PDF document into elements
    elements = partition_pdf(filename=args.filename)
    
    # Print out the elements to see the structure
    for element in elements:
        print(element)

if __name__ == "__main__":
    main()

