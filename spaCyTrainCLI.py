# #.txt import

# with open ("./Data/Dataset.txt", "r") as f:
#     text =  f.read()
#     chapters = text.split("CHAPTER ") [1:]

# __________________________________________

#Creating training data

# import json
# import spacy
# from spacy.matcher import Matcher
# from spacy.tokens import Span, DocBin

# with open("dataset.udt.json", encoding="utf8") as f:
#     TEXTS = json.loads(f.read())

# nlp = spacy.blank("en")
# matcher = Matcher(nlp.vocab)
# # Add patterns to the matcher
# pattern1 = ([{"LOWER": "iphone"}, {"LOWER": "x"}])
# pattern2 = [{"LOWER": "iphone"}, {"IS_DIGIT": True}]
# matcher.add("GADGET", [pattern1, pattern2])
# docs = []
# for doc in nlp.pipe(TEXTS):
#     matches = matcher(doc)
#     spans = [Span(doc, start, end, label=match_id) for match_id, start, end in matches]
#     doc.ents = spans
#     docs.append(doc)

# doc_bin = DocBin(docs=docs)
# doc_bin.to_disk("./train.spacy")

# _______________________________________

# #Create config file

# python -m spacy init config ./config.cfg --lang en --pipeline ner

# ________________________________________

# #Training model

python -m spacy train ./config.cfg --output ./output --paths.train ./Data/data.spacy # --paths.dev ./exercises/en/dev_gadget.spacy