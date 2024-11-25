import torch
import torch.nn as nn
import torch.optim as optim
import wandb
from model import SimpleNet
from torch.utils.data import DataLoader, TensorDataset
import torch.nn.functional as F
import numpy as np


class Trainer:
    def __init__(self, config, use_wandb=False):
        self.config = config
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SimpleNet(
            config.get('input_dim', 32),  # Default values for sweep
            config.get('hidden_dim', 64),
            config.get('output_dim', 10)
        ).to(self.device)

        # Optimizer and loss function
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = self._initialize_optimizer()

        self.use_wandb = use_wandb
        if self.use_wandb:
            wandb.init(project="hyperparameter_sweep", config=config)
        else:
            print("WandB logging is disabled. Logs will be saved locally.")

    def _initialize_optimizer(self):
        lr = self.config.get('learning_rate', 0.001)
        optimizer_name = self.config.get('optimizer', 'adam').lower()

        if optimizer_name == 'adam':
            return optim.Adam(self.model.parameters(), lr=lr)
        elif optimizer_name == 'sgd':
            return optim.SGD(self.model.parameters(), lr=lr)
        else:
            raise ValueError(f"Unknown optimizer: {optimizer_name}")

    def get_dummy_data(self):
        # Generate dummy data
        input_dim = self.config.get('input_dim', 32)
        output_dim = self.config.get('output_dim', 10)
        batch_size = self.config.get('batch_size', 32)

        X = np.random.rand(1000, input_dim).astype(np.float32)
        y = np.random.randint(0, output_dim, size=(1000,))
        dataset = TensorDataset(torch.tensor(X), torch.tensor(y))
        return DataLoader(dataset, batch_size=batch_size, shuffle=True)

    def train(self):
        dataloader = self.get_dummy_data()
        epochs = self.config.get('epochs', 10)

        for epoch in range(epochs):
            for batch_idx, (data, target) in enumerate(dataloader):
                data, target = data.to(self.device), target.to(self.device)

                # Forward pass
                outputs = self.model(data)
                loss = self.criterion(outputs, target)

                # Backward pass
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

            # Log metrics
            if self.use_wandb:
                wandb.log({"epoch": epoch + 1, "loss": loss.item()})
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss.item()}")

        print("Training Completed.")
        if self.use_wandb:
            wandb.finish()
