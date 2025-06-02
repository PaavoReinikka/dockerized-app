### Client/front template for Eprice app

You need to have deno installed: https://docs.deno.com/runtime/

* missing project.env -- ask Paavo for this.

* run this with docker compose.

* first run `deno install --allow-scripts` in `client/` and `e2e-tests/` directories. This is likely to change in the future, but for now the denoland's alpine base image does not allow installing with optional flags (why this is the case beats me).

