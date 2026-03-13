UID=$(shell id -u)
GID=$(shell id -g)
IMAGE=pdiow-python

build:
	docker build --build-arg UID=$(UID) --build-arg GID=$(GID) -t $(IMAGE) .

run_jupyter:
	docker run --rm -p 7777:7777 -v "$(PWD):/app" -e PYTHONPATH=/app --user "$(UID):$(GID)" $(IMAGE) python -m jupyterlab --ip=0.0.0.0 --port=7777 --no-browser --NotebookApp.token='password' --NotebookApp.password='password'