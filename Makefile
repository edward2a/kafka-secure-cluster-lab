
help:
	@echo -e "\n\tHelp! I need somebody, help!\n"

prepare:
	chmod o+r certs certs/stores certs/stores/*
	chmod o+r config/kafka config/kafka/*
