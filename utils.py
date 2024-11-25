import yaml
import argparse
import wandb
import subprocess


def parse_yaml(config_path):
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

def create_sweep(sweep_config):
    sweep_id = wandb.sweep(sweep_config, project="hyperparameter-sweep-demo")
    print(f"Sweep created with Sweep ID: {sweep_id}")
    return sweep_id

# def start_sweep_agent(sweep_id):
#     print(f"Starting sweep agent for sweep ID: {sweep_id}...")
#     subprocess.run(["wandb", "agent", sweep_id])

# def start_sweep_agent(sweep_id):
#     """Start the WandB sweep agent."""
#     wandb.agent(sweep_id, function=sweep_run)

def start_sweep_agent(sweep_id, sweep_function):
    """Start the WandB sweep agent with the given function."""
    wandb.agent(sweep_id, function=sweep_function)

def setup_argparse():
    parser = argparse.ArgumentParser(description="A project to for yaml, args and wandb integration")
    parser.add_argument("--config", type=str, required=False, help="Path to the YAML configuration file.")
    parser.add_argument("--use_wandb", type=bool, default=False, help="Enable WandB logging if True.")
    parser.add_argument("--sweep_config", type=str, required=True, help="Path to the sweep YAML configuration file.")
    return parser.parse_args()
