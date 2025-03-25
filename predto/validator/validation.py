from collections import deque
from statistics import mean
from typing import List, Dict, Tuple

import asyncio
from communex.client import CommuneClient
from communex.compat.key import Keypair

def weight_miners(accuracy_scores: Dict[str, List[float]]) -> Dict[str, float]:
    """
    Assigns weights to miners based on their accuracy scores using an exponentially weighted moving average.
    """
    weights = {}
    alpha = 0.5  # Smoothing factor for EWMA
    
    for miner, scores in accuracy_scores.items():
        if not scores:  # Handle empty scores
            weights[miner] = 0.0
        else:
            ewma = scores[0]  # Initialize with first score
            for score in scores[1:]:
                ewma = alpha * score + (1 - alpha) * ewma
            weights[miner] = ewma
    
    return weights

def validate_prediction(
    ground_truth: float,
    miner_predictions: Dict[str, float],
    miner_weights: Dict[str, float],
    threshold: float = 0.1
) -> Tuple[str, float]:
    """
    Validates predictions from miners based on weighted accuracy.
    """
    best_miner = None
    best_accuracy = float('-inf')
    
    for miner, prediction in miner_predictions.items():
        if ground_truth == 0:  # Avoid division by zero
            accuracy = 1.0 if prediction == 0 else 0.0
        else:
            accuracy = max(0, 1 - abs(prediction - ground_truth) / abs(ground_truth))
        weighted_accuracy = accuracy * miner_weights.get(miner, 0.0)
        
        if weighted_accuracy > best_accuracy and accuracy >= threshold:
            best_miner = miner
            best_accuracy = weighted_accuracy
    
    return best_miner, best_accuracy if best_miner else 0.0

def update_accuracy_scores(
    accuracy_scores: Dict[str, List[float]],
    miner: str,
    new_score: float,
    max_history: int = 10
) -> None:
    """
    Updates accuracy scores for a miner while maintaining a fixed history size.
    """
    if miner not in accuracy_scores:
        accuracy_scores[miner] = deque(maxlen=max_history)
    accuracy_scores[miner].append(new_score)

def predict_and_validate(
    ground_truth: float,
    miner_predictions: Dict[str, float],
    accuracy_scores: Dict[str, List[float]],
    threshold: float = 0.1
) -> Tuple[str, float, Dict[str, float]]:
    """
    Performs prediction validation and updates miner weights accordingly.
    """
    miner_weights = weight_miners(accuracy_scores)
    best_miner, best_accuracy = validate_prediction(ground_truth, miner_predictions, miner_weights, threshold)
    
    if best_miner:
        update_accuracy_scores(accuracy_scores, best_miner, best_accuracy)
    
    return best_miner, best_accuracy, miner_weights

def get_subnet_netuid(client: CommuneClient, subnet_name: str) -> int:
    """
    Retrieves the network UID for a given subnet name.
    """
    subnets = client.query_map_subnet_names()
    for netuid, name in subnets.items():
        if name == subnet_name:
            return netuid
    raise ValueError(f"Subnet '{subnet_name}' not found")

class Validation:
    """
    Manages the validation loop for miners on a subnet.
    """
    def __init__(self, keypair: Keypair, netuid: int, client: CommuneClient, call_timeout: int):
        self.keypair = keypair
        self.netuid = netuid
        self.client = client
        self.call_timeout = call_timeout
        self.accuracy_scores: Dict[str, List[float]] = {}

    async def validation_loop(self, settings):
        """
        Runs an infinite loop to validate miner predictions on the subnet.
        """
        print(f"Starting validation loop for subnet {self.netuid}...")
        while True:
            # Fetch registered modules (miners) from subnet
            # Use query_map_key (or adjust based on your communex version)
            modules = self.client.query_map_key(self.netuid)  # Dict of key: info
            print(modules)
            if not modules:
                print("No miners registered on subnet.")
                await asyncio.sleep(60)
                continue

            # Placeholder: Replace with real prediction query logic
            miner_predictions = {}
            for miner_key in modules.keys():
                print(miner_key)
                print(hash(miner_key))
                # Simulate a prediction (replace with actual miner call)
                miner_predictions[miner_key] = 100.0 + hash(miner_key) % 10  # Example variation

            # Placeholder: Replace with real ground truth source
            ground_truth = 102.0  # Example value; needs real data

            best_miner, best_accuracy, miner_weights = predict_and_validate(
                ground_truth, miner_predictions, self.accuracy_scores
            )
            print(f"Best miner: {best_miner}, Accuracy: {best_accuracy}, Weights: {miner_weights}")
            
            await asyncio.sleep(60)  # Adjust interval as needed
