#!/usr/bin/env python

import argparse
from time import sleep
import sysrsync
from os import environ
import traceback
import mlflow
from dotenv import load_dotenv, set_key
from pathlib import Path

tasks = ["schedule", "sync", "stop", "artifact_url"]

variables_name = {
    "url": "TRAKING_URL",
    "experiment": "EXPERIMENT",
    "run_name": "RUN_NAME",
    "run_id": "RUN_ID",
    "user": "REMOTE_USER",
    "host": "REMOTE_HOST",
    "src": "REMOTE_SOURCE_PATH",
    "destination": "DESTINATION",
}

tasks_and_variables = {
    "schedule": ["url", "experiment", "run_name"],
    "sync": ["url", "experiment", "user", "host", "src", "run_id", "destination"],
    "stop": ["url", "experiment", "user", "host", "src", "run_id", "destination"],
    "artifact_url": ["url", "experiment", "run_id"],
}

def get_env_variables(file):
    load_dotenv(Path(file))
    return { key: environ.get(name, None) 
            for key, name in variables_name.items() }
        

def check_variables(task, variables, file):
    required = [ variables_name[var] for var in tasks_and_variables[task] if not variables[var] ]
    if len(required) > 0:
        raise  Exception(f"Missing following variables from the environment file '{file}': {required} ")


class MlflowLogging():
    def __init__(self, tracking_uri, experiment_name) -> None:
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)

    def schedule(self, run_name, env_file):
        run = mlflow.start_run(run_name=run_name)
        load_dotenv()
        filtered_vars = {name: value for name, value in environ.items() if name.startswith(('JOB_', 'SLURM_', 'GPFS_', 'GITHUB_'))}

        env_vars = dict(sorted(filtered_vars.items(), key=lambda item: (
            1 if item[0].startswith('JOB_') else 
            2 if item[0].startswith('SLURM_') else 
            3 if item[0].startswith('GPFS_') else 
            4 if item[0].startswith('GITHUB_') else 5
        )))

        mlflow.log_params(env_vars)
        mlflow.end_run('SCHEDULED')
        set_key(Path(env_file), key_to_set="RUN_ID", value_to_set=run.info.run_id)
        return run.info.run_id

    def sync(self, remote_user, remote_host, source, destination):
        try:
            sysrsync.run(
                    source_ssh=f"{remote_user}@{remote_host}",
                    source=source,
                    destination=destination,
                    strict_host_key_checking=False,
                    options=['-avh'])

            mlflow.log_artifacts(destination)
            
        except:
            traceback.print_exc()

    
    def syncloop(self, remote_user, remote_host, source, destination, run_id):
        mlflow.start_run(run_id=run_id)
        while True:
            self.sync(remote_user, remote_host, source, destination)
            sleep(15)

    def get_artifact_url(self, run_id):
        run = mlflow.get_run(run_id=run_id)
        return f"{mlflow.get_tracking_uri()}/#/experiments/{run.info.experiment_id}/runs/{run.info.run_id}/artifacts"

    def stop(self, remote_user, remote_host, source, destination, run_id, failed=False):
        mlflow.start_run(run_id=run_id)
        self.sync(remote_user, remote_host, source, destination)
        if failed:
            mlflow.end_run('FAILED')
        else:
            mlflow.end_run()

def main(task, variables, env_file, failed):
    client = MlflowLogging(variables["url"], variables["experiment"])
    if task == 'schedule':
        client.schedule(variables["run_name"], env_file)
    
    elif task == 'sync':
        client.syncloop(variables["user"], variables["host"], variables["src"], variables["destination"], variables["run_id"])
    
    elif task == 'stop':
        client.stop(variables["user"], variables["host"], variables["src"], variables["destination"], variables["run_id"], failed)
    
    elif task == 'artifact_url':
        url = client.get_artifact_url(variables["run_id"])
        print(url)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mlflow logging')
    parser.add_argument('-t', '--task', required=True, choices=tasks, help=f'Permited tasks: {tasks}')
    parser.add_argument('-f', '--failed', required=False, default=False, action='store_true' ,help='Experiment Name')
    parser.add_argument('-e', '--env', required=False, default=".env_mlflow", help='Env File')
    args = parser.parse_args()
    variables = get_env_variables(args.env)
    check_variables(args.task, variables, args.env)
    main(args.task, variables, args.env, args.failed)

    


