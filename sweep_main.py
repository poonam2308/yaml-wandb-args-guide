import argparse
from utils import parse_yaml, setup_argparse, create_sweep, start_sweep_agent
from sweep_trainer import Trainer
from dotenv import load_dotenv
import os
import wandb

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
    if args.sweep_config:
        # Parse sweep configuration
        sweep_config = parse_yaml(args.sweep_config)
        # Create and start the sweep
        sweep_id = create_sweep(sweep_config)
        start_sweep_agent(sweep_id, sweep_function=sweep_run)  # Pass the sweep_run function
    else:
        # Parse training configuration
        config = parse_yaml(args.config)

        # Train without sweep
        trainer = Trainer(config, use_wandb=True)
        trainer.train()

    # Sweep run function called for each WandB sweep run
def sweep_run():
    wandb.init()
    sweep_config = wandb.config
    trainer = Trainer(sweep_config, use_wandb=True)
    trainer.train()
if __name__ == "__main__":
    main()
