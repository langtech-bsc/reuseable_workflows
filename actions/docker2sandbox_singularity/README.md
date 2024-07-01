# Check hpc jobs

### Inputs

| variable | description|
|----|------------|
| job_id | Id of the job to check |
| job_name | Name of the jobs to check |
| remote_user | Remote user |
| remote_host | Remote host |


### Outputs
| variable | description|
|----|------------|
| exists | Whether the job exists or not |
| jobs | All running jobs id |



## Usage

```
    steps:

    - uses: webfactory/ssh-agent@v0.9.0
      with:
        ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}

    - name: Docker to sandbox
      id: docker2sandbox
        with:
          dir: ${{vars.GPFS_SINGULARITY_IMAGE_REGISTRY_PATH }}/sandboxs/${{ steps.globals.outputs.REPO_NAME }}
          name: ${{ steps.globals.outputs.JOB_BRANCH }}
          remote_user: ${{ secrets.REMOTE_USER }}
          remote_host: ${{ secrets.REMOTE_HOST }}
          overwrite: true
          sandbox: true
```