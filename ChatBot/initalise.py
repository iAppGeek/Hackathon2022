import glob
import os
import ssl

import nltk

for f in glob.glob("*.db*"):
    os.remove(f)
    print("Deleted existing db files")

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')