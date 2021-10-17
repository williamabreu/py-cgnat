# Use this makefile to run development procedures.

style: black flake8 isort pydocstyle mypy requirements
	@echo "🎉 style passed!"

test: style
	python setup.py test
	@echo "🎉 test passed!"

build: test clean
	python setup.py sdist bdist_wheel
	@echo "📦 build complete."

publish: build
	pip install --upgrade twine
	twine upload dist/*
	@echo "🎯 publish complete."

black:
	black . --line-length=79
	@echo "✅ black done."

flake8:
	flake8
	@echo "✅ flake done."

isort:
	isort . --profile black
	@echo "✅ isort done."

pydocstyle:
	pydocstyle
	@echo "✅ pydocstyle done."

mypy:
	mypy
	@echo "✅ mypy done."

requirements:
	poetry export --without-hashes --output requirements.txt
	poetry export --dev --without-hashes --output requirements.dev.txt
	@echo "✅ requirements done."

clean:
	pyclean -v .
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	@echo "♲ clean done."
