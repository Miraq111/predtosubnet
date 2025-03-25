import typer
from typing import Annotated, Optional

from communex._common import get_node_url
from communex.client import CommuneClient
from communex.compat.key import classic_load_key
from communex.module._rate_limiters.limiters import StakeLimiterParams
from communex.module.server import ModuleServer

from predto.validator._config import ValidatorSettings

# Import validation safely to avoid circular imports
try:
    from predto.validator.validation import get_subnet_netuid, Validation
except ImportError as e:
    print(f"Warning: Unable to import validation module - {e}")
    get_subnet_netuid = None
    Validation = None

from predto.miner.app import Miner
import uvicorn

app = typer.Typer()

@app.command("serve-miner")
def serve(
    commune_key: Annotated[
        str, typer.Argument(help="Name of the key present in `~/.commune/key`")
    ],
    ip: Optional[str] = "127.0.0.1",  # Default value for IP
    port: Optional[int] = 8000,       # Default value for Port
):
    """
    Starts the server to serve the Miner module.
    
    Args:
        commune_key (str): The name of the commune key.
        ip (str, optional): The IP address to host the server. Default is "127.0.0.1".
        port (int, optional): The port to bind the server. Default is 8000.
    """
    keypair = classic_load_key(commune_key)  # Load key for the commune
    module = Miner()  # Initialize the Miner module

    server = ModuleServer(
        module, keypair, subnets_whitelist=[38]  # Specify the subnets whitelist
    )
    
    miner_app = server.get_fastapi_app()  # Get FastAPI app from the server
    uvicorn.run(miner_app, host=ip, port=port)  # Run the Uvicorn server

if __name__ == "__main__":
    typer.run(serve)
