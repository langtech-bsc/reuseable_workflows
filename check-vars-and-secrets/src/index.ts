import * as core from "@actions/core";

export default async function run(): Promise<void> {
  try {

    const requiredSecrets: string = core.getInput('must_include')
    const secretsJson = core.getInput("json", { required: true });
    const type = core.getInput("type", { required: true });

    let secrets: Record<string, string>
    try {
      secrets = JSON.parse(secretsJson)
    } catch (e) {
      throw new Error(`Cannot parse JSON.
      Make sure you add the following to this action:
      with:
          json: \${{ toJSON(secrets) }}
                  or
          json: \${{ toJSON(vars) }}
        `)
    }

    let secretsError = false;

    // Check for required secrets
    for (const key of requiredSecrets.split(",")) {
      const secretValue = secrets[key.trim()];
      if (!secretValue) {
        core.error(`Required ${type} '${key}' is not set.`);
        secretsError = true;
      }
    }

    // Set outputs
    core.setOutput("secrets_error", secretsError.toString());
    // Exit with error if any errors were found
    if (!secretsError) {
      for (const key of Object.keys(secrets)) {
        core.exportVariable(key, secrets[key])
        core.info(`Exported secret ${key}`)
      }
    }

  } catch (error: any) {
    core.setFailed(error.message);
  }
}

run();
