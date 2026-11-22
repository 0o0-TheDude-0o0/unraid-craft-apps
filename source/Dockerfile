# syntax=docker/dockerfile:1

FROM ghcr.io/linuxserver/baseimage-selkies:ubunturesolute AS runtime-base

# set version label
ARG BUILD_DATE
ARG VERSION
LABEL build_version="Linuxserver.io version:- ${VERSION} Build-date:- ${BUILD_DATE}"
LABEL maintainer="thelamer"

# title
ENV TITLE="Craft Apps" \
    NO_FULL=true \
    SELKIES_DESKTOP=true \
    PIXELFLUX_WAYLAND=true

RUN \
  echo "**** add icon ****" && \
  curl --fail --location --output \
    /usr/share/selkies/www/icon.png \
    https://raw.githubusercontent.com/linuxserver/docker-templates/master/linuxserver.io/img/artcraft-logo.png && \
  echo "**** install packages ****" && \
  add-apt-repository ppa:xtradeb/apps && \
  apt-get update && \
  apt-get install -y --no-install-recommends \
    caja \
    chromium \
    chromium-l10n \
    libegl1 \
    xdg-desktop-portal \
    xdg-desktop-portal-gtk && \
  echo "**** application tweaks ****" && \
  mv \
    /usr/bin/chromium \
    /usr/bin/chromium-real && \
  sed -i \
    's/^Icon=.*/Icon=system-file-manager-symbolic/' \
    /usr/share/applications/caja.desktop && \
  echo "**** cleanup ****" && \
  apt-get autoclean && \
  rm -rf \
    /config/.cache \
    /tmp/* \
    /usr/share/applications/caja-autorun-software.desktop \
    /usr/share/applications/caja-browser.desktop \
    /usr/share/applications/caja-computer.desktop \
    /usr/share/applications/caja-file-management-properties.desktop \
    /usr/share/applications/caja-folder-handler.desktop \
    /usr/share/applications/caja-home.desktop \
    /usr/share/applications/debian-uxterm.desktop \
    /usr/share/applications/debian-xterm.desktop \
    /usr/share/applications/footclient.desktop \
    /usr/share/applications/foot-server.desktop \
    /usr/share/applications/mate-about.desktop \
    /usr/share/applications/mate-color-select.desktop \
    /usr/share/applications/st.desktop \
    /var/lib/apt/lists/* \
    /var/tmp/*

FROM runtime-base AS app-source
COPY build/extract-app.sh /usr/local/bin/extract-app

FROM app-source AS app-photocraft
COPY versions/photocraft.lock /tmp/app.lock
RUN /usr/local/bin/extract-app photocraft x86_64

FROM app-source AS app-vectorcraft
COPY versions/vectorcraft.lock /tmp/app.lock
RUN /usr/local/bin/extract-app vectorcraft x86_64

FROM app-source AS app-filmcraft
COPY versions/filmcraft.lock /tmp/app.lock
RUN /usr/local/bin/extract-app filmcraft x86_64

FROM app-source AS app-lightcraft
COPY versions/lightcraft.lock /tmp/app.lock
RUN /usr/local/bin/extract-app lightcraft x86_64

FROM app-source AS app-pdfcraft
COPY versions/pdfcraft.lock /tmp/app.lock
RUN /usr/local/bin/extract-app pdfcraft x86_64

FROM app-source AS app-effectcraft
COPY versions/effectcraft.lock /tmp/app.lock
RUN /usr/local/bin/extract-app effectcraft x86_64

FROM app-source AS app-anicraft
COPY versions/anicraft.lock /tmp/app.lock
RUN /usr/local/bin/extract-app anicraft x86_64

FROM app-source AS app-designcraft
COPY versions/designcraft.lock /tmp/app.lock
RUN /usr/local/bin/extract-app designcraft x86_64

FROM app-source AS app-figcraft
COPY versions/figcraft.lock /tmp/app.lock
RUN /usr/local/bin/extract-app figcraft x86_64

FROM app-source AS app-texturecraft
COPY versions/texturecraft.lock /tmp/app.lock
RUN /usr/local/bin/extract-app texturecraft x86_64

FROM app-source AS app-materialcraft
COPY versions/materialcraft.lock /tmp/app.lock
RUN /usr/local/bin/extract-app materialcraft x86_64

FROM app-source AS app-soundcraft
COPY versions/soundcraft.lock /tmp/app.lock
RUN /usr/local/bin/extract-app soundcraft x86_64

FROM app-source AS app-wordcraft
COPY versions/wordcraft.lock /tmp/app.lock
RUN /usr/local/bin/extract-app wordcraft x86_64

FROM app-source AS app-deckcraft
COPY versions/deckcraft.lock /tmp/app.lock
RUN /usr/local/bin/extract-app deckcraft x86_64

FROM app-source AS app-cadcraft
COPY versions/cadcraft.lock /tmp/app.lock
RUN /usr/local/bin/extract-app cadcraft x86_64

FROM app-source AS app-gridcraft
COPY versions/gridcraft.lock /tmp/app.lock
RUN /usr/local/bin/extract-app gridcraft x86_64

FROM app-source AS app-craft-anything
COPY versions/craft-anything.lock /tmp/app.lock
RUN /usr/local/bin/extract-app craft-anything x86_64

FROM runtime-base

# each app is a separate reusable layer
COPY --link --from=app-photocraft /app-root/ /
COPY --link --from=app-vectorcraft /app-root/ /
COPY --link --from=app-filmcraft /app-root/ /
COPY --link --from=app-lightcraft /app-root/ /
COPY --link --from=app-pdfcraft /app-root/ /
COPY --link --from=app-effectcraft /app-root/ /
COPY --link --from=app-anicraft /app-root/ /
COPY --link --from=app-designcraft /app-root/ /
COPY --link --from=app-figcraft /app-root/ /
COPY --link --from=app-texturecraft /app-root/ /
COPY --link --from=app-materialcraft /app-root/ /
COPY --link --from=app-soundcraft /app-root/ /
COPY --link --from=app-wordcraft /app-root/ /
COPY --link --from=app-deckcraft /app-root/ /
COPY --link --from=app-cadcraft /app-root/ /
COPY --link --from=app-gridcraft /app-root/ /
COPY --link --from=app-craft-anything /app-root/ /

# add local files
COPY --link /root /

ARG BUILD_REVISION=local
LABEL maintainer="0o0-TheDude-0o0" \
      build_version="Unofficial ArtCraft ${BUILD_REVISION}" \
      org.opencontainers.image.source="https://github.com/0o0-TheDude-0o0/unraid-craft-apps" \
      org.opencontainers.image.documentation="https://github.com/0o0-TheDude-0o0/unraid-craft-apps/blob/main/README.md" \
      org.opencontainers.image.revision="${BUILD_REVISION}" \
      org.opencontainers.image.description="Unofficial x86-64 ArtCraft suite based on LinuxServer.io Craft Apps"

# ports and volumes
EXPOSE 3001

VOLUME /config
