from tkinter import *
from pathlib import Path

from tkPDFViewer import tkPDFViewer as pdfViewer


help_file = Path("data/aide.pdf")


class WindowHelp(Toplevel):

    def __init__(self, *args, **kwargs):
        """Docstring"""
        super().__init__(*args, **kwargs)
        self.width = 600
        self.height = 1000
        self.geometry(f"{self.width}x{self.height}")
        self.title("Help")
        self.load_pdf()
    
    def load_pdf(self):
        v1 = pdfViewer.ShowPdf()
        # Adding pdf location and width and height.
        v2 = v1.pdf_view(self, pdf_location=help_file,
                        width=self.width, height=self.height)
        v2.pack()


if __name__ == '__main__':
    APP = WindowHelp()
    APP.mainloop()