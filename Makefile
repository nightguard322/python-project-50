install:
	uv sync
run-gendiff:
	uv run gendiff file1.json file2.json
build:
	uv build
package-install:
	uv tool install dist/hexlet_code-0.1.0-py3-none-any.whl

test:
	uv run pytest
	
test-coverage:
	uv run pytest --cov=hexlet-code