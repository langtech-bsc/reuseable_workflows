#===========Workflows========================


#===========TEST workflows===================
run-gh-run-test-workflow-job-enhanced-launch-job:
	gh act -j test-workflow-job-enhanced-launch-job -W .github/workflows/test_workflow_enhanced_launch_job.yml --secret-file my.secrets --var-file .env --no-cache-server

#===========TEST actions===================
run-gh-run-test-action-addons:
	gh act -j test-action-addons -W .github/workflows/test_action_addons.yml --secret-file my.secrets --var-file .env --no-cache-server

run-gh-run-test-action-get_repo_and_ref_name:
	gh act -j test-action-get-repo-and-ref-name -W .github/workflows/test_action_get_repo_and_ref_name.yml --secret-file my.secrets --var-file .env --no-cache-server