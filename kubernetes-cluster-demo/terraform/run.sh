#!/bin/bash

# Check if the environment variable HCLOUD_TOKEN is set
if [ -z "$HCLOUD_TOKEN" ]; then
    echo "Error: HCLOUD_TOKEN environment variable is not set"
    exit 1
else
   echo -e "HCLOUD_TOKEN: \033[32m✔️\033[0m" 
fi

# Check if Terraform is installed and install it if not
if ! command -v terraform &> /dev/null; then
    echo "Error: Terraform is not installed. please go to https://developer.hashicorp.com/terraform/downloads and install it"
else
   echo -e "Terraform: \033[32m✔️\033[0m" 
fi

# Check if kubectl is installed and install it if not
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed please go to https://kubernetes.io/docs/tasks/tools/ and install it"
else
   echo -e "Kubectl: \033[32m✔️\033[0m" 
fi

# Initialize the Terraform project
if [ ! -d ".terraform" ]; then
    terraform init
else
    echo -e "Terraform initialized: \033[32m✔️\033[0m" 
fi

# Copy terraform.tfvars.example to terraform.tfvars if it does not exists
if [ -e "terraform.tfvars.example" ] && [ ! -e "terraform.tfvars" ]; then
    cp terraform.tfvars.example terraform.tfvars
else
    echo -e "Terraform vars(terraform.tfvars): \033[32m✔️\033[0m"     
fi

# Extract and check ssh_public_key_file value
ssh_key_file=$(grep -E "^ssh_public_key_file" terraform.tfvars | awk -F= '{gsub(/[ \047"]/, "", $2); print $2}' | sed 's/^[ \t]*//;s/[ \t]*$//')

ssh_key_file="${ssh_key_file/#\~/$HOME}"


if ! [ -f "$ssh_key_file" ]; then
    echo "Error: SSH public key file '$ssh_key_file' not found."
    echo "Please make sure the file exists and has appropriate permissions"
    exit 1
else
    echo -e "Using ssh: \033[32m$ssh_key_file\033[0m"
    echo -e "== Please make sure that this key is unique in your Hetzner Cloud account === \n"
fi

# Show a summary of the Terraform variables
echo "Summary of Terraform variables (terraform.tfvars):"
awk -F' *= *' '/^[^#]/ {printf "| %-40s | %-20s |\n", $1, $2}' terraform.tfvars
printf "+------------------------------------------+----------------------+\n"

kubeconfig(){
    echo "export kubernetes configuration"

    # Extract cluster_name from terraform.tfvars
    cluster_name=$(grep -E "^cluster_name" terraform.tfvars | awk -F= '{gsub(/[ \047"]/, "", $2); print $2}' | sed 's/^[ \t]*//;s/[ \t]*$//')
    
    # Generate kubeconfig filename
    kubeconfig_file="${cluster_name}-kubeconfig"
    
    # Export KUBECONFIG as an environment variable
    export KUBECONFIG="$PWD/$kubeconfig_file"
    
    source <(echo export KUBECONFIG="$KUBECONFIG")
    echo "KUBECONFIG is set to '$PWD/$kubeconfig_file'"
    echo "done"
}

run() {
    local choice
    read -p "What do you want to do? (1: plan, 2: apply, 3: save infra, 4:deploy cluster, 5: export kubeconfig, other: exit): " choice
    case $choice in
        1)
            # Run terraform plan
            terraform plan
            run
            ;;
        2)
            # Run terraform apply
            terraform apply
            if [ $? -eq 0 ]; then
            echo "Saving infrastructure..."
                terraform output -json > tf.json
                echo "Deploying cluster"
                kubeone apply -m kubeone.yaml -t tf.json
                kubeconfig
            else
                echo "Terraform apply failed."
                run
            fi
            ;;
        3)
            # Run save output
            echo "Saving infrastructure..."
            terraform output -json > tf.json
            echo -e "done"
            run
            ;;        
        4)
            # deploy cluster
            echo "Deploying cluster"
            kubeone apply -m kubeone.yaml -t tf.json
            echo -e "done"
            run
            ;;             
        5)
            # export kubeconfig
            kubeconfig
            run
            ;;                   
        *)
            echo "Invalid exiting..."
            echo "The script has finished."
            exit 0;
            ;;
    esac
}

run

