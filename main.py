import argparse
from utils import parse_yaml, setup_argparse
from trainer import Trainer

def main():
    # Parse arguments and configuration
    args = setup_argparse()
    config = parse_yaml(args.config)

    # Run training
    trainer = Trainer(config)
    trainer.train()

if __name__ == "__main__":
    main()
