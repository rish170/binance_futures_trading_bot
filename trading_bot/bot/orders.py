import time
from typing import Optional
from .client import BinanceFuturesClient
from .logger import logger

def execute_order(client: BinanceFuturesClient, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None) -> dict:
    logger.info(f"Placing {order_type} order | symbol={symbol} side={side} quantity={quantity} price={price}")
    try:
        response = client.place_order(symbol, side, order_type, quantity, price)
        
        order_id = response.get("orderId")
        status = response.get("status")
        executed_qty = response.get("executedQty")
        avg_price = response.get("avgPrice", "0")
        
        logger.info(f"Response | orderId={order_id} status={status} executedQty={executed_qty} avgPrice={avg_price}")
        return response
    except Exception as e:
        logger.error(f"Failed to place order | symbol={symbol} reason={str(e)}")
        raise

def execute_twap_order(client: BinanceFuturesClient, symbol: str, side: str, total_quantity: float, slices: int, interval_seconds: int):
    logger.info(f"Starting TWAP | symbol={symbol} side={side} total_quantity={total_quantity} slices={slices} interval={interval_seconds}s")
    
    slice_qty = round(total_quantity / slices, 3)
    
    total_executed = 0.0
    
    for i in range(1, slices + 1):
        if i == slices:
            current_qty = round(total_quantity - total_executed, 3)
        else:
            current_qty = slice_qty
            
        logger.info(f"TWAP Step | step={i}/{slices} quantity={current_qty}")
        
        try:
            execute_order(client, symbol, side, "MARKET", current_qty)
            total_executed += current_qty
            total_executed = round(total_executed, 3)
            logger.info(f"[{i}/{slices}] Executed {current_qty} {symbol.replace('USDT', '')}")
        except Exception as e:
            logger.error(f"TWAP Step Failed | step={i}/{slices} reason={str(e)}")
        
        if i < slices:
            logger.info(f"TWAP Waiting | seconds={interval_seconds}")
            time.sleep(interval_seconds)
            
    logger.info(f"TWAP Completed | total_executed={total_executed}/{total_quantity}")
