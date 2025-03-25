from pydantic_settings import BaseSettings

class ValidatorSettings(BaseSettings):
    iteration_interval: int = 120  # Interval for running prediction requests (2 minutes)
    max_allowed_weights: int = 420  # Maximum score assigned to a miner
    weighting_period: int = 240  # Duration over which miner weights are adjusted (4 minutes)
