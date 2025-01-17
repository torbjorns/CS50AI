import numpy
import torch
from model import model


rain_values = ["none", "light", "heavy"]
maintenance_values = ["yes", "no"]
train_values = ["on time", "delayed"]
appoinment_values = ["attend", "miss"]


# Calculate likelihood of this specific combination of events
probability = model.probability( 
    torch.as_tensor(
        [
            [
                rain_values.index("none"),
                maintenance_values.index("no"),
                train_values.index("on time"),
                appoinment_values.index("miss"),
            ]
        ]
    )
)

print(probability)