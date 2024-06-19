run-gh-run-test-job-enhanced-launch-job:
	gh act -j test-job-enhanced-launch-job -W .github/workflows/test_enhanced_launch_job.yml --secret-file my.secrets --var-file .env --no-cache-server

run-gh-run-test-addons-action:
	gh act -j test-addons-action -W .github/workflows/test_addons_action.yml --secret-file my.secrets --var-file .env --no-cache-server