import boto3
import botocore

import constants

from dotenv import load_dotenv

from langchain_aws import ChatBedrock
from langchain_community.vectorstores import FAISS
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings

import os

import re

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

AWS_ACCESS_KEY_ID = os.getenv ("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv ("AWS_SECRET_ACCESS_KEY")

REGION = os.getenv ("REGION")
SQL_MODEL = os.getenv ("SQL_MODEL")
FINAL_MODEL = os.getenv ("FINAL_MODEL")

def get_bedrock_client():
    bedrock_config = botocore.config.Config(read_timeout=900, connect_timeout=900, region_name=REGION)
    return boto3.client(
        service_name = "bedrock-runtime",
        config=bedrock_config,
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )

def generate_few_shot_prompt (query):
    try:
        local_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        example_selector = SemanticSimilarityExampleSelector.from_examples(
            constants.EXAMPLES,
            local_embeddings,
            FAISS,
            k=3,
            input_keys=["input"]
        )

        example_prompt = PromptTemplate.from_template("User input: {input}\nSQL query: {query}")

        prompt = FewShotPromptTemplate(
                example_selector=example_selector,
                example_prompt=example_prompt,
                prefix=constants.FEW_SHOT_PREFIX,
                suffix="User input: {input}\nSQL query: ",
                input_variables=["input", "top_k", "table_info"],
            )

        return prompt.format(input=query, top_k=5, table_info=constants.TABLE_INFO)
    except Exception as e:
        raise e

def get_sql_query_response (prompt):
    llm_sql = ChatBedrock (
        client=get_bedrock_client (),
        model=SQL_MODEL,
        model_kwargs={"temperature": 0},
    )

    return llm_sql.invoke (prompt).content

def is_write_query(sql_query: str) -> bool:
    write_keywords = ['INSERT', 'UPDATE', 'DELETE', 'ALTER', 'DROP', 'CREATE', 'TRUNCATE', 'REPLACE']

    cleaned_query = re.sub(r'\s+', ' ', sql_query).strip().upper()

    for keyword in write_keywords:
        if re.search(rf'\b{keyword}\b', cleaned_query):
            return True

    return False

def query_db (sql_query):
    new_query = get_sql_query_response (constants.RECHECK_QUERY_PROMPT.format (table_info=constants.TABLE_INFO, query=sql_query))

    if (is_write_query (new_query)):
        return "No response."
    else:
        db = SQLDatabase.from_uri (f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

        return (db.run (new_query, include_columns=True))

def get_final_analysis (prompt):
    llm = ChatBedrock (
        client=get_bedrock_client(),
        model=FINAL_MODEL,
        model_kwargs={"temperature": 0.2}
    )

    return llm.invoke (prompt).content

def run_query_engine (query):
    prompt = generate_few_shot_prompt (query)

    sql_query = get_sql_query_response (prompt)
    print (sql_query)
    data = query_db (sql_query)

    analysis_prompt = constants.DATA_ANALYST_PROMPT.format (query=query, sql_query=sql_query, data=data)

    final_response = get_final_analysis (analysis_prompt)

    return final_response