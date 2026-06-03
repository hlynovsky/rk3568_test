FROM arm64v8/debian:11-slim

RUN apt update && apt install -y \
        python3 \
        python3-venv \
        python3-dev \
        python3-pip \
        git \
        binutils \
        gcc-aarch64-linux-gnu \
        g++-aarch64-linux-gnu \
        binutils-aarch64-linux-gnu \
        libc6-dev-arm64-cross \
        dpkg-dev \
        devscripts \
        equivs \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip wheel setuptools && \
    /app/venv/bin/pip install -r requirements.txt

COPY . /app

RUN /app/venv/bin/pyinstaller --onefile \
    --name nms-sm-evb_tests \
    --hidden-import=ipaddress \
    /app/nms-sm-evb_tests/main.py

RUN mkdir -p /app/deb_package/DEBIAN \
             /app/deb_package/usr/bin \
             /app/deb_package/etc

COPY examples/configuration/nms-sm-evb_tests.json /app/deb_package/etc/
RUN cp /app/dist/nms-sm-evb_tests /app/deb_package/usr/bin/
COPY debian/control /app/deb_package/DEBIAN/
RUN dpkg-deb --build /app/deb_package /app/nms-sm-evb_tests_arm64.deb
RUN mkdir -p /app/dist && \
    cp /app/nms-sm-evb_tests_arm64.deb /app/dist/

WORKDIR /app/dist