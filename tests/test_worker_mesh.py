"""Suite mesh Live Nodes + QNM-BUILD-1.0 + QNS-CD-1.0 cross-map.

Default OFF. live|locked|isolated. No Node Gate. No public qnsd proxy.
No auto-heal. Not anonymity. Not a Softwares-tab product.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MESH = (ROOT / "workers/download-tracker/src/mesh.js").read_text(encoding="utf-8")
INDEX = (ROOT / "workers/download-tracker/src/index.js").read_text(encoding="utf-8")
WRANGLER = (ROOT / "workers/download-tracker/wrangler.toml").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
WORKER_README = (ROOT / "workers/download-tracker/README.md").read_text(encoding="utf-8")


def test_mesh_contract_default_off_qnm_law() -> None:
    assert 'QNM_SPEC = "QNM-BUILD-1.0"' in MESH
    assert "MESH_DEFAULT_OFF = true" in MESH
    assert "MESH_ANONYMITY_NETWORK = false" in MESH
    assert "MESH_NODE_GATE = false" in MESH
    assert "MESH_AUTO_HEAL = false" in MESH
    assert "MESH_IDENTITY = IDENTITY" in MESH or '"Aziel Eliab"' in MESH
    assert 'MESH_PRODUCT = "azai"' in MESH
    assert 'MESH_PATH = "/v1/mesh"' in MESH
    assert "live|locked|isolated" in MESH
    assert "enabled_default: false" in MESH
    assert "anon_broadcast_publish_path: false" in MESH
    assert "Aziel Eliab" in MESH
    assert 'code: extra.code || "MESH-OK"' in MESH or '"MESH-OK"' in MESH
    assert 'QNS_CD_SPEC = "QNS-CD-1.0"' in MESH
    assert "export const QNS_CD" in MESH
    assert "photon QNS1 packet transfer" in MESH
    assert "https://github.com/AzielEliab/qnm-node" in MESH
    assert "https://github.com/AzielEliab/aziel-runtime" in MESH
    assert "QNS-CD-1.0" in MESH
    assert "public_qnsd_proxy: false" in MESH
    assert "softwares_tab: false" in MESH
    assert "Not a public qnsd proxy" in MESH
    assert "QNS-CD-1.0" in MESH.split("MESH_NOTE", 1)[1]


def test_mesh_pointer_and_openapi_helpers() -> None:
    assert "export function meshPointer" in MESH
    assert "export function meshOpenApiPaths" in MESH
    assert "export function parseMeshDoc" in MESH
    assert "export function emptyMesh" in MESH
    assert "export function alignLiveNodes" in MESH
    assert "export function attachQnsCd" in MESH
    assert "fraggate_slug: MESH_SLUG" in MESH
    assert "azai_mesh_" in MESH
    assert "qns_cd: QNS_CD" in MESH
    assert "qns_cd_spec: QNS_CD_SPEC" in MESH


def test_mesh_proxies_via_aziel_runtime() -> None:
    assert "MESH_ROUTE_METHODS" in MESH
    assert "isMeshPath" in MESH
    assert "runMeshProxy" in MESH
    assert "handleMeshApi" in MESH
    assert "originFetch" in MESH
    assert '"/v1/mesh"' in MESH
    assert 'startsWith("/v1/mesh/")' in MESH
    assert "AZIEL_RUNTIME" in MESH
    assert "HTTPS fallback" in MESH or "https fallback" in MESH.lower() or "stub" in MESH
    assert "AZIEL_RUNTIME" in WRANGLER
    assert "aziel-runtime" in WRANGLER
    assert "/v1/mesh" in WRANGLER
    assert 'id = "155f641feb8244bea7fa245133128a32"' in WRANGLER


def test_index_routes_mesh_before_runtime_catchall() -> None:
    assert 'from "./mesh.js"' in INDEX
    assert "handleMeshApi" in INDEX
    mesh_idx = INDEX.index("const mesh = await handleMeshApi(request, url, env)")
    runtime_idx = INDEX.index("const runtime = await handleRuntime(request, url)")
    assert mesh_idx < runtime_idx
    not_found = INDEX.rindex('return json({ error: "not found" }, 404)')
    assert mesh_idx < not_found


def test_runtime_advertises_mesh_proxy_and_pointer() -> None:
    assert 'from "./mesh.js"' in INDEX
    assert "meshPointer" in INDEX
    assert "meshOpenApiPaths" in INDEX
    assert "...meshOpenApiPaths()" in INDEX
    assert "mesh: meshPointer()" in INDEX
    assert "/v1/mesh" in INDEX
    assert "QNM-BUILD-1.0" in INDEX
    assert "QNS-CD-1.0" in INDEX
    assert "No Node Gate" in INDEX
    assert "not a public qnsd proxy" in INDEX
    assert 'path === "/v1/mesh"' in INDEX or 'path.startsWith("/v1/mesh/")' in INDEX


def test_home_download_is_the_primary_action() -> None:
    assert 'id="downloadBtn"' in INDEX
    assert 'href="/download?asset=${DEFAULT_ASSET}"' in INDEX
    assert 'class="btn block primary dl"' in INDEX
    assert 'const DEFAULT_ASSET = "azai-0.3.1.tar.gz"' in INDEX
    assert '<footer class="quiet">' in INDEX
    assert ":focus-visible" in INDEX
    assert "prefers-color-scheme: light" in INDEX
    assert 'id="install-btn"' in INDEX
    assert 'id="meshLiveCount"' in INDEX


def test_home_live_nodes_strip_no_node_gate() -> None:
    assert 'id="meshStrip"' in INDEX
    assert 'id="meshLiveCount"' in INDEX
    assert 'id="meshLine"' in INDEX
    assert "Live Nodes" in INDEX
    assert "QNM-BUILD-1.0" in INDEX
    assert "QNS-CD-1.0 cite" in INDEX
    assert "No Node Gate" in INDEX
    assert "No auto-heal" in INDEX
    assert "Not an anonymity network" in INDEX
    assert "not a Softwares-tab product" in INDEX
    assert "not a public qnsd proxy" in INDEX
    assert "/v1/mesh" in INDEX
    assert 'product: "azai"' in INDEX
    assert 'id="node-gate"' not in INDEX
    assert 'href="/node-gate"' not in INDEX
    assert "auto-heal this node" not in INDEX
    assert "/v1/qnsd" not in INDEX
    assert "qnsd proxy" in INDEX.lower() or "public qnsd proxy" in INDEX


def test_docs_advertise_mesh_proxy() -> None:
    assert "/v1/mesh" in README
    assert "/v1/mesh" in SKILL
    assert "QNS-CD-1.0" in README
    assert "QNS-CD-1.0" in SKILL
    assert "photon QNS1 packet transfer" in README
    assert "photon QNS1 packet transfer" in SKILL
    assert "https://github.com/AzielEliab/qnm-node" in SKILL
    assert "https://github.com/AzielEliab/aziel-runtime" in SKILL
    assert "Not a Softwares-tab product" in SKILL
    assert "QNM-BUILD-1.0" in WORKER_README
    assert "QNS-CD-1.0" in WORKER_README
    assert "AZIEL_RUNTIME" in WORKER_README
    assert "Live Nodes" in WORKER_README
    assert "MESH-OK" in WORKER_README
    assert "enabled: false" in WORKER_README
    assert "qns_cd" in WORKER_README
    assert "Aziel Eliab" in MESH
    assert "MESH_DEFAULT_OFF = true" in MESH
    assert "public_qnsd_proxy: false" in MESH
