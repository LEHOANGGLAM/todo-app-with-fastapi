from fastapi import FastAPI
from routers import company, auth


app = FastAPI()

# app.include_router(author.router)
# app.include_router(book.router)
app.include_router(company.router)
app.include_router(auth.router)

@app.get("/", tags=["Health Check"])
async def health_check():
    return "API Service is up and running!"
