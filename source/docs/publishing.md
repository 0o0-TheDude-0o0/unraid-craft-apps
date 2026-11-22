# Publishing the unofficial x86-64 image

The image name is `ghcr.io/0o0-thedude-0o0/docker-craft-apps`.

The release checker runs every six hours and can also be started manually with
`dry_run` enabled. It reads the latest stable release for every app in
`versions/`, checks that the x86-64 Debian package and its SHA-256 digest are
present, and changes only the locks for newer app releases. A replaced asset
under the same release tag or a missing package stops the update. After a real
update, it commits the locks and starts the amd64 build and smoke test.

The build workflow does not publish by default. To publish a tested image,
manually run **Build and test amd64** on `master` with `publish` enabled. Only
after the container passes the 17 app and desktop service checks will it push
`latest` and `sha-<12-character commit>` tags to GHCR. The first package is
private by default; its visibility can be changed in the package settings.

Before sharing the image with Unraid users, make the GHCR package public and
verify that an unauthenticated pull works. The GitHub repository itself can
remain private. GitHub states that changing a package to public cannot be
reversed, so review the package and image details before that step.

This project currently builds and checks only `linux/amd64`. ARM64 checksums
in the existing lock files are preserved but are not updated by the release
checker. An Unraid template and automatic publication after successful release
checks are separate follow-up steps.
