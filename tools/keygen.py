import secrets
import os
import sys

def generate_key(length=32):
    return secrets.token_hex(length)

def main():
    key = generate_key()
    print(f"Generated API Key: {key}")
    
    save = input("Save to .env file? (y/n): ").lower()
    if save == 'y':
        env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        mode = 'a' if os.path.exists(env_path) else 'w'
        with open(env_path, mode) as f:
            if mode == 'a':
                f.write("\n")
            f.write(f"X_API_KEY={key}\n")
        print(f"API Key saved to {os.path.abspath(env_path)}")

if __name__ == "__main__":
    main()
