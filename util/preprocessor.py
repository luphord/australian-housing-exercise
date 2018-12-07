from nbconvert.preprocessors import Preprocessor
import re


class CustomPreprocessor(Preprocessor):
    '''Custom preprocessor for replacing links to other .ipynb file by a .html extension
       when converting notebooks using nbconvert.
    '''

    def preprocess_cell(self, cell, resources, index):

        if 'source' in cell and cell.cell_type == "markdown":
            cell.source = re.sub(r"\[([^]]*)\]\(([^)]*)\.ipynb\)",r"[\1](\2.html)",cell.source)

        return cell, resources
