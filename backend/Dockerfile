FROM python:3.10

# install requirments
COPY requirements.txt /tmp/build/requirements.txt
RUN python -m pip install -r /tmp/build/requirements.txt

# install main application
COPY README.md /tmp/build/README.md
COPY pyproject.toml /tmp/build/pyproject.toml
COPY image_search /tmp/build/image_search
RUN cd /tmp/build && python -m pip install .

CMD ["uvicorn", "image_search:app", "--host", "0.0.0.0", "--port", "8080"]
