if __name__ == "__main__":
    import uvicorn

    # Run the application
    uvicorn.run(
        "app.main:app",  # Path to the FastAPI app instance
        host="0.0.0.0",  # Host to listen on
        port=8000,       # Port to listen on
        reload=True,     # Auto-reload during development
        log_level="debug"  # Log level
    )
