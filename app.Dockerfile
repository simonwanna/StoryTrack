FROM storytrack-base:latest

COPY src/storytrack/app.py .
COPY src/storytrack/delta_reader.py .
COPY src/storytrack/dash_components.py .

RUN mkdir -p tmp

EXPOSE 8050

CMD ["python", "app.py"]