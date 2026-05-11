FROM alpine
ENV MY_VAR='{"key": "value'\''"}'
RUN echo "$MY_VAR"
