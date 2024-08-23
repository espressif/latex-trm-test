# Start building the image for TeX Live image
FROM texlive/texlive:TL2021-historic

# Install Python script dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y python3-openpyxl python3-urllib3 python3-gitlab python3-pip python3-yaml

# Install TeX Live dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends libfontconfig

# Remove the downloaded package index files by previous apt-get commands
RUN rm -rf /var/lib/apt/lists/*
