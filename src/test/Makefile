PYTHON_LIB=../lib


syntax: clean
	PYTHONPATH=${PYTHON_LIB} python3 -m py_compile ../bin/qr_alchemy
	PYTHONPATH=${PYTHON_LIB} ./TestSyntax.py -v

basic: syntax clean
	PYTHONPATH=${PYTHON_LIB} ./TestGenerate.py -v
	PYTHONPATH=${PYTHON_LIB} ./TestPlugins.py -v
	PYTHONPATH=${PYTHON_LIB} ./TestConfig.py -v
	PYTHONPATH=${PYTHON_LIB} ./TestProcess.py -v
	PYTHONPATH=${PYTHON_LIB} ./TestSaved.py -v
	make clean
	
clean:
	rm -rf tmp/
