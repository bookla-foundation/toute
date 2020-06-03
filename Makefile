.PHONY: test install pep8 release clean doc

test: install
	pipenv run python -m pytest -v --cov=toute -l --tb=short --maxfail=1 tests/ -vv

test-ci: pep8
	py.test -v --cov=toute -l --tb=short --maxfail=1 tests/ -vv

install:
	pipenv run python setup.py develop

pep8:
	@flake8 lib/toute --ignore W504 --ignore=F403 --ignore F821 --ignore F405

release: test
	@python setup.py sdist bdist_wheel upload

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;

epydoc:
	@git up && git checkout master
	@epydoc --html toute -o /tmp/toute_docs
	@git checkout gh-pages
	@cp -r /tmp/toute_docs docs
	@git add docs/
	@git commit -am"updated docs"
	@git push -u origin gh-pages
	@git checkout master
