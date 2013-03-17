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
