FROM python:3.9.5-buster
LABEL project="blog website"
# import code 
COPY . /app 

# changing working dir 
WORKDIR /app 

#installing packages 
RUN pip3 install --no-cache-dir -r requirements.txt 

# env
ENV PORT 5001
# Expose port 
EXPOSE $PORT 

# running python file 
ENTRYPOINT [ "python3" ]
CMD ["main.py"]
