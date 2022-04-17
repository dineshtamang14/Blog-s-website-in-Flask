FROM python:3.9.5-buster

# import code 
ADD . /app 

# changing working dir 
WORKDIR /app 

#installing packages 
RUN pip3 install -r requirements.txt 

# Expose port 
EXPOSE 5001     

# running python file 
CMD ["python3", "main.py"]
