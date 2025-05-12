import sys
import os

# Add project root to path to ensure imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from api.vercel_entry import app
    import uvicorn
    
    if __name__ == "__main__":
        print("Starting Myra ChatBot API for local testing...")
        uvicorn.run(app, host="127.0.0.1", port=8000)
except Exception as e:
    print(f"Error starting app: {str(e)}")
    import traceback
    traceback.print_exc()
