# Predto Subnet  

## Description  

The **Predto Subnet** is a decentralized system designed to validate real-world projections. It uses an **accuracy-based weighting system** to determine the most reliable miners. This ensures that projections are evaluated fairly and that the most accurate contributors are rewarded.  

---

## Getting Started  

### Prerequisites  

Ensure you have **Python 3.10+** installed on your system. You can verify this by running:  

```sh
python --version
```

### Installation  

Clone the repository to your local machine:  

```sh
git clone https://github.com/Miraq111/predtosubnet.git
cd predtosubnet
```

## Install required dependencies:

```sh
pip install -r requirements.txt
```
## Validator Setup
Run the validator script to start validating predictions. Replace <name-of-your-com-key> with your actual key:
```sh

python3 -m predto.validator.cli <name-of-your-com-key>
```

## Miner Setup
Start your miner by running the miner application. Ensure your key is correctly configured:

```sh

python3 -m predto.miner.cli <name-of-your-com-key>
```
