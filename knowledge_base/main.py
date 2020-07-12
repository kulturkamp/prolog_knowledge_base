# This is a simple program that creates a knowledge base from Prolog file and user`s queries.
# Each fact and rule in the file MUST begin from a new line.
# NOTE! Any lines in the Prolog file which are not facts or rules (including comments) is assumed "corrupted"
# and won`t be parsed.

import os
import re
import json
from pyswip import Prolog
from collections import defaultdict

# Knowledge base to create
knowledgeBase = defaultdict(list)

# Prolog Query handler for Python
prolog = Prolog()

# Consulting Prolog code and parsing it into sets of facts and rules respectively
while True:
    filename = input("Enter a name of a prolog file to parse: ")
    if filename == "done":
        break
    try:
        with open(os.path.join(os.getcwd(), filename)) as f:
            prolog.consult(filename)
            line = f.readline()
            while line:
                # regex for fact in Prolog
                if re.match("^[A-Za-z0-9]+\(([A-Za-z0-9]*\,)*([A-Za-z0-9])*\).$", line.replace("\n", '').replace(" ", '')):
                    knowledgeBase["F"].append(line.replace("\n", '').replace(" ", ''))
                # regex for rule in Prolog
                elif re.match("^[A-Za-z0-9]+\(([A-Za-z0-9]*\,)*([A-Za-z0-9])*\)\:\-((.+),)*(.)*\.$", line.replace("\n", '').replace(" ", '')):
                    knowledgeBase["R"].append(line.replace("\n", '').replace(" ", ''))
                else:
                    if line != '\n':
                        print("Attention! Corrupted line! Quarries might work incorrectly!")
                line = f.readline()

        # Handling user`s query and adding it to a set of procedures
        while True:
            query = input("Enter Prolog query for chosen file: ")
            if query == "done":
                print(json.dumps(knowledgeBase, indent=1))
                knowledgeBase.clear()
                break
            try:
                if not bool(list(prolog.query(query))):
                    print("No")
            except:
                print("Query is not correct")
                continue
            knowledgeBase["P"].append(query)
            for q in prolog.query(query):
                if not q:
                    print("Yes")
                else:
                    print(q)
    except FileNotFoundError:
        print("File {} does not exist".format(filename))
