main branch not developed anymore. There are 2 master branches:
job_env_version : This version preppers data for application and contains ai and embeddings logic and jobs
read_only_ver: This is lightweight version of app containing only functionality to show UI

# FastInfo
App for creating short description of articles and grouping them by the same topic with use of AI  

In order launch working app there need to be .env file configured with keys for:

    #Huggingface token
    HF_TOKEN=
    
    #Open AI api key
    OPEN_AI_KEY=
    
    #Url to db
    DATABASE_URL=
    
    #Api key to pinecone
    PINECONE_API_KEY=
