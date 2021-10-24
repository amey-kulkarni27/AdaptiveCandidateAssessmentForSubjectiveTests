# # import PyPDF2

# # # creating an object 
# # file = open('../../SS_10.pdf', 'rb')

# # # creating a pdf reader object
# # fileReader = PyPDF2.PdfFileReader(file)

# # # print the number of pages in pdf file
# # print(fileReader.numPages)

# from tika import parser # pip install tika

# raw = parser.from_file('../../SS_10.pdf')
# print(raw['content'][30000:60000])

import pdfplumber


x0 = 0    # Distance of left side of character from left side of page.
x1 = 0.5  # Distance of right side of character from left side of page.
y0 = 0  # Distance of bottom of character from bottom of page.
y1 = 1  # Distance of top of character from bottom of page.

all_content = []
with pdfplumber.open("../../SS_10.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        width = page.width
        height = page.height

        # Crop pages
        left_bbox = (x0*float(width), y0*float(height), x1*float(width), y1*float(height))
        page_crop = page.crop(bbox=left_bbox)
        left_text = page_crop.extract_text()

        left_bbox = (0.5*float(width), y0*float(height), 1*float(width), y1*float(height))
        page_crop = page.crop(bbox=left_bbox)
        right_text = page_crop.extract_text()
        page_context = '\n'.join([left_text, right_text])
        all_content.append(page_context)
        if i < 2:
            print(page_context)