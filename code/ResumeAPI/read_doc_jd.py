from docx import Document
import spacy
import io
import extract_pdf_text
from fuzzywuzzy import fuzz
from spacy.tokens import Span
from spacy.language import Language

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")
roles = []
# def main(file_names):
#     global roles
#     global nlp
#     nlp = spacy.load("en_core_web_sm")
#     roles = file_names
#     # Add the custom NER component to the pipeline
#     if "ner" in nlp.pipe_names:
#         ner = nlp.get_pipe("ner")
#         nlp.add_pipe("custom_ner", after="ner")
#     else:
#         raise ValueError("NER component not found in the pipeline.")

# @Language.component("custom_ner")
# def custom_ner(doc):
#     new_ents = []
#     token_indices = set()  # Keep track of token indices covered by entities
#     for ent in doc.ents:
#         token_indices.update(range(ent.start, ent.end))
#     for token in doc:
#         if token.i not in token_indices:  # Check if token is part of an existing entity
#             for role in roles:
#                 if token.text.lower() in role.lower():
#                     # Calculate the end index of the span
#                     end_idx = min(token.i + len(role.split()), len(doc))
#                     # Check if adding this role would cause overlapping spans
#                     if end_idx not in token_indices:
#                         span = Span(doc, token.i, end_idx, label="PERSON")
#                         new_ents.append(span)
#                         token_indices.update(range(token.i, end_idx))
#                     break  # Stop checking for other roles once a match is found
#     doc.ents = list(doc.ents) + new_ents
#     return doc

def perform_ner(text, prompt):
    """Perform Named Entity Recognition (NER) on the given text."""
    #main(file_names)
    doc = nlp(text)       
    entities = [ent.text for ent in doc.ents if ent.label_ == prompt]
    
    return entities

def score_document(doc_content, prompt,file_name):
    """Score the document based on the presence of entities matching the prompt."""
    entities = perform_ner(doc_content, prompt)
    score = len(entities) / len(doc_content.split())  # Normalize score to be between 0 and 1
    similarity_score = fuzz.partial_ratio(file_name.lower(), prompt.lower())
    score = similarity_score/100
    return score

def extract_data_from_doc(blob,scored_documents, file_names):
    blob_bytes = blob.download_as_string()
    with io.BytesIO(blob_bytes) as f:
            doc = Document(f)
            doc_content = extract_pdf_text.remove_unwanted_data_in_text('\n'.join([paragraph.text for paragraph in doc.paragraphs]))
            scored_documents.append(doc_content)
            file_names.append(blob.name[:blob.name.rfind(".")])
            file_info = {
                 'id': blob.name[:blob.name.rfind(".")],
                'score': 0,
                'path': blob.media_link
             }
    return file_info

def score_documents(prompt,scored_documents, threshold,file_infos):
    final_score_list=[]
    for doc_content,file_info in zip(scored_documents, file_infos):
        score = score_document(doc_content, prompt, file_info['id'])
        if score >= threshold:  # Apply threshold of 0.7
            file_info['score']= score
            final_score_list.append(file_info)

    sorted_documents = sorted(final_score_list, key=lambda x: x['score'], reverse=True)
    return sorted_documents



