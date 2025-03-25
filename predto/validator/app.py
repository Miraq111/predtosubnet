import asyncio
import random
import json

from communex.client import CommuneClient
from substrateinterface import Keypair
from validation import Validation

def load_categories(filename):
    """Load available prediction categories from a JSON file."""
    with open(filename, 'r') as file:
        categories = json.load(file)
    return categories

def random_category_selection(categories):
    """Select a random main category and sub-category (pair)."""
    main_category = random.choice(list(categories.keys()))
    sub_category = random.choice(categories[main_category])
    return main_category, sub_category

async def main():
    client = CommuneClient()
    key = Keypair()  # Placeholder for actual keypair initialization
    netuid = 1234
    validation = Validation(key, netuid, client)

    # Load prediction categories from a file
    filename = 'predictionList.json'
    categories = load_categories(filename)
    
    # Select a random category and sub-category
    category, pair = random_category_selection(categories)

    # Schedule validation tasks
    validation.schedule_tasks(category, pair)

if __name__ == '__main__':
    asyncio.run(main())
