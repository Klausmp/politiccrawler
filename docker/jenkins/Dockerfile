FROM jenkins/jenkins:lts

# Switch to root to install Python
USER root

# Update package lists and install Python3 and pip
RUN apt update && apt install -y \
    python3 \
    python3-pip \
 && rm -rf /var/lib/apt/lists/*

# Optionally, install a specific version of Python if needed (this may require adding external repositories or building from source)
# For example, if the default version isn’t what you need, you may have to build Python from source.

# Switch back to the jenkins user
USER jenkins
