run-gh-run-test-job-enhanced-launch-job:
	gh act -j test-job-enhanced-launch-job --secret-file my.secrets --var-file .env --no-cache-server