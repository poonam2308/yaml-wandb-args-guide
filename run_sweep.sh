source .env
pip install --upgrade pip
pip install -r requirements.txt

# Check if WandB API key is set
if [ -z "$WANDB_API_KEY" ]; then
    echo -e "WANDB_API_KEY not set. Logs will be saved locally"
    USE_WANDB=false
else
    echo -e "WandB API key found. Logging into WandB..."
    wandb login
    USE_WANDB=true
fi

# for hyperparameter sweeping
python sweep_main.py --sweep_config sweep_config.yaml --use_wandb $USE_WANDB

