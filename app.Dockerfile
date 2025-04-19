FROM storytrack-base:latest

# Set timezone sinze Docker interprets time in GPX files to be relative to its timezone
ENV TZ=Europe/Stockholm
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY src/storytrack/app.py .
COPY src/storytrack/delta_reader.py .
COPY src/storytrack/dash_components.py .
COPY src/storytrack/photo_process.py .
COPY assets/ ./assets/

RUN mkdir -p tmp

EXPOSE 8050

CMD ["python", "app.py"]