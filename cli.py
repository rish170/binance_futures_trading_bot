import typer
from rich import print
from rich.console import Console
from trading_bot.bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
from trading_bot.bot.client import BinanceFuturesClient
from trading_bot.bot.orders import execute_order, execute_twap_order
from trading_bot.bot.logger import log_separator

app = typer.Typer(help="Binance Futures Testnet Trading Bot CLI")
console = Console()

@app.command()
def place_order(
    symbol: str = typer.Argument(..., help="Trading symbol (e.g., BTCUSDT)"),
    side: str = typer.Argument(..., help="Order side (BUY/SELL)"),
    order_type: str = typer.Argument(..., help="Order type (MARKET/LIMIT)"),
    quantity: float = typer.Argument(..., help="Order quantity (e.g., 0.001)"),
    price: float = typer.Option(None, help="Price (required if LIMIT)")
):
    try:
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        order_type = validate_order_type(order_type)
        quantity = validate_quantity(quantity)
        price = validate_price(order_type, price)

        console.print(f"[cyan]Summary: Placing {order_type} {side} order for {quantity} {symbol} at price {price}[/cyan]")
        
        client = BinanceFuturesClient()
        response = execute_order(client, symbol, side, order_type, quantity, price)
        
        console.print("[green]Order executed successfully![/green]")
        console.print(response)

    except ValueError as ve:
        console.print(f"[red]Validation Error: {ve}[/red]")
    except Exception as e:
        console.print(f"[red]Error placing order: {e}[/red]")
    finally:
        log_separator()


@app.command()
def twap_order(
    symbol: str = typer.Argument(..., help="Trading symbol (e.g., BTCUSDT)"),
    side: str = typer.Argument(..., help="Order side (BUY/SELL)"),
    total_quantity: float = typer.Argument(..., help="Total quantity to execute"),
    slices: int = typer.Argument(..., help="Number of slices to split the order into"),
    interval_seconds: int = typer.Argument(..., help="Time interval between orders in seconds")
):
    try:
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        total_quantity = validate_quantity(total_quantity)
        
        if slices <= 1:
            raise ValueError("Slices must be > 1 for TWAP.")
        if interval_seconds <= 0:
            raise ValueError("Interval must be > 0.")

        console.print(f"[cyan]Summary: TWAP {side} order for {total_quantity} {symbol} in {slices} slices every {interval_seconds}s[/cyan]")

        client = BinanceFuturesClient()
        execute_twap_order(client, symbol, side, total_quantity, slices, interval_seconds)

        console.print("[green]TWAP execution completed successfully![/green]")

    except ValueError as ve:
        console.print(f"[red]Validation Error: {ve}[/red]")
    except Exception as e:
        console.print(f"[red]Error executing TWAP order: {e}[/red]")
    finally:
        log_separator()

if __name__ == "__main__":
    app()
