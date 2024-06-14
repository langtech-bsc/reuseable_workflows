import * as core from "@actions/core";

export default async function run(): Promise<void> {
  try {

    const requiredSecrets: string = core.getInput('requiredSecrets')
    const requiredVars: string = core.getInput('requiredVars')

    const secretsJson = core.getInput("secrets");
    const varsJson = core.getInput("vars");

    console.log(secretsJson)

    const secretsArray = requiredSecrets.split(",");
    const varsArray = requiredVars.split(",");

    let secretsError = false;
    let varsError = false;

    // Check for required secrets
    for (const secret of secretsArray) {
      const secretValue = core.getInput(secret);
      if (!secretValue) {
        core.error(`Required secret '${secret}' is not set.`);
        secretsError = true;
      }
    }

    // Check for required environment variables
    for (const variable of varsArray) {
      const variableValue = process.env[variable];
      if (!variableValue) {
        core.error(`Required environment variable '${variable}' is not set.`);
        varsError = true;
      }
    }

    // Set outputs
    core.setOutput("secrets_error", secretsError.toString());
    core.setOutput("vars_error", varsError.toString());

    // Exit with error if any errors were found
    if (secretsError || varsError) {
      core.setFailed("Required secrets or environment variables are missing.");
    }
  } catch (error: any) {
    core.setFailed(error.message);
  }
}

run();
