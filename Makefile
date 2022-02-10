

build: clean
	python3 setup.py py2app -A

.PHONY: clean

clean:
	rm -rf build dist
