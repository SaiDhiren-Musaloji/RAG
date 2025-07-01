import os
from pathlib import Path
from huggingface_hub import snapshot_download, login
from dotenv import load_dotenv

def verify_downloads(model_dir: Path) -> bool:
    """Verify that all required files are downloaded and have correct sizes."""
    required_files = {
        'tokenizer.model.v3': 500000,  # ~500KB
        'consolidated.safetensors': 13000000000,  # ~13GB
        'params.json': 100  # ~100 bytes is normal for a config file
    }
    
    all_files_present = True
    for filename, min_size in required_files.items():
        file_path = model_dir / filename
        if not file_path.exists():
            print(f"Missing file: {filename}")
            all_files_present = False
        else:
            size = file_path.stat().st_size
            if size < min_size:
                print(f"File {filename} is too small: {size} bytes (expected at least {min_size} bytes)")
                all_files_present = False
            else:
                print(f"✓ {filename} downloaded successfully ({size:,} bytes)")
    
    return all_files_present

def setup_mistral_model():
    """Download and set up the Mistral 7B model."""
    # Load environment variables
    load_dotenv()
    
    # Get Hugging Face token from environment variable
    hf_token = os.getenv('HUGGINGFACE_TOKEN')
    if not hf_token:
        print("\nError: HUGGINGFACE_TOKEN not found in environment variables.")
        print("Please set your Hugging Face token in the .env file or as an environment variable.")
        print("You can get your token from: https://huggingface.co/settings/tokens")
        return
    
    # Login to Hugging Face
    try:
        login(token=hf_token)
    except Exception as e:
        print(f"\nError logging in to Hugging Face: {str(e)}")
        return
    
    # Create models directory if it doesn't exist
    models_dir = Path.home() / 'mistral_models'
    model_dir = models_dir / '7B-Instruct-v0.3'
    model_dir.mkdir(parents=True, exist_ok=True)
    
    print("Downloading Mistral 7B model files...")
    try:
        snapshot_download(
            repo_id="mistralai/Mistral-7B-Instruct-v0.3",
            allow_patterns=["params.json", "consolidated.safetensors", "tokenizer.model.v3"],
            local_dir=model_dir,
            token=hf_token
        )
        # Verify downloads
        if verify_downloads(model_dir):
            print("\nModel setup complete! All files downloaded successfully.")
        else:
            print("\nWarning: Some files may not have downloaded correctly. Please check the errors above.")
    except Exception as e:
        print(f"\nError downloading model: {str(e)}")
        print("Please make sure you have:")
        print("1. Accepted the model's terms of use at https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3")
        print("2. A valid Hugging Face token")
        print("3. Enough disk space (at least 15GB) and a stable internet connection")

if __name__ == "__main__":
    setup_mistral_model() 