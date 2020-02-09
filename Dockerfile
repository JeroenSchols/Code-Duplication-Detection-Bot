FROM python:3

 ADD entry_script.py /
 ADD parser.py /
 ADD requirements.txt /

 RUN pip install -r requirements.txt
 RUN python -m nltk.downloader punkt
 RUN python -m nltk.downloader stopwords

 ENTRYPOINT [ "python", "./entry_script.py" ]   