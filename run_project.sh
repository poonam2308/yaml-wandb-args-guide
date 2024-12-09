#! /usr/bin/env bash

# Here you can add bash commands:
#SBATCH --container-mounts=/etc/slurm/task_prolog:/etc/slurm/task_prolog,/scratch:/scratch,/pfs/work7/workspace/scratch/ul_plx49-amos-ssd:/myworkspace
#SBATCH --container-mount-home
#SBATCH --output=slurm_log/%x_%j.out  # Output file for job logs %x for job-name and %j for job-id

# Get Data form Workspace to GPU Node -------------------------------
# Set TMPDIR for temporary storage specific to this job
export TMPDIR="/scratch/slurm_tmpdir/job_${SLURM_JOBID}"


#-------

# Other Stuff:
export CUDA_DEVICE_ORDER=PCI_BUS_ID
export DOME_CPUSET=$(scontrol show job $SLURM_JOB_ID --details | grep 'CPU_IDs' | awk '{print $2}' | awk -F= '{print $2}')
export DOME_MEMSET=$(scontrol show job $SLURM_JOB_ID --details | grep 'MemPerTres' | awk -F= '{print $2}' | awk -F: '{print $2}')
export XDG_CACHE_HOME=/tmp/cache
JOB_TIME_LIMIT=$(scontrol show job $SLURM_JOB_ID | grep -oP 'TimeLimit=\K\S+')
echo "================================================================================"
echo "Running on $(hostname). This worker has IP $(ip a | grep 134.60.70 | awk '{print $2}')"
echo "Running as $USER, with groups: $(groups)"
echo "Job ID: $SLURM_JOB_ID"
echo "CUDA_VISIBLE_DEVICES: $CUDA_VISIBLE_DEVICES"
echo "The job time limit is: $JOB_TIME_LIMIT"
echo "Using CPU Cores $DOME_CPUSET"
echo "Using $DOME_MEMSET MiB RAM"
echo "================================================================================"
nvidia-smi



source .env
pip install --upgrade pip
pip install -r ./yaml-wandb-args-guide/requirements.txt

# Check if WandB API key is set
if [ -z "$WANDB_API_KEY" ]; then
    echo -e "WANDB_API_KEY not set. Logs will be saved locally"
    USE_WANDB=false
else
    echo -e "WandB API key found. Logging into WandB..."
    wandb login
    USE_WANDB=true
fi

python main.py --config config.yaml --use_wandb $USE_WANDB

