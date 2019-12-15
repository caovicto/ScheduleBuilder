# importing parsing modules
import collections

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

def parse_pdf(file_name):
    print(results.text)
    for ele in results:
        print(ele.get_attribute("innerHTML"))

    time.sleep(3)

    for ele in select:
        print(ele)
    select.select_by_visible_text(c_code)

    results = driver.find_elements_by_xpath("//*[@id='MainContent_divSearchResults']")
    # print(results)
    for ele in results:
        print(ele.text)



    # variables for file scraping
    document = open(file_scrape, 'rb')

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # variables

    window = collections.deque()

    # loop for each line in file
    for pg in PDFPage.get_pages(document):
        interpreter.process_page(pg)
        layout = device.get_result()
        waiting = ["|", "/", "-", "\\"]

        ind = 0

        for ele in layout:
            # sys.stdout.write(waiting[ind])
            # sys.stdout.flush()
            # ind = (ind+1) % 4
            if isinstance(ele, LTTextBoxHorizontal):
                # splitting by line
                for line in ele.get_text().split('\n'):
                    window.append(line)

        while window:
            # sys.stdout.write(waiting[ind])
            # sys.stdout.flush()
            # ind = (ind+1) % 4

            pop = window.popleft()

