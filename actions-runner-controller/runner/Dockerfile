FROM ghcr.io/actions/actions-runner:2.317.0

USER root

RUN apt-get update && apt-get install -y \
   openssh-client \
   python3-pip \
   && rm -rf /var/lib/apt/lists/

USER runner

ENV PATH "$PATH:/home/runner/.local/bin"

RUN python3 -m pip install --upgrade pip
RUN pip install --user hpc-rocket==0.6.1 mlflow==2.14.1 sysrsync==1.1.1 python-dotenv==1.0.1 --no-cache-dir