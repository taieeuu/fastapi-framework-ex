PYTEST_OPTS ?= -n auto --dist=loadfile
PYTEST_AND_OPTS = pytest ${PYTEST_OPTS}
PYTEST = pytest

ENV ?= dev
TAG ?= latest

define get_api_base_url
$(shell if [ "$(ENV)" = "uat" ]; then \
    echo "<uat_ip>:8080"; \
elif [ "$(ENV)" = "prod" ]; then \
    echo "<prod_ip>:8080"; \
elif [ "$(ENV)" = "dev" ]; then \
    echo "http://localhost:8080"; \
else \
    echo "Invalid ENV value. Must be 'uat' or 'prod' or 'dev'" >&2; \
    exit 1; \
fi)
endef

.PHONY: test_e2e
test_e2e:
	@echo "Running e2e tests in $(ENV) environment"
	$(eval API_BASE_URL := $(call get_api_base_url))
	@echo "API_BASE_URL: $(API_BASE_URL)"
	$(PYTEST) tests/da_app/end2end/ --API_BASE_URL=$(API_BASE_URL) --ENV=${ENV}

.PHONY: test_unit
test_unit:
	pytest -m unit

.PHONY: archive
archive:
	@echo "Tags: $(TAG) ENV: $(ENV) DEPLOY: $(DEPLOY)"
	bash ./shell_scripts/archive.sh $(ENV) $(TAG) $(DEPLOY)

.PHONY: deploy
deploy:
	bash ./shell_scripts/deploy.sh $(local_file_path) $(remote_ip_address)

.PHONY: update_env
update_env:
	bash ./shell_scripts/update_env.sh $(ENV)

.PHONY: unit_test
unit_test:
	$(PYTEST) tests/da_app/unit/ ${CODECOV_OPTS}
