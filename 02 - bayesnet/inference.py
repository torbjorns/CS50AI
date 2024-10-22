import torch
from model import model

# This is the observed data, -1 means missing data 
X = torch.tensor(
    [
        [
            -1,
            -1,
            1, # train is delayed
            -1,
        ]
    ]
)

X_masked = torch.masked.MaskedTensor(X, mask=(X != -1))

states = (
    ("rain", ["none", "light", "heavy"]),
    ("maintenance", ["yes", "no"]),
    ("train", ["on time", "delayed"]),
    ("appointment", ["attend", "miss"]),
)

# Calculate predictions
predictions = model.predict_proba(X_masked)

# Print predictions for each node
for (node_name, values), prediction in zip(states, predictions):
    if isinstance(prediction, str):
        print(f"{node_name}: {prediction}")
    else:
        print(f"{node_name}")
        for value, probability in zip(values, prediction[0]):
            print(f"    {value}: {probability:.4f}")