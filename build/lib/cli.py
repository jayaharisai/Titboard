import typer
import uvicorn

app = typer.Typer()

@app.command()
def serve(host: str = "0.0.0.0", port: int = 8000, reload: bool = True):
    """Start the FastAPI server"""
    uvicorn.run("main.main:app", host=host, port=port, reload=reload)

if __name__ == "__main__":
    app()
