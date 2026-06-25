import yaml
import subprocess
import sys

def update_image_version(file_path, new_image):
    print(f"Opening YAML file: {file_path}")
    
    with open(file_path, 'r') as file:
        manifest = yaml.safe_load(file)
    
    print(f"Modifying the container image to {new_image}...")
    manifest['spec']['template']['spec']['containers'][0]['image'] = new_image
    
    with open(file_path, 'w') as file:
        yaml.dump(manifest, file, default_flow_style=False)
        
    print(f"Successfully saved {file_path}!")

def deploy_to_gcp(file_path):
    print(f"\n--- DEPLOYING TO GOOGLE CLOUD ---")
    print(f"Running: kubectl apply -f {file_path}")
    
    try:
        # Use subprocess to push the YAML to the GKE cluster
        subprocess.run(["kubectl", "apply", "-f", file_path], check=True)
        print("Successfully deployed to GCP!")
        print("---------------------------------\n")
    except subprocess.CalledProcessError as e:
        print(f"Failed to deploy to GCP! Ensure your cluster is running. Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    yaml_file = "config.yaml"
    # 1. Update the YAML file automatically
    update_image_version(yaml_file, "nginx:1.22.0")
    
    # 2. Push it to the GKE cluster automatically
    deploy_to_gcp(yaml_file)
