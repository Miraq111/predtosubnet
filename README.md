Predto Subnet

Description

The Predto Subnet is a decentralized system designed to validate real world Projection. It uses an accuracy-based weighting system to determine the most reliable miners. This ensures that Projection are evaluated fairly and the most accurate contributors are rewarded.

Getting Started

Prerequisites

Ensure you have Python 3.10+ installed on your system. You can verify this by running:

python --version

Installation

Clone the repository to your local machine:

git clone https://github.com/Miraq111/predtosubnet.git
cd predtosubnet

Install required dependencies:

pip install -r requirements.txt

Validator Setup

Run the validator script to start validating predictions. Replace <name-of-your-com-key> with your actual key.

python3 -m predto.validator.cli <name-of-your-com-key>

Miner Setup

Start your miner by running the miner application. Ensure your key is correctly configured.

python3 -m predto.miner.cli <name-of-your-com-key>

How It Works

Miners submit their Projection for a given task.

Validator processes the work done by miners and compares them with the ground truth.

Weight Calculation: Miners receive weights based on their historical accuracy using an exponentially weighted moving average (EWMA).

Best Miner Selection: The miner with the highest weighted accuracy score is selected.

Updating Accuracy: The best miner's accuracy is updated for future evaluations.

Contributing

If you'd like to contribute to this project, feel free to fork the repository, create a new branch, and submit a pull request.

License

This project is licensed under the MIT License.
