import typer
from typing import Annotated

from communex._common import get_node_url
from communex.client import CommuneClient
from communex.compat.key import classic_load_key

from predto.validator._config import ValidatorSettings
from predto.validator.validation import get_subnet_netuid, Validation
import asyncio

app = typer.Typer()

@app.command()
def main(
    commune_key: Annotated[
        str, typer.Argument(help="Name of the key present in `~/.commune/key`")
    ],
    call_timeout: Annotated[int, typer.Option(help="Timeout for calls in seconds")] = 60,
):
    """
    Starts the validator for the predto subnet using the specified Commune key.
    """
    print(f"Debug: commune_key={commune_key}, call_timeout={call_timeout}")
    keypair = classic_load_key(commune_key)
    settings = ValidatorSettings()
    client = CommuneClient(get_node_url(use_testnet=True))  # Explicitly use testnet

    # Use netuid directly since "predto" isn't found
    subnet_uid = 38  # Hardcode for now; replace with get_subnet_netuid once confirmed
    # subnet_uid = get_subnet_netuid(client, "predto")  # Uncomment once name is verified
    print(f"subnet_uid: {subnet_uid}")

    validator = Validation(
        keypair,
        subnet_uid,
        client,
        call_timeout=call_timeout,
    )
    
    asyncio.run(validator.validation_loop(settings))

if __name__ == "__main__":
    app()
