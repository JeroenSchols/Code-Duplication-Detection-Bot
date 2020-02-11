FROM python:3

 ADD entry_script.py /
 ADD parser.py /
 ADD vector_representer.py /
 ADD trace_link_generator.py /
 ADD evaluator.py /
 ADD probabilistic_model.py /

 ADD requirements.txt /

 RUN pip install -r requirements.txt
 RUN python -W ignore -m nltk.downloader punkt
 RUN python -W ignore -m nltk.downloader stopwords

 ENTRYPOINT [ "python", "./entry_script.py" ]   