# Confusing class for the time being, a place keeping until i build my own
# time series nn from the ground up
# Ive essentially wrapped the torch time-series NN model with another class to 
# be able to slice it into my current design, this entire class will be rebuilt
# and simplified eventually
import torch
import torch.nn as nn
import torch.optim as optim

# --- Define a simple time-series NN from torches library---
class TimeSeriesNN(nn.Module):
    def __init__(self, input_size, hidden_size=64, output_size=3):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)


    def forward(self, x):
        _, (h_n, _) = self.lstm(x)
        out = self.fc(h_n[-1])
        return out


# --- Temp: Wrapper class to scalpel cut in torches workflow to ours ---
class Torchnn:
    def __init__(self, mlt, X_train, X_test, y_train, y_test, epochs=200, lr=0.001, window=10, training=False):
        self.mlt = mlt
        self.window = window
        # --- Convert to PyTorch tensors ---
        self.X_train = torch.tensor(X_train, dtype=torch.float32)
        self.y_train = torch.tensor(y_train, dtype=torch.long)  # multi-class
        self.X_test = torch.tensor(X_test, dtype=torch.float32)
        self.y_test = torch.tensor(y_test, dtype=torch.long)
        self.epochs = epochs
        self.lr = lr

        # Model specific stuff
        input_size = X_train.shape[2]  # features per timestep
        output_size = 3  # multi-class labels
        self.model = TimeSeriesNN(input_size, hidden_size=64, output_size=output_size)

        if training:
            self.training_loop()


    def training_loop(self):
        # --- Training setup ---
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
    
        # --- Training loop ---
        y_train = self.y_train.flatten().long()
    
        for epoch in range(self.epochs):
            self.model.train()
            optimizer.zero_grad()
            outputs = self.model(self.X_train)
            loss = criterion(outputs, y_train)
            loss.backward()
            optimizer.step()
    
            if epoch % 20 == 0:
                print(f"Epoch {epoch}: Loss = {loss.item():.4f}")
    
    
    # --- Evaluation ---
    def evaluation(self):
        # y_test = torch.tensor(self.y_test.flatten(), dtype=torch.long)
        self.model.eval()
        with torch.no_grad():
            preds = torch.argmax(self.model(self.X_test), dim=1)
            acc = (preds == self.y_test.flatten()).float().mean()
            print("Test Accuracy:", acc.item())
    
    
    # --- Predict next candle ---
    def predict(self):
        latest_X = torch.tensor(self.mlt.latest_features(window=self.window), dtype=torch.float32)
        latest_X = latest_X.reshape(1, self.window, self.X_train.shape[2])
        with torch.no_grad():
            pred_next = torch.argmax(self.model(latest_X), dim=1).item()
        print(f"Next candle prediction: {pred_next}")
        return pred_next
    

    def save_checkpoint(self, path:str) -> None:
        checkpoint = {
            "model_state": self.model.state_dict(),
            "input_size": self.X_train.shape[2],
            "window": self.window,
            "epochs": self.epochs,
            "lr": self.lr, 
        }
        torch.save(checkpoint, path)


    def load_checkpoint(self, path:str) -> None:
        checkpoint = torch.load(path)
        self.model.load_state_dict(checkpoint["model_state"])
        self.window = checkpoint["window"]
        self.model.eval()
