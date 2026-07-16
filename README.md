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

## Docker

The app is ready to run in a container

Build locally:

```bash
docker build -t fastinfo .
docker run --rm -p 8080:8080 -e DATABASE_URL="postgresql+psycopg://..." fastinfo
```

Use container port `8080`.
The app starts with `uvicorn app.main:app --host 0.0.0.0 --port ${PORT}`.
