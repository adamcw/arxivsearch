# Whether or not you use BibDesk to handle your references (will automatically
# export BibTex references into the currently open BibDesk bilbiography)
USE_BIBDESK = True

# The default categories to search if no other categories are specified
DEFAULT_CATEGORIES = ['quant-ph']

# Whether or not to include the abstract in exported BibTex references
INC_ABSTRACT = True

# The number of results to return if no number is specified
DEFAULT_LIMIT = 100

# The software to use to 'open' a URL. Try "open" for OSX, "gnome-open" for
# Linux or "cmd /c start" for Windows. Commands for your specific setup may
# need to be determined.
OPEN_SOFTWARE = "open"

# A Python .format() string representing how results will be formatted
OUTPUT_FORMAT = "{i:<6} {date} ({arxiv_id}) | {score} | {cate} | {mark}{title}{mark}"

# Keywords to look for in titles and abstracts, used for scoring articles
KEYWORDS = {
    'topological': 10, 
    'qubit': 5, 
    'qec': 20,
    'tqec': 20,
    'ftqc': 20,
    'ftqec': 20,
    'fault tolerant': 25,
    'error correction': 20,
    'error': 5,
    'surface code': 20,
    'code': 10, 
    'circuit': 15,
    'quantum computing': 15,
    'computer': 15, 
    'lower': 5,
    'distillation': 4,
    'threshold': 6, 
    'cluster state': 15,
    'error rate': 10,
    'classical processing': 15,
    'ion trap': 10,
    'scalability': 8, 
    'scalable': 8, 
    'stabiliser': 15,
    'minimum weight': 25,
    'perfect matching': 25,
    'gate': 10,
    'cnot': 15,
    'shor': 20, 
    'pauli': 20,
    'clifford': 20,
    'toffoli': 20,
    'grover': 20, 
    'algorithm': 20,
    'hadamard': 10, 
    'unitary': 5,
    'logical qubit': 15,
    'logical': 7,
    'nearest neighbour': 15, 
    'nearest neighbor': 15, 
}
