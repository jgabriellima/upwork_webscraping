FROM selenium/standalone-firefox
USER root
RUN sudo apt-get update
RUN sudo apt install -y software-properties-common
RUN sudo add-apt-repository ppa:deadsnakes/ppa
RUN sudo apt install -y python3.7
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 \
    curl unzip zlib1g-dev xz-utils gcc wget \
    xvfb

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 10

# -- Install application
RUN mkdir /opt/app
ENV PATH="/opt/app/bin:${PATH}"
ENV IS_DOCKER_INSTANCE Yes
COPY . /opt/app
WORKDIR /opt/app
RUN sudo chmod 777 -R /opt/app/

# -- Install Python packages with pipenv
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN sudo python get-pip.py
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade pipenv
RUN pipenv install --deploy --system --dev

USER seluser
# -- Run application
CMD ["python", "app.py"]