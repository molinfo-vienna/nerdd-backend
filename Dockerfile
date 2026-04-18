#
# BUILD APPLICATION
#
FROM mambaorg/micromamba:2.0.5 AS build

# necessary to display the image on Github
LABEL org.opencontainers.image.source="https://github.com/molinfo-vienna/nerdd-backend"

# using the root user during the build stage
USER root

# Necessary, so Docker doesn't buffer the output and that we can see the output 
# of the application in real-time.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY environment.yml requirements.txt ./

# --mount creates a cache directory for conda, so that it doesn't have to download the dependencies 
#   every time we build the image
RUN --mount=type=cache,target=/root/.mamba/pkgs \
    # create the conda environment in a fixed path so it can be copied to the runtime image
    micromamba env create --copy -p /env -f environment.yml && \
    # remove the cache and the tarballs of the packages
    micromamba clean --all --yes

# --mount creates a cache directory for pip, so that it doesn't have to download the dependencies 
#   every time we build the image
RUN --mount=type=cache,target=/root/.cache/pip \
    micromamba run -p /env pip install -r requirements.txt

COPY . .
RUN micromamba run -p /env pip install --no-deps .

#
# RUN APPLICATION
#
FROM gcr.io/distroless/base-debian12

COPY --from=build /env /env

ENTRYPOINT ["/env/bin/python3", "-m", "nerdd_backend.main"]
