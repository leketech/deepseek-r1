#!/usr/bin/env python3
"""
Script to run the complete optimization workflow
"""

import subprocess
import sys
import os
import argparse

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}")
    print(f"Running: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Run inference optimization workflow')
    parser.add_argument('--profile', default='production',
                        choices=['development', 'production', 'high_throughput', 'cost_optimized'],
                        help='Performance profile to apply')
    parser.add_argument('--skip-deploy', action='store_true',
                        help='Skip deployment step')
    parser.add_argument('--skip-test', action='store_true',
                        help='Skip performance testing')
    
    args = parser.parse_args()
    
    print("DeepSeek Inference Optimization Workflow")
    print("=" * 50)
    
    # Step 1: Apply performance profile
    print(f"\n1. Applying {args.profile} performance profile...")
    if not run_command(f"python apply_performance_profile.py {args.profile}", 
                      "Applying performance profile"):
        print("Failed to apply performance profile")
        sys.exit(1)
    
    # Step 2: Deploy updated configuration
    if not args.skip_deploy:
        print("\n2. Deploying updated configuration...")
        if not run_command("kubectl apply -f k8s/", 
                          "Deploying Kubernetes configuration"):
            print("Failed to deploy configuration")
            sys.exit(1)
    else:
        print("\n2. Skipping deployment (as requested)")
    
    # Step 3: Wait for deployment to stabilize
    print("\n3. Waiting for deployment to stabilize...")
    run_command("kubectl rollout status deployment/deepseek-inference", 
                "Waiting for deployment rollout")
    
    # Step 4: Run performance tests
    if not args.skip_test:
        print("\n4. Running performance tests...")
        print("Note: Make sure the server is running before running tests")
        print("You can start the server with: python -m uvicorn server.app:app --host 0.0.0.0 --port 8080")
        input("Press Enter when the server is running, or Ctrl+C to skip...")
        
        if not run_command("python performance_test.py", 
                          "Running performance tests"):
            print("Performance tests failed")
            sys.exit(1)
    else:
        print("\n4. Skipping performance tests (as requested)")
    
    print("\n" + "=" * 50)
    print("Optimization workflow completed successfully!")
    print("=" * 50)
    
    if not args.skip_test:
        print("\nPerformance test results are available in performance_test_results.json")
    
    print(f"\nApplied profile: {args.profile}")
    print("Configuration files have been updated with optimized settings")

if __name__ == "__main__":
    main()