import yaml
import argparse

def parse_yaml(config_path):
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

def setup_argparse():
    parser = argparse.ArgumentParser(description="Simple DL Project")
    parser.add_argument("--config", type=str, required=True, help="Path to the YAML configuration file.")
    parser.add_argument("--use_wandb", type=bool, default=False, help="Enable WandB logging if True.")
    return parser.parse_args()
