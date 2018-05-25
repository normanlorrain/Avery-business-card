# Create a printable PDF of business cards
# Automatically places original in repeated, tiled locations.

from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.pdf import PageObject
import argparse

# Note: All measurements in Points.
PPI = 72 # Points Per Inch
CARD_WIDTH = 3.5 * PPI
CARD_HEIGHT = 2 * PPI
PAGE_WIDTH = 8.5 * PPI
PAGE_HEIGHT = 11 * PPI

# Avery paper is 2 x 5 tiles.
PRINTED_WIDTH = CARD_WIDTH * 2
PRINTED_HEIGHT = CARD_HEIGHT * 5
MARGIN_X = (PAGE_WIDTH - PRINTED_WIDTH) / 2
MARGIN_Y = (PAGE_HEIGHT - PRINTED_HEIGHT) / 2


parser = argparse.ArgumentParser(
    description='Build a PDF printable to Avery *8873 paper.  Tested with 38873.'
)
parser.add_argument("input", help="input PDF")
parser.add_argument("output", help="output PDF")
args = parser.parse_args()


def createOutput(infileName, outfileName):
    # Get the one and only page of our input.
    pdfInput = PdfFileReader( open(infileName, "rb"))
    card = pdfInput.pages[0]

    # Starting with a clean page, merge the input PDF at every tiled location
    tilePage = PageObject.createBlankPage(None, width = 612, height = 792)
    for x in range(2):
        for y in range(5):
            print(f'tiling {x}, {y}')
            tilePage.mergeTranslatedPage(card, MARGIN_X + x * CARD_WIDTH, 
                                            MARGIN_Y + y * CARD_HEIGHT )

    pdfOutput = PdfFileWriter()
    pdfOutput.addPage(tilePage)
    pdfOutput.write(open(outfileName, "wb"))


createOutput(args.input, args.output)
print('Done')