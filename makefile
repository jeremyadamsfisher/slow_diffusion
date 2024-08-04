.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

release:  ## bump patch version
	@bump-my-version bump patch
	@git push
	@git push --tags

lint:  ## clean up the source code
	@isort .
	@black .

preview:  ## preview docs server
	@PYTHONPATH=. nbdev_preview

readme:  ## update the readme
	@PYTHONPATH=. nbdev_prepare

pin:  ## pin python deps
	@python -m piptools compile -o requirements.txt requirements.in