help:
	@echo -e "\n\tHelp!!! I need somebody, help!\n"

check_var_env:
	@if [ -z "$${ENV}" ]; then \
		echo "WARN: ENV not defined, using default of ENV=lab." ;\
		#echo "ERROR: ENV not defined, please invoke make <target> ENV=<value>." ;\
		#exit 1 ;\
	fi

clean: check_var_env
	tf destroy -var env=$${ENV:-lab}
	rm -f stores/*

all: check_var_env
	tf apply -var env=$${ENV:-lab}
	ENV=$${ENV:-lab} ./create-keystores.sh
