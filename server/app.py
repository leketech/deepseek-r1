import asyncio
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import time
import json
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class RequestIn(BaseModel):
    input_text: str

class ResponseOut(BaseModel):
    result: str
    latency_ms: float

# Dynamic batching configuration
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", 32))
BATCH_TIMEOUT = float(os.environ.get("BATCH_TIMEOUT", 0.01))  # 10 ms default
MAX_CONCURRENT_BATCHES = int(os.environ.get("MAX_CONCURRENT_BATCHES", 4))

# Enhanced batcher with dynamic sizing
batch_queue = []
batch_event = asyncio.Event()
batch_semaphore = asyncio.Semaphore(MAX_CONCURRENT_BATCHES)

# Counter for monitoring
inference_count = 0
error_count = 0
batch_count = 0

# Performance metrics
total_batch_processing_time = 0
total_batches_processed = 0

async def batch_worker():
    global inference_count, error_count, batch_count, total_batch_processing_time, total_batches_processed
    while True:
        await batch_event.wait()
        # Acquire semaphore to limit concurrent batches
        async with batch_semaphore:
            # collect up to BATCH_SIZE items or until timeout
            start_time = time.time()
            await asyncio.sleep(BATCH_TIMEOUT)
            items = []
            while batch_queue and len(items) < BATCH_SIZE:
                items.append(batch_queue.pop(0))
            batch_event.clear()

            if not items:
                continue

            batch_count += 1
            batch_size = len(items)
            
            # Log batch size for monitoring
            logger.info(f"Processing batch #{batch_count} of size {batch_size}")

            # Extract payloads
            inputs = [it["payload"].input_text for it in items]
            
            # Process batch
            batch_start = time.time()
            try:
                # Simulate actual model inference with optimized batching
                # In a real implementation, this would be replaced with actual model inference
                results = await process_batch_inference(inputs)
                inference_count += len(inputs)
                
                batch_processing_time = (time.time() - batch_start) * 1000
                total_batch_processing_time += batch_processing_time
                total_batches_processed += 1
                
                # Log successful inferences
                avg_latency_per_item = batch_processing_time / len(items) if len(items) > 0 else 0
                logger.info({
                    "event": "batch_processed",
                    "batch_id": batch_count,
                    "batch_size": batch_size,
                    "processing_time_ms": batch_processing_time,
                    "avg_latency_per_item_ms": avg_latency_per_item,
                    "throughput_items_per_second": len(items) / (batch_processing_time / 1000) if batch_processing_time > 0 else 0
                })
                
            except Exception as e:
                error_count += len(inputs)
                logger.error(f"Inference error in batch #{batch_count}: {str(e)}")
                # Propagate error to all items in the batch
                for it in items:
                    it["future"].set_exception(e)
                continue

            # Set results for all items in the batch
            for res, it in zip(results, items):
                it["future"].set_result(res)

async def process_batch_inference(inputs):
    """
    Process a batch of inputs efficiently.
    In a real implementation, this would call the actual model.
    """
    # Simulate optimized batch processing
    # For demonstration, we're still doing echo but in a more efficient way
    await asyncio.sleep(0.001 * len(inputs))  # Simulate processing time
    return [f"echo:{s}" for s in inputs]

@app.on_event("startup")
async def startup():
    # Start multiple batch workers for better concurrency
    for i in range(MAX_CONCURRENT_BATCHES):
        asyncio.create_task(batch_worker())
    logger.info(f"Model server started with {MAX_CONCURRENT_BATCHES} batch workers")

@app.on_event("shutdown")
async def shutdown():
    logger.info(f"Server shutting down. Total inferences: {inference_count}, Errors: {error_count}, Batches: {batch_count}")

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.post("/infer", response_model=ResponseOut)
async def infer(req: RequestIn):
    start_time = time.time()
    fut = asyncio.get_event_loop().create_future()
    entry = {"payload": req, "future": fut}
    batch_queue.append(entry)
    batch_event.set()
    try:
        result = await asyncio.wait_for(fut, timeout=10.0)
        latency_ms = (time.time() - start_time) * 1000
        
        # Log inference for monitoring
        logger.info(json.dumps({
            "event": "model_inference",
            "input_text_length": len(req.input_text),
            "latency_ms": latency_ms,
            "timestamp": time.time()
        }))
        
        return ResponseOut(result=result, latency_ms=latency_ms)
    except asyncio.TimeoutError:
        error_count += 1
        logger.error("Inference timeout")
        raise HTTPException(status_code=504, detail="inference timeout")
    except Exception as e:
        error_count += 1
        logger.error(f"Inference failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"inference failed: {str(e)}")

@app.get("/metrics")
async def metrics():
    """Expose metrics for monitoring"""
    avg_batch_processing_time = total_batch_processing_time / total_batches_processed if total_batches_processed > 0 else 0
    return {
        "inference_count": inference_count,
        "error_count": error_count,
        "batch_count": batch_count,
        "avg_batch_processing_time_ms": avg_batch_processing_time,
        "uptime": time.time()
    }

@app.get("/config")
async def get_config():
    """Expose current configuration for monitoring"""
    return {
        "batch_size": BATCH_SIZE,
        "batch_timeout": BATCH_TIMEOUT,
        "max_concurrent_batches": MAX_CONCURRENT_BATCHES
    }