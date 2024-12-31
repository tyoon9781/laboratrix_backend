if __name__ == "__main__":
    import uvicorn
    from app.config import LOCAL_BACKEND_PORT

    uvicorn.run("app.app:app", host="0.0.0.0", port=LOCAL_BACKEND_PORT, reload=True)
