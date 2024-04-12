from transformers import BertTokenizer, BertModel
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import torch
import spacy
import torch

nltk.download('punkt')
nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm")

def score_resumes(prompt, all_resume_texts, threshold):
    prompt_tokens = word_tokenize(prompt.lower())
    prompt_tokens = [token for token in prompt_tokens if token.isalnum() and token not in stopwords.words('english')]
    prompt_processed = ' '.join(prompt_tokens)
    
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    
    prompt_input = tokenizer(prompt_processed, return_tensors='pt', padding=True, truncation=True)
    
    with torch.no_grad():
        outputs = model(**prompt_input)
        prompt_embedding = outputs.last_hidden_state.mean(dim=1)
        
    similarities = []
    for item in all_resume_texts:
        id, resume_text, path = item
        resume_tokens = word_tokenize(resume_text.lower())
        resume_tokens = [token for token in resume_tokens if token.isalnum() and token not in stopwords.words('english')]
        resume_processed = ' '.join(resume_tokens)

        resume_input = tokenizer(resume_processed, return_tensors='pt', padding=True, truncation=True)

        with torch.no_grad():
            outputs = model(**resume_input)
            resume_embedding = outputs.last_hidden_state.mean(dim=1)


        similarity = torch.nn.functional.cosine_similarity(prompt_embedding, resume_embedding)
        similarities.append([id,similarity,path])
        
        """ prompt_entities = [ent.text for ent in nlp(prompt).ents]

    scores = []
    max_similarity = max(similarities)
    if max_similarity != 0:
        score = [similarity / max_similarity for similarity in similarities]
        scores.append(score)
    else:
        score = [0] * len(similarities)
        scores.append(score) """

    #for similarity, resume_text in zip(similarities, all_resume_texts):
        
        #resume_entities = [ent.text for ent in nlp(resume_text).ents]

        #score = similarity * (len(set(prompt_entities) & set(resume_entities)) / len(prompt_entities))
        #scores.append(score)
    max_score = float('-inf')
    for row in similarities:
        tensor_element = row[1]
        score_value = float(tensor_element.item())
        max_score = max(max_score, score_value)

# Normalize the scores

    filtered_data = []
    for row in similarities:
        tensor_element = row[1]
        score_value = float(tensor_element.item())
        normalized_score = score_value / max_score if max_score != 0 else 0
        if normalized_score >= threshold:
            scored_resumes = [{'score': normalized_score, 'id': row[0], 'path':row[2]}]
            row[1] = normalized_score
            filtered_data.append(scored_resumes)
        
        
    #max_similarity = max(similarities)
    #normalized_scores = [similarity / max_similarity if max_similarity != 0 else 0 for similarity in similarities]

    return filtered_data
