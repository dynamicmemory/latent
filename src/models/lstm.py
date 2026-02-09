from src.models.baseModel import BaseModel
import torch
import torch.nn as nn
import torch.optim as optim

# TODO: Rebuild non torch customer model
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
class LSTM(BaseModel):
    def __init__(self, epochs=200, lr=0.001, hidden_size=64, input_size=None, output_size=3):
        self.epochs = epochs 
        self.lr = lr 
        self.hidden_size = hidden_size
        self.input_size = input_size
        self.output_size = output_size
        self.window = 10 # HARDCODED TO 10 FOR NOW MATCHING THE DATA.
        self.model: None|TimeSeriesNN = None


    def train(self, X, y, verbose: bool = False) -> None:
        X = torch.tensor(X, dtype=torch.float32)
        y = torch.tensor(y.flatten(), dtype=torch.long)          # multi-class

        if self.input_size is None:
            self.input_size = X.shape[2]

        if self.model is None:
            self.model = TimeSeriesNN(X.shape[2], 
                                      hidden_size=self.hidden_size, 
                                      output_size=self.output_size)

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
    
        for epoch in range(self.epochs):
            self.model.train()
            optimizer.zero_grad()
            loss = criterion(self.model(X), y)
            loss.backward()
            optimizer.step()
    
            if verbose:
                if epoch % 20 == 0:
                    print(f"Epoch {epoch}: Loss = {loss.item():.4f}")


    # --- Evaluation ---
    def evaluation(self, X_test, y_test):
        y_test = torch.tensor(y_test.flatten(), dtype=torch.long)
        self.model.eval()
        with torch.no_grad():
            preds = torch.argmax(self.model(X_test), dim=1)
            acc = (preds == y_test).float().mean()
            print("Test Accuracy:", acc.item())
    
    
    # --- Predict next candle ---
    def predict(self, X_latest, X_train):
        """

        Args: 
            X - the latest windowed features 
        """
        X_train = torch.tensor(X_train, dtype=torch.float32)
        X_latest = torch.tensor(X_latest, dtype=torch.float32)
        X_latest = X_latest.reshape(1, 10, X_train.shape[2])

        with torch.no_grad():
            pred_next = torch.argmax(self.model(X_latest), dim=1).item()
        print(f"Next candle prediction: {pred_next}")
        return pred_next
    

    def save(self, path:str) -> None:
        checkpoint = {
            "model_state": self.model.state_dict(),
            "input_size": self.input_size,
            "hidden_size": self.hidden_size,
            "output_size": self.output_size,
            "window": self.window,
            "epochs": self.epochs,
            "lr": self.lr, 
        }
        torch.save(checkpoint, path)


    def load(self, path:str) -> None:
        checkpoint = torch.load(path)
        self.input_size = checkpoint["input_size"]
        self.hidden_size = checkpoint["hidden_size"]
        self.output_size = checkpoint["output_size"]
        self.window = checkpoint["window"]
        self.epochs = checkpoint["epochs"]
        self.lr = checkpoint["lr"]

        self.model = TimeSeriesNN(self.input_size, 
                                      hidden_size=self.hidden_size, 
                                      output_size=self.output_size)

        self.model.load_state_dict(checkpoint["model_state"])
        self.model.eval()
