# Glide

## Setup
This repository serves the the container root for the ROS2 workspace for the Jetbot code by a Polyhobbyist. The intention is for this repo to be cloned on the host operating system, and use Docker compose or VSCode DevContainers to start a ROS2 container to work in.

First, clone this repository onto your Jetson. The location doesn't matter.

### Using Docker directly
``` bash
setup.sh
Docker-compose -f Docker-compose.yaml up
```

### Using Docker directly
``` bash
docker exec -it jetbot_jetbot_1 /bin/bash
/ws/src/build_src.sh
```

### Using VSCode Dev containers
Ensure that you have the remote extension pack installed.
Open the Jetbot folder within VSCode. 
When VSCode asks to open the Devcontainer, [you say yes](https://youtu.be/jCe5vfQx50c?t=118).

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
