# COMP472 - Assignment 2
# Programmed By:
# Constantine Karellas - 40109253
# Max Burah - 40077075

import math
import string
import numpy as np
import random
from sklearn.feature_extraction.text import *
from sklearn.datasets import load_files
from sklearn import *
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import *
from collections import Counter
import matplotlib.pyplot as plt
import re
import pandas as pd

def read_documents(docName):
    docs = []
    label = []
    with open(docName, encoding="utf8") as f:
        for line in f:
            split_line = re.findall(r'\w+', line)
            label.append(split_line[1])
            docs.append(" ".join(split_line[4:]))
    return docs, label






print("\nProgram Terminated.\n")
