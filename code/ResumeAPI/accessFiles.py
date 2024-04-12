from ast import And
from google.cloud import storage
import re
import extract_pdf_text
import score_resume
import read_doc_jd
import os

def verify_Access_To_Cloud_Storage_And_Return_Files(bucket_name, mlEvaluateRequest):
    noOfmatches = mlEvaluateRequest.get('noOfmatches',None), 
    threshold = mlEvaluateRequest["threshold"]
    context = mlEvaluateRequest["context"]
    category = mlEvaluateRequest["category"]
    
    storage_client = storage.Client.create_anonymous_client()
    bucket = storage_client.bucket(bucket_name)

    blobs = bucket.list_blobs()
    all_resume_texts = []
    all_job_descriptions =[]
    base_file_names =[]
    file_infos =[]
    for blob in blobs:
        if (blob.name.endswith('.pdf') and category == "resume"):
            """Logic for resume related models """

            all_resume_texts.append([blob.name[:blob.name.rfind(".")],extract_pdf_text.extract_text_from_file(blob),blob.media_link] )

            
            print(f"File Name for Resume: {blob.name} ")

        if (blob.name.endswith('.docx') and category == "job"):
            """Logic for job description """
            
            file_infos.append(read_doc_jd.extract_data_from_doc(blob, all_job_descriptions, base_file_names))
            print(f"File Name for Job Description: {blob.name} ")
    
    if(category == "job"):
        flattened_data = read_doc_jd.score_documents(context,all_job_descriptions,threshold,file_infos)
        return flattened_data[:noOfmatches[0]]
    if(category == "resume"):
        scores = score_resume.score_resumes(context, all_resume_texts, threshold)
        flattened_data = [entry[0] for entry in scores]
        return sorted(flattened_data, key=lambda x: x['score'], reverse=True)[:noOfmatches[0]]
    return [{"status":"No Match"}]

def Extract_Bucket_Name_From_Input_Path(input_path):

    pattern = r"^(?:https?://)?console.cloud.google.com/storage/browser/([^/]+)/?"
    match = re.match(pattern, input_path)
    if match:
        return match.group(1)
    else:
        return None


if __name__ == "__main__":

    bucket_name = Extract_Bucket_Name_From_Input_Path(
        "https://console.cloud.google.com/storage/browser/hackathontestdata2024")

    """ https://console.cloud.google.com/storage/browser/hackathon1415 """

    scores = verify_Access_To_Cloud_Storage_And_Return_Files(bucket_name)
    flattened_data = [item for sublist in scores for item in sublist]
    print(flattened_data)

    """ Golden Data Set :https://console.cloud.google.com/storage/browser/hackathon1415/RESUME
    Final code will be tested against this set of data 
    """
