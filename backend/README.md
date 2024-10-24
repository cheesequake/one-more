## Backend

Backend has been written on Python using FastAPI, a lightweight, fast web framework for building APIs. The following files are of utmost importance.

### [Constants](./constants.py)

Contains constants to be used in the application

### [Query Engine](./query_engine.py)

The query engine is a structured pipeline of data. It is a blackbox for the main [app.py](./app.py), and handles all the LLM processing. The LLM first converts user input to Embeddings using a local HuggingFace sentence transformer model. These embeddings are used to get few shot examples. Then these examples are combined into table info, and sent as a prompt via ChatBedrock to Claude 3.5 Sonnet, which generates an SQL query. This query is again sent to Sonnet for double checking. Finally, this query gets executed in RDS MySQL, and the data is sent to Llama 3.1 for analysis.

### [App](./app.py)

This is the heart of the application. It contains all the end-points of the application which can be accessed through React front-end.