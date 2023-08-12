.venv/bin/python -m nuitka --standalone --lto=no \
--include-data-dir=../react-frontend/build=build \
--include-data-dir=../ansible=toolbox/ansible \
--include-data-dir=src/toolbox/templates=toolbox/templates \
--include-package-data=xstatic.pkg --include-package-data=terminado \
--include-package=xstatic src/toolbox/main.py

# rename main.dist to standalone
mv main.dist toolbox