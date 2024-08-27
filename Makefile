container_name = webserver
output_file = test_results.log

# when the container is up and running, root url should be available
health_check_url = http://localhost/ 

test:
	# pre-setup
	docker compose down
	
	# setup
	docker compose --env-file .env.test up --build -d
	until curl -s ${health_check_url} > /dev/null; do \
		echo 'Waiting for service to be ready...'; \
		sleep 1; \
	done

	# run tests
	docker exec ${container_name} bash -c "pytest > /tmp/${output_file} 2>&1 || true"

	# report
	docker cp ${container_name}:/tmp/${output_file} ${output_file}
	
	# teardown :: app level teared-down is carried out by the 'run tests' step
	docker compose down
	@clear
	@echo "The test results are available @ ${output_file}."
run:
	docker compose up --build



