# Check hpc jobs

### Inputs

| variable | description|
|-----|------------|
| dir | Directory where to save |
| name | Name of the sigularity or sandbox (.sif will be added if sandbox=false) |
| sandbox | True or False, whether it's a sandbox or singularity (Default: False) |
| overwrite | True or False, whether to overwrite sandbox/singularity or not (Default: False) |
| remote_user | Remote user |
| remote_host | Remote host |

### Outputs
| variable | description|
|----|------------|
| exists | true, if sandbox/singularity already exist and overwirte=false|



## Usage
The run must be able to build a docker image.
```
    steps:

    - uses: webfactory/ssh-agent@v0.9.0
      with:
        ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}

    - uses: langtech-bsc/magma/actions/docker2sandbox_singularity@main
      with:
        dir: ${{vars.GPFS_SINGULARITY_IMAGE_REGISTRY_PATH }}/sandboxs
        name: jupyter
        remote_user: ${{ secrets.REMOTE_USER }}
        remote_host: ${{ secrets.REMOTE_HOST }}
        sandbox: true
```