import argparse
from utils import parse_yaml, setup_argparse
from trainer import Trainer
from dotenv import load_dotenv
import os

def main():
    # Load environment variables from .env file
    load_dotenv()

    # You can now access your environment variables, e.g., WANDB_API_KEY
    wandb_api_key = os.getenv("WANDB_API_KEY")
    if wandb_api_key:
        print("WANDB_API_KEY is loaded successfully.")
    else:
        print("WANDB_API_KEY is not set. Please check your .env file.")

    # Parse arguments and configuration
    args = setup_argparse()
    config = parse_yaml(args.config)

    # Run training
    trainer = Trainer(config)
    trainer.train()

if __name__ == "__main__":
    main()
