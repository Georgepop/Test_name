data:
	python -m src.cli data

train:
	python -m src.cli train

predict:
	python -m src.cli predict

eval:
	python -m src.cli eval

test:
	pytest -q
