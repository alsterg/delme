all: build run

build:
	docker build -t mwam .

run:
	docker run mwam
