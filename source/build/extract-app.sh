#!/usr/bin/env bash
set -euo pipefail

app="$1"
arch="$2"
mapfile -t release < /tmp/app.lock
tag="${release[0]}"
case "$arch" in
  x86_64) expected_sha="${release[1]}" ;;
  aarch64) expected_sha="${release[2]}" ;;
  *) echo "Unsupported architecture: $arch" >&2; exit 1 ;;
esac

version="${tag#v}"
deb="/tmp/${app}.deb"
url="https://github.com/storytold/${app}/releases/download/${tag}/${app}-${version}-linux-${arch}.deb"
curl --fail --location --retry 3 --output "$deb" "$url"
printf '%s  %s\n' "$expected_sha" "$deb" | sha256sum --check --status

apt-get --simulate install --yes --no-install-recommends "$deb" > /tmp/install-plan
if awk -v app="$app" '$1 == "Inst" && $2 != app { found = 1; print "Missing shared dependency: " $2 > "/dev/stderr" } END { exit !found }' /tmp/install-plan; then
  exit 1
fi

dpkg-deb --extract "$deb" /app-root
test -x "/app-root/usr/bin/${app}"
test -f "/app-root/usr/share/applications/ai.storyteller.${app}.desktop"
