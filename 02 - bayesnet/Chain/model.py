from pomegranate.distributions import Categorical, ConditionalCategorical
from pomegranate.markov_chain import *
from pomegranate.hmm import DenseHMM

import numpy

# ------------------------------------Markov Model------------------------------------

# Define starting probabilities
probs_start = torch.tensor([[0.5,   # sun
                            0.5]    # rain
])
start = Categorical(probs=probs_start)

# Define transition model
probs_transitions = torch.tensor([
    [0.8, 0.2],  # sun [start]: sun, rain
    [0.3, 0.7]   # rain [start]: sun, rain
])
transitions = ConditionalCategorical(probs=[probs_transitions])

# Create Markov chain
model = MarkovChain([start, transitions])

# Sample 50 states from chain (if starts from sun, can change if desired)
sample = []
for i in range(100):
    samples = model.sample(1)
    if samples[:, 0] == 0: 
        sample.append(samples[:, 1].item())
# print("Samples: ",sample)
for i in range(len(sample)):
    if sample[i] == 0:
        print("Sun")
    else:
        print("Rain")

# ------------------------------------Hidden Markov Models------------------------------------

# Observation model for each state
probs_sun = torch.tensor([[0.2,   # umbrella
                            0.8]    # no umbrella
])
sun = Categorical(probs=probs_sun)

probs_rain = torch.tensor([[0.9,   # umbrella
                            0.1]    # no umbrella
])
rain = Categorical(probs=probs_rain)

states = [sun, rain]

# Transition model (prediction for tommorow's weather)
edges = [
    [0.8, 0.2], # "sun": sun, rain
    [0.3, 0.7] # "rain": sun, rain
]

# Starting probabilities
starts = [0.5, 0.5]

# Create the model
model = DenseHMM(states, edges=edges, starts=starts)

# Observed data
observations = numpy.array([[[0],[0],[1],[0],[0],[0],[0],[1],[1]]])
print("Observations: ", observations.shape)

# Predict underlying states
predictions = model.predict(observations)
predarray = numpy.array(predictions)
# print("Predictions: ",predarray)
for i in range(len(predarray[0])):
    if predarray[0][i] == 0:
        print("Sun")
    else:
        print("Rain")