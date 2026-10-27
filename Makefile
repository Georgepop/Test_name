data:
	python -m src.cli data

train:
	python -m src.cli train

baseline:
    python -m src.cli baseline

predict:
	python -m src.cli predict

eval:
	python -m src.cli eval

effect:
    python -m src.cli effect

test:
	pytest -q
