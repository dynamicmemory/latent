import torch
import torch.nn as nn
import torch.optim as optim
from src.miniML.machLearnTools import MachLearnTools
from src.features import Features
from src.sqlitedb import DatabaseManager

# --- Settings ---
asset = "BTCUSDT"
timeframe = "15"
window = 10
epochs = 200
lr = 0.001

# --- Load data ---
dbm = DatabaseManager(asset, timeframe)
df = dbm.get_dataframe()

features = Features(df)
X, y = features.run_features()

mlt = MachLearnTools(X, y)
X_train, X_test, y_train, y_test = mlt.timeseries_pipeline(window=window)

# --- Convert to PyTorch tensors ---
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.long)  # multi-class
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.long)

# --- Define a simple time-series NN ---
class TimeSeriesNN(nn.Module):
    def __init__(self, input_size, hidden_size=64, output_size=3):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        _, (h_n, _) = self.lstm(x)
        out = self.fc(h_n[-1])
        return out

input_size = X_train.shape[2]  # features per timestep
output_size = 3  # multi-class labels

model = TimeSeriesNN(input_size, hidden_size=64, output_size=output_size)

# --- Training setup ---
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=lr)

# --- Training loop ---
for epoch in range(epochs):
    model.train()
    optimizer.zero_grad()
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()

    if epoch % 20 == 0:
        print(f"Epoch {epoch}: Loss = {loss.item():.4f}")

# --- Evaluation ---
model.eval()
with torch.no_grad():
    preds = torch.argmax(model(X_test), dim=1)
    acc = (preds == y_test.flatten()).float().mean()
    print("Test Accuracy:", acc.item())

# --- Predict next candle ---
latest_X = torch.tensor(mlt.latest_features(window=window), dtype=torch.float32)
with torch.no_grad():
    pred_next = torch.argmax(model(latest_X), dim=1).item()
print(f"Next candle prediction: {pred_next}")
