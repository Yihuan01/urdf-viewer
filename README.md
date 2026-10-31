# URDF Viewer

**English** · [中文说明](README.zh-CN.md)

A zero-install URDF viewer that runs in the browser. Open a `.urdf`, drag joint sliders, and toggle collision meshes, joint axes and link frames — no ROS, no build step, no Python packages.

> **Live demo**: <https://yihuan01.github.io/urdf-viewer/>
> The bundled demo model loads automatically. The file browser needs a directory index, which GitHub Pages does not provide — type `examples/demo.urdf` in the path box there.

![URDF Viewer](docs/screenshot.png)

## Requirements

- **Python 3** — only to serve the directory (`http.server`), no third-party packages.
- A modern browser (Chrome / Edge / Firefox / Safari).
- three.js and urdf-loader are loaded from unpkg via CDN, so the **first load needs network access**. To work fully offline, download both libraries and point the import map in `index.html` at your local copies.

## Quick start

```bash
cd urdf-viewer
./start_viewer.sh          # default port 8975, opens the browser if possible
./start_viewer.sh 9000     # custom port
```

Or serve it yourself (the bundled script also answers the directory-listing endpoint the file browser uses):

```bash
python3 serve.py 8975
# Windows: python serve.py 8975
```

Plain `python3 -m http.server 8975` works too, but it will not list a directory that contains an `index.html`, so type the URDF path manually in that case.

Then open <http://127.0.0.1:8975/index.html>.

Do **not** double-click `index.html`: under `file://` browsers refuse to fetch mesh files and you get a blank page.

## Loading your own model

- Put `index.html`, your URDF and its meshes in the same directory (subdirectories are fine), then pick the `.urdf` in the **Model files** browser on the left.
- Or type a relative path in the box, e.g. `myrobot/urdf/robot.urdf`.
- Mesh paths inside the URDF are resolved **relative to the URDF file**, so relative paths are the safest:
  ```xml
  <mesh filename="../meshes/base_link.stl"/>
  ```
- `package://` is not resolved (that would need a ROS environment) — rewrite those paths as relative or absolute ones.
- Add `?root=../other_robot/` to the URL to browse a directory outside the page's own folder.
- `examples/demo.urdf` is a minimal two-link arm made of primitives; it needs no mesh files and is a good sanity check.

## Features

| Area | What it does |
|---|---|
| **Model files** | Browse directories, load `.urdf` files, or type a path. |
| **Joints** | One slider per movable joint, showing name, range (degrees for revolute, metres for prismatic) and live value; dragging updates the model immediately. Joints without limits (wheels) open up to ±180°. |
| **Visual** | Show/hide visual meshes. On by default. |
| **Collision** | Show/hide collision geometry as translucent orange. Off by default. |
| **Axis** | Show/hide each joint's rotation/translation axis as a yellow arrow. Off by default. |
| **Frames** | Show/hide each link's local frame (red = X, green = Y, blue = Z). Off by default. |
| **Reset** | Zero every joint, restore the default toggles, re-frame the camera. |

Collision geometry, with the toggle switched on:

![Collision view](docs/screenshot-collision.png)

**Mouse**: left drag = orbit, wheel = zoom, right drag = pan.

## Known limitations

- Must be served over HTTP; `file://` will not work.
- `.xacro` files are listed by the browser but **not expanded** — only plain URDF can be parsed.
- The directory browser asks the bundled `serve.py` for a JSON listing and otherwise scrapes the server's HTML autoindex. Servers with neither — GitHub Pages, for instance — show an empty list; type the path manually.
- Models are assumed to be **Z-up** (rotated −90° about X for display). A Y-up model needs `robot.rotation.x` adjusted in `index.html`.
- No animation playback, no IK, no multi-robot scenes.

## Third-party

- [three.js](https://threejs.org/) r160 — MIT
- [urdf-loader](https://github.com/gkjohnson/urdf-loader) 0.12.3 — Apache-2.0

Both are fetched from unpkg at runtime and are not redistributed in this repository.

## License

[MIT](LICENSE) © 2026 Yihuan01

A personal tool, shared as-is. No support, no roadmap; fork it and change whatever you like.
