# app/main.py

from fastapi import FastAPI, Depends
# from routes.item import route as item_router  # Correct import
from routes.user import route2, get_current_user  # Import the dependency



app = FastAPI(title="Authentication & User Management API",
              description="All in ONE User Management API for your Desired Need",
              version="1.1.0",
              servers=[
    #     {"url": "https://auth.globaltamasha.in", "description": "Staging environment"},
    #     {"url": "https://auth.globaltamasha.com", "description": "Production environment"},
    # ],
    docs_url="/docs",
    contact={
        "name": "Developed by Abhigyan Kumar",
        "url": "https://globaltamasha.com",
        "email": "info@globaltamasha.com",

    },
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})


app.openapi_version = "3.0.2"
app.include_router(route2)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

