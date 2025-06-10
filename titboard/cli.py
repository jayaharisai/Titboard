import typer
import uvicorn
import os
import sys

# Create the Typer app
app = typer.Typer()

@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="Host to bind to"),
    port: int = typer.Option(8000, help="Port to bind to"),
    reload: bool = typer.Option(True, help="Enable auto-reload")
):
    """Start the FastAPI server"""
    print(f"Starting server on {host}:{port}")
    
    # Get the directory where the package is installed
    package_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add the package directory to Python path so imports work
    if package_dir not in sys.path:
        sys.path.insert(0, package_dir)
    
    # Change to package directory so relative paths work
    os.chdir(package_dir)
    
    try:
        uvicorn.run("main:app", host=host, port=port, reload=reload)
    except Exception as e:
        print(f"Error starting server: {e}")
        raise typer.Exit(1)

def main():
    """Entry point for the CLI"""
    app()

if __name__ == "__main__":
    main()