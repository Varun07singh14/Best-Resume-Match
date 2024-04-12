FROM --platform=linux/amd64 python:3.12-slim as build

WORKDIR /app

RUN pip install Flask google-cloud-storage PyPDF2 transformers 
RUN pip install spacy
RUN pip install -U pip setuptools wheel
RUN python -m spacy download en_core_web_sm
RUN pip install python-docx
RUN pip install fuzzywuzzy
RUN pip install nltk
RUN pip install torch --default-timeout=1000

# RUN python -m spacy download en_core_web_sm

# RUN python -m spacy download en

COPY . .

EXPOSE 8080

CMD [ "python", "resumeapi.py"]
