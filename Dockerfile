FROM python:3.8-slim-buster

COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
