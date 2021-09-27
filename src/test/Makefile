PYTHON_LIB=../lib


syntax: clean
	PYTHONPATH=${PYTHON_LIB} python3 -m py_compile ../bin/qr_alchemy
	PYTHONPATH=${PYTHON_LIB} ./TestSyntax.py -v

basic: syntax
	PYTHONPATH=${PYTHON_LIB} ./TestGenerate.py -v
	PYTHONPATH=${PYTHON_LIB} ./TestPlugins.py -v
	
clean:
	rm -rf tmp/
