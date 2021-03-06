.PHONY: clean data lint requirements download extract_dataframe extract_timeseries reports folders

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROFILE = default
PROJECT_NAME = data-science-exercise
PYTHON_INTERPRETER = python3
IPYNB_FILES=$(wildcard notebooks/*.ipynb)
HTML=$(IPYNB_FILES:.ipynb=.html)
HTML_REPORTS=$(HTML:notebooks/%=reports/%)
DOCKER_IMAGE=datascienceexercise

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

folders:
	mkdir -p data/raw
	mkdir -p data/interim
	mkdir -p data/processed
	mkdir -p reports

data/raw/australian_housing.json: folders
	$(PYTHON_INTERPRETER) -m australian_housing download

## Download raw json data from Australian Bureau of Statistics
download: data/raw/australian_housing.json

data/interim/australian_housing_decoded.csv: data/raw/australian_housing.json
	$(PYTHON_INTERPRETER) -m australian_housing extract_dataframe

## Decode raw json data and extract a (multidimensional) dataframe
extract_dataframe: data/interim/australian_housing_decoded.csv

data/processed/new_south_wales_housing.csv: data/interim/australian_housing_decoded.csv
	$(PYTHON_INTERPRETER) -m australian_housing extract_timeseries

## Extract New South Wales housing time series
extract_timeseries: data/processed/new_south_wales_housing.csv

## Execute and save notebooks
execute_notebooks: data/processed/new_south_wales_housing.csv
	jupyter nbconvert --execute notebooks/*.ipynb --inplace --to notebook

reports/%.html: notebooks/%.ipynb data/processed/new_south_wales_housing.csv
	jupyter nbconvert --config util/nbconvert_config.py --execute $< --output-dir reports/

## Generate reports from jupyter notebooks
reports: $(HTML_REPORTS)

## Delete all compiled Python files, data files and reports
clean:
	rm -f data/raw/australian_housing.json
	rm -f data/interim/australian_housing_decoded.csv
	rm -f data/processed/new_south_wales_housing.csv
	rm -f reports/*.html
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Set up python interpreter environment
create_environment:
ifeq (True,$(HAS_CONDA))
		@echo ">>> Detected conda, creating conda environment."
ifeq (3,$(findstring 3,$(PYTHON_INTERPRETER)))
	conda create --name $(PROJECT_NAME) python=3
else
	conda create --name $(PROJECT_NAME) python=2.7
endif
		@echo ">>> New conda env created. Activate with:\nsource activate $(PROJECT_NAME)"
else
	$(PYTHON_INTERPRETER) -m pip install -q virtualenv virtualenvwrapper
	@echo ">>> Installing virtualenvwrapper if not already intalled.\nMake sure the following lines are in shell startup file\n\
	export WORKON_HOME=$$HOME/.virtualenvs\nexport PROJECT_HOME=$$HOME/Devel\nsource /usr/local/bin/virtualenvwrapper.sh\n"
	@bash -c "source `which virtualenvwrapper.sh`;mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER)"
	@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"
endif

## Create docker image from Dockerfile
docker_image:
	docker build -t $(DOCKER_IMAGE) .

## Run pipeline in docker container output folders mounted 
run_docker:
	docker run -v $(shell pwd)/data:/opt/data-science-exercise/data -v $(shell pwd)/reports:/opt/data-science-exercise/reports --rm $(DOCKER_IMAGE)

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
