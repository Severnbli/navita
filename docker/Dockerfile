# Navita: the official Kavita image with a web UI rebuilt from patched source.
#
# Build context: the Kavita source tree (release tag + patches/ applied).
# Extra build context "navita": a directory containing NAVITA-NOTICE.md.
# BASE_IMAGE must be the official image of the same version as the source tree.

ARG BASE_IMAGE=jvmilazz0/kavita:latest

# The UI bundle is platform independent, so build it once on the build host
FROM --platform=$BUILDPLATFORM node:24 AS ui
WORKDIR /src/UI/Web
COPY UI/Web/package.json UI/Web/package-lock.json ./
RUN npm ci --legacy-peer-deps
COPY UI/Web/ ./
RUN npm run prod

FROM ${BASE_IMAGE}
RUN rm -rf /kavita/wwwroot/*
COPY --from=ui /src/UI/Web/dist/browser/ /kavita/wwwroot/
COPY --from=ui /src/UI/Web/dist/3rdpartylicenses.txt /kavita/wwwroot/
COPY --from=navita NAVITA-NOTICE.md /kavita/NAVITA-NOTICE.md
