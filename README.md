# ArtCraft All Apps for Unraid

An unofficial x86-64 container with all 17 ArtCraft desktop apps in one
browser-accessible desktop. It is based on LinuxServer.io's Craft Apps image.
This project is not maintained by LinuxServer.io or the ArtCraft team.

## Install on Unraid

The container image is `ghcr.io/0o0-thedude-0o0/docker-craft-apps:latest`.
The template is [`templates/artcraft-all-apps.xml`](templates/artcraft-all-apps.xml).
For a manual installation, copy that XML file to
`/boot/config/plugins/dockerMan/templates-user/` on the Unraid server, then
choose `artcraft-all-apps` from **Docker → Add Container**.

The template maps HTTPS port 3001 and `/config` to
`/mnt/user/appdata/artcraft-all-apps`. Open `https://YOUR-UNRAID-IP:3001/`.
The built-in certificate is self-signed, so a browser warning is expected.
Keep the desktop on a trusted local network unless you add a reverse proxy
with strong authentication. The desktop includes a terminal.

## Source and attribution

The exact packaging source used for the current image is in the
[versioned source archive](sources/source-5058d437a027.tar.gz).
[`SOURCE_COMMIT`](SOURCE_COMMIT) records the build repository revision. The
original packaging is by LinuxServer.io; the
application packages come from the ArtCraft team. The packaging source license
is in [`LICENSE`](LICENSE). The apps and third-party components retain their
own licenses and notices.

Published image versions and their corresponding packaging source:

| Image tag | Build revision | Public source snapshot |
| --- | --- | --- |
| `sha-5058d437a027` | `5058d437a0279626538b009b81473708f957af07` | [Source archive](sources/source-5058d437a027.tar.gz) |
| `sha-d4288ac9567e` | `d4288ac9567ea2ddb3902702da0673f02cd9fa89` | [Source archive](sources/source-d4288ac9567e.tar.gz) |

Report issues with this image or template in this repository's Issues tab.
For application bugs, use the relevant ArtCraft upstream repository.
