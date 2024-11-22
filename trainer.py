import torch
import torch.nn as nn
import torch.optim as optim
import wandb
from model import SimpleNet
from torch.utils.data import DataLoader, TensorDataset
import torch.nn.functional as F
import numpy as np


class Trainer:
    def __init__(self, config):
        self.config = config
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = SimpleNet(
            config['model']['input_dim'],
            config['model']['hidden_dim'],
            config['model']['output_dim']
        ).to(self.device)
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=config['experiment']['learning_rate'])
        wandb.init(project="simple-dl-project", name=config['experiment']['name'], config=config)

    def get_dummy_data(self):
        # Create dummy data
        X = np.random.rand(1000, self.config['model']['input_dim']).astype(np.float32)
        y = np.random.randint(0, self.config['model']['output_dim'], size=(1000,))
        dataset = TensorDataset(torch.tensor(X), torch.tensor(y))
        return DataLoader(dataset, batch_size=self.config['experiment']['batch_size'], shuffle=True)

    def train(self):
        dataloader = self.get_dummy_data()
        epochs = self.config['experiment']['epochs']

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

            # Log metrics to WandB
            wandb.log({"epoch": epoch + 1, "loss": loss.item()})
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss.item()}")

        print("Training Completed.")
        wandb.finish()
