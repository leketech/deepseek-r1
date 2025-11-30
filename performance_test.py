#!/usr/bin/env python3
"""
Performance testing script for the optimized inference server
"""

import asyncio
import aiohttp
import time
import statistics
from typing import List
import json

# Configuration
SERVER_URL = "http://localhost:8080"
NUM_CONCURRENT_REQUESTS = 100
REQUESTS_PER_CLIENT = 10
TOTAL_REQUESTS = NUM_CONCURRENT_REQUESTS * REQUESTS_PER_CLIENT

async def send_request(session, request_id):
    """Send a single inference request"""
    payload = {
        "input_text": f"This is test input number {request_id} for performance testing"
    }
    
    start_time = time.time()
    try:
        async with session.post(f"{SERVER_URL}/infer", json=payload) as response:
            end_time = time.time()
            latency = (end_time - start_time) * 1000  # Convert to milliseconds
            
            if response.status == 200:
                result = await response.json()
                return {
                    "success": True,
                    "latency_ms": latency,
                    "response": result
                }
            else:
                return {
                    "success": False,
                    "latency_ms": latency,
                    "error": f"HTTP {response.status}"
                }
    except Exception as e:
        end_time = time.time()
        latency = (end_time - start_time) * 1000
        return {
            "success": False,
            "latency_ms": latency,
            "error": str(e)
        }

async def client_worker(client_id: int, results: List[dict]):
    """Worker that sends multiple requests"""
    async with aiohttp.ClientSession() as session:
        for i in range(REQUESTS_PER_CLIENT):
            request_id = client_id * REQUESTS_PER_CLIENT + i
            result = await send_request(session, request_id)
            result["client_id"] = client_id
            result["request_id"] = request_id
            results.append(result)
            # Small delay to simulate realistic request patterns
            await asyncio.sleep(0.01)

async def run_performance_test():
    """Run the performance test"""
    print(f"Starting performance test with {NUM_CONCURRENT_REQUESTS} concurrent clients")
    print(f"Each client will send {REQUESTS_PER_CLIENT} requests")
    print(f"Total requests: {TOTAL_REQUESTS}")
    print("-" * 50)
    
    # Collect results
    results = []
    
    # Start time
    test_start_time = time.time()
    
    # Create tasks for all clients
    tasks = [
        client_worker(i, results) 
        for i in range(NUM_CONCURRENT_REQUESTS)
    ]
    
    # Run all clients concurrently
    await asyncio.gather(*tasks)
    
    # End time
    test_end_time = time.time()
    total_test_time = test_end_time - test_start_time
    
    # Analyze results
    successful_requests = [r for r in results if r["success"]]
    failed_requests = [r for r in results if not r["success"]]
    
    total_requests = len(results)
    success_rate = len(successful_requests) / total_requests * 100 if total_requests > 0 else 0
    
    # Latency statistics
    latencies = [r["latency_ms"] for r in successful_requests]
    
    if latencies:
        avg_latency = statistics.mean(latencies)
        median_latency = statistics.median(latencies)
        p95_latency = statistics.quantiles(latencies, n=20)[-1] if len(latencies) > 1 else latencies[0]
        min_latency = min(latencies)
        max_latency = max(latencies)
    else:
        avg_latency = median_latency = p95_latency = min_latency = max_latency = 0
    
    # Throughput calculation
    throughput = total_requests / total_test_time if total_test_time > 0 else 0
    
    # Print results
    print("Performance Test Results")
    print("=" * 50)
    print(f"Total Test Time: {total_test_time:.2f} seconds")
    print(f"Total Requests: {total_requests}")
    print(f"Successful Requests: {len(successful_requests)} ({success_rate:.1f}%)")
    print(f"Failed Requests: {len(failed_requests)}")
    print(f"Throughput: {throughput:.2f} requests/second")
    print()
    print("Latency Statistics (ms):")
    print(f"  Average: {avg_latency:.2f}")
    print(f"  Median: {median_latency:.2f}")
    print(f"  95th Percentile: {p95_latency:.2f}")
    print(f"  Min: {min_latency:.2f}")
    print(f"  Max: {max_latency:.2f}")
    print()
    
    # Print first few errors if any
    if failed_requests:
        print("Sample Errors:")
        for i, failed in enumerate(failed_requests[:5]):
            print(f"  {i+1}. {failed['error']}")
        if len(failed_requests) > 5:
            print(f"  ... and {len(failed_requests) - 5} more errors")
    
    # Save detailed results to file
    detailed_results = {
        "test_config": {
            "server_url": SERVER_URL,
            "concurrent_clients": NUM_CONCURRENT_REQUESTS,
            "requests_per_client": REQUESTS_PER_CLIENT,
            "total_requests": TOTAL_REQUESTS
        },
        "test_results": {
            "total_test_time_seconds": total_test_time,
            "total_requests": total_requests,
            "successful_requests": len(successful_requests),
            "failed_requests": len(failed_requests),
            "success_rate_percent": success_rate,
            "throughput_requests_per_second": throughput
        },
        "latency_stats_ms": {
            "average": avg_latency,
            "median": median_latency,
            "p95": p95_latency,
            "min": min_latency,
            "max": max_latency
        },
        "all_results": results
    }
    
    with open("performance_test_results.json", "w") as f:
        json.dump(detailed_results, f, indent=2)
    
    print(f"Detailed results saved to performance_test_results.json")
    
    return detailed_results

async def check_server_health():
    """Check if the server is running"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{SERVER_URL}/healthz") as response:
                if response.status == 200:
                    print("✓ Server is healthy")
                    return True
                else:
                    print(f"✗ Server health check failed with status {response.status}")
                    return False
    except Exception as e:
        print(f"✗ Could not connect to server: {e}")
        return False

async def main():
    """Main function"""
    print("DeepSeek Inference Server Performance Test")
    print("=" * 50)
    
    # Check server health first
    if not await check_server_health():
        print("Server is not accessible. Please make sure the server is running.")
        return
    
    # Run performance test
    try:
        results = await run_performance_test()
        
        # Print summary
        print("\n" + "=" * 50)
        print("TEST SUMMARY")
        print("=" * 50)
        print(f"Throughput: {results['test_results']['throughput_requests_per_second']:.2f} req/sec")
        print(f"Success Rate: {results['test_results']['success_rate_percent']:.1f}%")
        print(f"Avg Latency: {results['latency_stats_ms']['average']:.2f} ms")
        print(f"95th Percentile: {results['latency_stats_ms']['p95']:.2f} ms")
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())