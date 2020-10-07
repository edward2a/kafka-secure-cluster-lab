.PHONY: help prepare certs

help:
	@echo -e "\n\tHelp! I need somebody, help!\n"

prepare:
	cd certs && terraform init

certs:
	cd certs && terraform apply -auto-approve -var env=lab
	cd certs && ENV=lab ./create-keystores.sh
	chmod o+r certs certs/stores certs/stores/*
	chmod o+r config/kafka config/kafka/*

