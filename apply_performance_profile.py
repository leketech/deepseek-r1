#!/usr/bin/env python3
"""
Script to apply performance profiles to the deployment
"""

import yaml
import json
import argparse
import os
import sys

def load_profiles(profiles_file="performance_profiles.yaml"):
    """Load performance profiles from YAML file"""
    try:
        with open(profiles_file, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {profiles_file}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing {profiles_file}: {e}")
        sys.exit(1)

def apply_profile_to_deployment(profile, deployment_file="k8s/deployment.yaml"):
    """Apply profile settings to Kubernetes deployment"""
    try:
        with open(deployment_file, 'r') as f:
            deployment = yaml.safe_load(f)
        
        # Update replicas
        deployment['spec']['replicas'] = profile['replicas']
        
        # Update container resources
        container = deployment['spec']['template']['spec']['containers'][0]
        container['resources']['requests']['cpu'] = profile['cpu_requests']
        container['resources']['requests']['memory'] = profile['memory_requests']
        container['resources']['limits']['cpu'] = profile['cpu_limits']
        container['resources']['limits']['memory'] = profile['memory_limits']
        
        # Update environment variables
        env_vars = container.get('env', [])
        
        # Remove existing performance-related env vars
        env_vars = [env for env in env_vars if env['name'] not in [
            'BATCH_SIZE', 'BATCH_TIMEOUT', 'MAX_CONCURRENT_BATCHES',
            'UVICORN_WORKERS', 'UVICORN_BACKLOG', 'UVICORN_LIMIT_CONCURRENCY'
        ]]
        
        # Add new performance-related env vars
        env_vars.extend([
            {'name': 'BATCH_SIZE', 'value': str(profile['batch_size'])},
            {'name': 'BATCH_TIMEOUT', 'value': str(profile['batch_timeout'])},
            {'name': 'MAX_CONCURRENT_BATCHES', 'value': str(profile['max_concurrent_batches'])},
            {'name': 'UVICORN_WORKERS', 'value': str(profile['uvicorn_workers'])},
            {'name': 'UVICORN_BACKLOG', 'value': str(profile['uvicorn_backlog'])},
            {'name': 'UVICORN_LIMIT_CONCURRENCY', 'value': str(profile['uvicorn_limit_concurrency'])}
        ])
        
        container['env'] = env_vars
        
        # Write updated deployment
        with open(deployment_file, 'w') as f:
            yaml.dump(deployment, f, default_flow_style=False, sort_keys=False)
        
        print(f"✓ Applied profile to {deployment_file}")
        
    except FileNotFoundError:
        print(f"Error: Could not find {deployment_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error updating deployment: {e}")
        sys.exit(1)

def apply_profile_to_hpa(profile, hpa_file="k8s/hpa.yaml"):
    """Apply profile settings to HPA"""
    try:
        with open(hpa_file, 'r') as f:
            hpa = yaml.safe_load(f)
        
        # Update replicas
        hpa['spec']['minReplicas'] = profile['hpa_min_replicas']
        hpa['spec']['maxReplicas'] = profile['hpa_max_replicas']
        
        # Update metrics
        metrics = []
        
        # CPU metric
        cpu_metric = {
            'type': 'Resource',
            'resource': {
                'name': 'cpu',
                'target': {
                    'type': 'Utilization',
                    'averageUtilization': profile['hpa_cpu_target']
                }
            }
        }
        metrics.append(cpu_metric)
        
        # Memory metric if specified
        if 'hpa_memory_target' in profile:
            memory_metric = {
                'type': 'Resource',
                'resource': {
                    'name': 'memory',
                    'target': {
                        'type': 'Utilization',
                        'averageUtilization': profile['hpa_memory_target']
                    }
                }
            }
            metrics.append(memory_metric)
        
        hpa['spec']['metrics'] = metrics
        
        # Write updated HPA
        with open(hpa_file, 'w') as f:
            yaml.dump(hpa, f, default_flow_style=False, sort_keys=False)
        
        print(f"✓ Applied profile to {hpa_file}")
        
    except FileNotFoundError:
        print(f"Error: Could not find {hpa_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error updating HPA: {e}")
        sys.exit(1)

def apply_profile_to_dockerfile(profile, dockerfile="server/Dockerfile"):
    """Apply profile settings to Dockerfile"""
    try:
        with open(dockerfile, 'r') as f:
            lines = f.readlines()
        
        # Find and update ENV lines
        updated_lines = []
        for line in lines:
            if line.startswith('ENV BATCH_SIZE='):
                updated_lines.append(f'ENV BATCH_SIZE={profile["batch_size"]} \\\n')
            elif line.startswith('    BATCH_TIMEOUT='):
                updated_lines.append(f'    BATCH_TIMEOUT={profile["batch_timeout"]} \\\n')
            elif line.startswith('    MAX_CONCURRENT_BATCHES='):
                updated_lines.append(f'    MAX_CONCURRENT_BATCHES={profile["max_concurrent_batches"]} \\\n')
            elif line.startswith('    UVICORN_WORKERS='):
                updated_lines.append(f'    UVICORN_WORKERS={profile["uvicorn_workers"]} \\\n')
            elif line.startswith('    UVICORN_BACKLOG='):
                updated_lines.append(f'    UVICORN_BACKLOG={profile["uvicorn_backlog"]} \\\n')
            elif line.startswith('CMD ["uvicorn", "app:app",') and '--workers' in line:
                # Update the workers in CMD
                updated_lines.append(f'CMD ["uvicorn", "app:app", \\\n')
                updated_lines.append(f'     "--host", "0.0.0.0", \\\n')
                updated_lines.append(f'     "--port", "8080", \\\n')
                updated_lines.append(f'     "--workers", "{profile["uvicorn_workers"]}", \\\n')
                updated_lines.append(f'     "--timeout-keep-alive", "60", \\\n')
                updated_lines.append(f'     "--backlog", "{profile["uvicorn_backlog"]}", \\\n')
                updated_lines.append(f'     "--limit-concurrency", "{profile["uvicorn_limit_concurrency"]}", \\\n')
                updated_lines.append(f'     "--timeout-graceful-shutdown", "120"]\n')
            else:
                updated_lines.append(line)
        
        # Write updated Dockerfile
        with open(dockerfile, 'w') as f:
            f.writelines(updated_lines)
        
        print(f"✓ Applied profile to {dockerfile}")
        
    except FileNotFoundError:
        print(f"Error: Could not find {dockerfile}")
        sys.exit(1)
    except Exception as e:
        print(f"Error updating Dockerfile: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Apply performance profile to deployment')
    parser.add_argument('profile_name', nargs='?', default=None, 
                        help='Profile name to apply (default: production)')
    parser.add_argument('--profiles-file', default='performance_profiles.yaml',
                        help='Path to profiles YAML file')
    parser.add_argument('--list-profiles', action='store_true',
                        help='List available profiles')
    
    args = parser.parse_args()
    
    # Load profiles
    profiles_data = load_profiles(args.profiles_file)
    profiles = profiles_data['profiles']
    
    if args.list_profiles:
        print("Available profiles:")
        for name in profiles.keys():
            print(f"  - {name}")
        return
    
    # Determine profile to use
    if args.profile_name:
        if args.profile_name not in profiles:
            print(f"Error: Profile '{args.profile_name}' not found")
            print("Available profiles:")
            for name in profiles.keys():
                print(f"  - {name}")
            sys.exit(1)
        profile_name = args.profile_name
    else:
        profile_name = profiles_data.get('default_profile', 'production')
    
    profile = profiles[profile_name]
    
    print(f"Applying profile: {profile_name}")
    print("-" * 30)
    print(f"Batch Size: {profile['batch_size']}")
    print(f"Batch Timeout: {profile['batch_timeout']}s")
    print(f"Max Concurrent Batches: {profile['max_concurrent_batches']}")
    print(f"Uvicorn Workers: {profile['uvicorn_workers']}")
    print(f"Replicas: {profile['replicas']}")
    print(f"CPU Requests: {profile['cpu_requests']}")
    print(f"CPU Limits: {profile['cpu_limits']}")
    print(f"Memory Requests: {profile['memory_requests']}")
    print(f"Memory Limits: {profile['memory_limits']}")
    print()
    
    # Apply profile to all configuration files
    apply_profile_to_deployment(profile)
    apply_profile_to_hpa(profile)
    apply_profile_to_dockerfile(profile)
    
    print(f"\n✓ Profile '{profile_name}' applied successfully!")
    print("You can now deploy the updated configuration.")

if __name__ == "__main__":
    main()