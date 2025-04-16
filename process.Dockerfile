FROM storytrack-base:latest

COPY src/storytrack/data_processing.py .

RUN mkdir -p gpx_files tmp

CMD ["python", "data_processing.py"]