FROM python:3.10-slim

WORKDIR /workspace

RUN pip install --no-cache-dir \
    jupyterlab \
    delta-sharing \
    pandas \
    matplotlib

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]