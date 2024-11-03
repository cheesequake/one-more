import boto3
import botocore

import constants

from database_connection import connect_to_rds

from decimal import Decimal
from dotenv import load_dotenv

import json

from langchain_aws import ChatBedrock
from langchain_aws import ChatBedrockConverse
from langchain_community.vectorstores import FAISS
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
    """
    get_bedrock_client

    :return: A Boto3 Client with Bedrock Runtime
    """
    bedrock_config = botocore.config.Config(read_timeout=900, connect_timeout=900, region_name=REGION)
    return boto3.client(
        service_name = "bedrock-runtime",
        config=bedrock_config,
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )

def generate_few_shot_prompt (query):
    """
    generate_few_shot_prompt

    :param query: String containing user query
    :return: A prompt suitable for few shot prompting
    """
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
    """
    get_sql_query_response

    :param prompt: A prompt to be converted to an SQL Query
    :return: A prompt suitable for few shot prompting
    """
    llm_sql = ChatBedrock (
        client=get_bedrock_client (),
        model=SQL_MODEL,
        model_kwargs={"temperature": 0},
    )

    return llm_sql.invoke (prompt).content

def is_write_query(sql_query: str) -> bool:
    """
    is_write_query

    :param sql_query: String containing SQL query
    :return: Whether the generated SQL query doesn't change any data
    """
    write_keywords = ['INSERT', 'UPDATE', 'DELETE', 'ALTER', 'DROP', 'CREATE', 'TRUNCATE', 'REPLACE']

    cleaned_query = re.sub(r'\s+', ' ', sql_query).strip().upper()

    for keyword in write_keywords:
        if re.search(rf'\b{keyword}\b', cleaned_query):
            return True

    return 

def recheck_query (sql_query, exception):
    """
    recheck_query

    :param sql_query: String containing SQL query
    :param exception: Exception which occurred
    :return: An SQL query
    """
    new_query = get_sql_query_response(constants.RECHECK_QUERY_PROMPT.format(table_info=constants.TABLE_INFO, query=sql_query, exception=exception))

    return new_query

def query_db(sql_query):
    """
    query_db

    :param sql_query: String containing SQL query
    :return: A JSON string containing database response
    """
    if is_write_query(sql_query):
        return json.dumps({"response": "No response as write operations detected."})

    # Establish connection and run the query using a cursor
    connection = connect_to_rds()
    cursor = connection.cursor()

    try:
        # Execute the query and fetch results
        cursor.execute(sql_query)
        columns = [col[0] for col in cursor.description]  # Get column names
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert to list of dictionaries

    finally:
        # Ensure resources are closed
        cursor.close()
        connection.close()

    def make_json_serializable(data):
        if isinstance(data, list):
            return [make_json_serializable(item) for item in data]
        elif isinstance(data, dict):
            return {key: make_json_serializable(value) for key, value in data.items()}
        elif isinstance(data, Decimal):
            return float(data)
        elif hasattr(data, "isoformat"):
            return data.isoformat()
        else:
            return data

    # Make the result JSON serializable
    serializable_result = make_json_serializable(result)

    # Return the JSON-encoded string
    return json.dumps(serializable_result)

def get_final_analysis (prompt):
    """
    get_final_analysis

    :param prompt: A prompt to get the analysis of data from
    :return: A string containing LLM analysis
    """
    llm = ChatBedrockConverse (
        client=get_bedrock_client(),
        model=FINAL_MODEL,
        temperature=0.2,
        max_tokens=4096
    )

    return llm.invoke (prompt).content

def run_query_engine(query, team):
    """
    run_query_engine

    :param query: A user input from a front-end
    :return: Final output of the LLM(s)
    """
    prompt = generate_few_shot_prompt(query)
    sql_query = get_sql_query_response(prompt)
    rechecked_sql_query = sql_query
    print(sql_query)

    max_attempts = 5
    attempt = 0

    while attempt < max_attempts:
        try:
            data = query_db(rechecked_sql_query)
            break
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1

            if attempt == max_attempts:
                return {"error": "Query failed after multiple rechecking attempts."}

            rechecked_sql_query = recheck_query(rechecked_sql_query, str(e))
            print(f"Rechecked SQL query (attempt {attempt}): {rechecked_sql_query}")

    analysis_prompt = constants.DATA_ANALYST_PROMPT.format(query=query, sql_query=rechecked_sql_query, data=data, team=team)
    final_response = get_final_analysis(analysis_prompt)

    return {"output": final_response, "data": data}
