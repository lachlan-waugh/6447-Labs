#!/bin/bash

docker run -d --rm -h banana --name banana -v $(pwd):/ctf/work --cap-add=SYS_PTRACE plsiamlegit/6447-ubuntu:pwndocker

docker exec -it banana /bin/bash
