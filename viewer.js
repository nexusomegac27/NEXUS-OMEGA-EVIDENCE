import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { RGBELoader } from "three/addons/loaders/RGBELoader.js";

const CLAIM = "C1_DESCRIPTIVE_ONLY";
const canvas = document.getElementById("c");
const poster = document.getElementById("poster");
const loadStatus = document.getElementById("load-status");
const chipRuntime = document.getElementById("chip-runtime");
const chipLod = document.getElementById("chip-lod");
const perfMeta = document.getElementById("perf-meta");
const modeHelp = document.getElementById("mode-help");
const stage = document.getElementById("stage");

const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const MODE_HELP = {
  HUMAN: "BodyTwin · Synthetic visual model · C1",
  STRUCTURE: "Illustrative scaffold overlay — not anatomical ground truth.",
  TISSUE: "Illustrative tissue cue — not histology or measurement.",
  PHYSICS: "Proxy capsules shown separately — PHOTOREAL_RENDER_BODY ≠ RAPIER_PHYSICS_BODY.",
  EVIDENCE: "Provenance bound · license ledger · no claim upgrade.",
};

const REGION = {
  FULL: { target: new THREE.Vector3(0, 0.95, 0), pos: new THREE.Vector3(0.35, 1.15, 2.35), min: 0.9, max: 4.2 },
  HEAD: { target: new THREE.Vector3(0, 1.62, 0.05), pos: new THREE.Vector3(0.18, 1.68, 0.55), min: 0.25, max: 1.2 },
  THORAX: { target: new THREE.Vector3(0, 1.25, 0), pos: new THREE.Vector3(0.4, 1.3, 1.1), min: 0.45, max: 2.0 },
  HAND: { target: new THREE.Vector3(0.28, 0.95, 0.05), pos: new THREE.Vector3(0.55, 1.0, 0.55), min: 0.2, max: 1.0 },
  SIDEVIS: { target: new THREE.Vector3(0, 1.0, 0), pos: new THREE.Vector3(2.1, 1.1, 0.15), min: 0.9, max: 3.5 },
  KNEE: { target: new THREE.Vector3(0.08, 0.48, 0), pos: new THREE.Vector3(0.35, 0.55, 0.85), min: 0.25, max: 1.4 },
  FOOT: { target: new THREE.Vector3(0.05, 0.08, 0.08), pos: new THREE.Vector3(0.25, 0.25, 0.55), min: 0.15, max: 1.0 },
};

let renderer = null;
let useWebGPU = false;
let scene, camera, controls, clock;
let humanRoot = null;
let physicsRoot = null;
let structureRoot = null;
let tissueMat = null;
let currentMode = "HUMAN";
let currentLod = "lod2";
let frameTimes = [];
let blinkT = 0;
let breathT = 0;

function setStatus(msg) {
  loadStatus.textContent = msg;
}

function detectRenderer() {
  // Let Three.js own the WebGL context — do not call getContext before WebGLRenderer.
  try {
    const probe = document.createElement("canvas").getContext("webgl2");
    const preferWebGL2 = !!probe;
    renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      alpha: false,
      powerPreference: "high-performance",
      preserveDrawingBuffer: true,
    });
    chipRuntime.textContent = preferWebGL2 ? "WEBGL2" : "WEBGL";
    chipRuntime.classList.add("ok");
    return preferWebGL2 ? "WEBGL2" : "WEBGL";
  } catch (_) {}
  chipRuntime.textContent = "POSTER_FALLBACK";
  return "POSTER";
}

async function init() {
  const kind = detectRenderer();
  if (kind === "POSTER") {
    poster.classList.add("on");
    canvas.style.display = "none";
    setStatus("3D runtime unavailable — static poster fallback active. Route remains usable.");
    chipLod.textContent = "POSTER";
    return;
  }

  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.35;
  renderer.shadowMap.enabled = false;
  renderer.setClearColor(0x0c0c0b, 1);

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0c0c0b);
  // Soft far fog only — earlier near-fog crushed skin into black.

  camera = new THREE.PerspectiveCamera(35, 1, 0.05, 40);
  controls = new OrbitControls(camera, canvas);
  controls.enableDamping = true;
  controls.dampingFactor = 0.06;
  controls.enablePan = false;
  applyRegion("FULL");

  const hemi = new THREE.HemisphereLight(0xf0e8dc, 0x2a241c, 0.95);
  scene.add(hemi);
  const key = new THREE.DirectionalLight(0xfff2e0, 1.85);
  key.position.set(1.4, 2.6, 1.8);
  scene.add(key);
  const fill = new THREE.DirectionalLight(0xb8c4d8, 0.65);
  fill.position.set(-2.0, 1.2, -1.0);
  scene.add(fill);
  const rim = new THREE.DirectionalLight(0xffe6c8, 0.7);
  rim.position.set(-0.5, 1.8, -2.2);
  scene.add(rim);

  physicsRoot = buildPhysicsProxies();
  physicsRoot.visible = false;
  scene.add(physicsRoot);

  structureRoot = buildStructure();
  structureRoot.visible = false;
  scene.add(structureRoot);

  clock = new THREE.Clock();
  resize();
  window.addEventListener("resize", resize);
  setupUI();
  // Render loop + first LOD must not wait on HDRI/PMREM (can hang under software GL).
  animate();
  await progressiveLoad();
  setStatus("BodyTwin ready · synthetic adult · no biometric capture");
  void loadEnvironmentMap();
}

async function loadEnvironmentMap() {
  try {
    const pmrem = new THREE.PMREMGenerator(renderer);
    const hdrPromise = new RGBELoader().loadAsync("assets/hdri/studio_small_09_1k.hdr");
    const timeout = new Promise((_, rej) => setTimeout(() => rej(new Error("HDRI_TIMEOUT")), 12000));
    const hdr = await Promise.race([hdrPromise, timeout]);
    scene.environment = pmrem.fromEquirectangular(hdr).texture;
    hdr.dispose();
    pmrem.dispose();
  } catch (e) {
    console.warn("HDRI deferred/skip", e && e.message ? e.message : e);
  }
}

function applyRegion(name) {
  if (name === "FULL" && humanRoot) {
    frameCameraToHuman();
    return;
  }
  if (humanRoot && name !== "FULL") {
    const box = new THREE.Box3().setFromObject(humanRoot);
    const size = box.getSize(new THREE.Vector3());
    const c = box.getCenter(new THREE.Vector3());
    const h = size.y;
    const presets = {
      HEAD: { ty: c.y + h * 0.38, tz: c.z, dist: Math.max(0.45, h * 0.28) },
      THORAX: { ty: c.y + h * 0.12, tz: c.z, dist: Math.max(0.7, h * 0.45) },
      HAND: { ty: c.y + h * 0.02, tz: c.z, dist: Math.max(0.4, h * 0.28), ox: size.x * 0.55 },
      SIDEVIS: { ty: c.y, tz: c.z, dist: Math.max(1.2, h * 0.85), side: true },
      KNEE: { ty: c.y - h * 0.22, tz: c.z, dist: Math.max(0.5, h * 0.35) },
      FOOT: { ty: box.min.y + h * 0.04, tz: c.z, dist: Math.max(0.35, h * 0.25) },
    };
    const p = presets[name];
    if (p) {
      controls.target.set(c.x + (p.ox || 0) * 0.15, p.ty, p.tz);
      if (p.side) camera.position.set(c.x + p.dist, p.ty, c.z + p.dist * 0.08);
      else camera.position.set(c.x + p.dist * 0.2, p.ty + h * 0.02, c.z + p.dist);
      controls.minDistance = p.dist * 0.35;
      controls.maxDistance = p.dist * 3.2;
      controls.update();
      return;
    }
  }
  const r = REGION[name] || REGION.FULL;
  controls.target.copy(r.target);
  camera.position.copy(r.pos);
  controls.minDistance = r.min;
  controls.maxDistance = r.max;
  controls.maxPolarAngle = Math.PI * 0.92;
  controls.minPolarAngle = 0.08;
  controls.update();
}

function buildPhysicsProxies() {
  const g = new THREE.Group();
  g.name = "physics_proxy";
  const mat = new THREE.MeshBasicMaterial({ color: 0x7d9a7a, wireframe: true, transparent: true, opacity: 0.55 });
  const specs = [
    [0.12, 0.9, 0.08, 0, 1.35, 0],
    [0.18, 0.35, 0.12, 0, 1.15, 0],
    [0.07, 0.35, 0.07, 0.22, 1.15, 0],
    [0.07, 0.35, 0.07, -0.22, 1.15, 0],
    [0.08, 0.42, 0.08, 0.1, 0.55, 0],
    [0.08, 0.42, 0.08, -0.1, 0.55, 0],
    [0.09, 0.09, 0.09, 0, 1.65, 0.02],
  ];
  for (const [sx, sy, sz, x, y, z] of specs) {
    const m = new THREE.Mesh(new THREE.BoxGeometry(sx * 2, sy * 2, sz * 2), mat);
    m.position.set(x, y, z);
    g.add(m);
  }
  return g;
}

function buildStructure() {
  const g = new THREE.Group();
  const mat = new THREE.LineBasicMaterial({ color: 0xa8895a, transparent: true, opacity: 0.85 });
  const pts = [
    [0, 0.05, 0], [0, 0.95, 0], [0, 1.35, 0], [0, 1.65, 0.02],
    [0, 1.35, 0], [0.28, 1.15, 0], [0.42, 0.95, 0.05],
    [0, 1.35, 0], [-0.28, 1.15, 0], [-0.42, 0.95, 0.05],
    [0, 0.95, 0], [0.12, 0.5, 0], [0.1, 0.08, 0.05],
    [0, 0.95, 0], [-0.12, 0.5, 0], [-0.1, 0.08, 0.05],
  ];
  const geo = new THREE.BufferGeometry().setFromPoints(pts.map((p) => new THREE.Vector3(...p)));
  g.add(new THREE.Line(geo, mat));
  return g;
}

async function loadGlb(url) {
  const loader = new GLTFLoader();
  return loader.loadAsync(url);
}

async function progressiveLoad() {
  // Always start with tiny LOD3 so the human is visible quickly; poster only if that fails.
  poster.classList.add("on");
  const mobile = window.matchMedia("(max-width: 720px)").matches;
  const saveData = navigator.connection && navigator.connection.saveData;
  setStatus("Poster → LOD3…");
  try {
    const lod3 = await loadGlb("assets/bodytwin_human_lod3.glb");
    mountHuman(lod3.scene, "lod3");
    poster.classList.remove("on");
    setStatus("LOD3 ready · refining…");
  } catch (e) {
    console.error(e);
    poster.classList.add("on");
    setStatus("GLB load failed — poster fallback. Route usable.");
    chipLod.textContent = "POSTER";
    return;
  }

  const upgrades = [];
  if (!saveData) upgrades.push("lod2");
  if (!saveData && !mobile) upgrades.push("lod1");
  if (!saveData && !mobile) upgrades.push("lod0");
  for (const lod of upgrades) {
    try {
      const g = await loadGlb(`assets/bodytwin_human_${lod}.glb`);
      mountHuman(g.scene, lod);
      setStatus(`${lod.toUpperCase()} mounted`);
    } catch (e) {
      console.warn(lod, "upgrade failed", e);
    }
  }
}

function frameCameraToHuman() {
  if (!humanRoot || !camera || !controls) return;
  const box = new THREE.Box3().setFromObject(humanRoot);
  const size = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());
  const height = Math.max(size.y, 0.1);
  // Slight 3/4 eye-level framing for full body.
  const dist = Math.max(2.1, height * 1.35);
  controls.target.set(center.x, center.y * 0.92, center.z);
  camera.position.set(center.x + dist * 0.22, center.y * 0.95, center.z + dist * 0.95);
  controls.minDistance = Math.max(0.6, height * 0.45);
  controls.maxDistance = Math.max(4.5, height * 2.6);
  controls.update();
}

function mountHuman(sceneIn, lod) {
  if (humanRoot) scene.remove(humanRoot);
  humanRoot = sceneIn;
  humanRoot.name = "human_render";
  // Normalize authored height to ~1.78 m (LOD simplify can shrink bounds).
  let box = new THREE.Box3().setFromObject(humanRoot);
  let size = box.getSize(new THREE.Vector3());
  const scale = 1.78 / Math.max(size.y, 1e-6);
  humanRoot.scale.setScalar(scale);
  box = new THREE.Box3().setFromObject(humanRoot);
  humanRoot.position.y -= box.min.y;
  humanRoot.traverse((o) => {
    if (o.isMesh) {
      o.castShadow = false;
      o.receiveShadow = false;
      o.frustumCulled = true;
      if (o.geometry) {
        o.geometry.computeVertexNormals();
      }
      if (o.material) {
        const mats = Array.isArray(o.material) ? o.material : [o.material];
        for (const m of mats) {
          if (m.map) {
            m.map.colorSpace = THREE.SRGBColorSpace;
            m.map.needsUpdate = true;
            m.color.setRGB(1, 1, 1);
          } else if (!m.color || m.color.r + m.color.g + m.color.b < 0.2) {
            m.color = new THREE.Color(0xd2b39a);
          }
          m.flatShading = false;
          m.roughness = Math.min(0.72, Math.max(0.35, m.roughness ?? 0.55));
          m.metalness = 0.0;
          m.envMapIntensity = 1.0;
          m.side = THREE.FrontSide;
          if ("emissiveIntensity" in m) m.emissiveIntensity = 0;
          m.needsUpdate = true;
        }
      }
    }
  });
  scene.add(humanRoot);
  currentLod = lod;
  chipLod.textContent = lod.toUpperCase();
  if (lod === "lod3" || !window.__BT) {
    frameCameraToHuman();
  }
  applyMode(currentMode);
  window.__BT = {
    lod,
    box: (() => {
      const b = new THREE.Box3().setFromObject(humanRoot);
      const s = b.getSize(new THREE.Vector3());
      return { min: b.min.toArray(), max: b.max.toArray(), size: s.toArray() };
    })(),
    cam: camera.position.toArray(),
    target: controls.target.toArray(),
  };
}

function applyMode(mode) {
  currentMode = mode;
  modeHelp.textContent = MODE_HELP[mode] || MODE_HELP.HUMAN;
  document.querySelectorAll("#modes button").forEach((b) => {
    b.setAttribute("aria-pressed", String(b.dataset.mode === mode));
  });
  if (humanRoot) {
    humanRoot.visible = mode !== "PHYSICS";
    humanRoot.traverse((o) => {
      if (!o.isMesh || !o.material) return;
      const mats = Array.isArray(o.material) ? o.material : [o.material];
      for (const m of mats) {
        if (mode === "STRUCTURE") {
          m.wireframe = true;
          m.transparent = true;
          m.opacity = 0.35;
        } else if (mode === "TISSUE") {
          m.wireframe = false;
          m.transparent = false;
          m.opacity = 1;
          m.color = new THREE.Color(0xc45c4a);
          m.roughness = 0.85;
        } else if (mode === "EVIDENCE") {
          m.wireframe = false;
          m.transparent = true;
          m.opacity = 0.75;
          m.color = new THREE.Color(0xeceae4);
        } else {
          m.wireframe = false;
          m.transparent = false;
          m.opacity = 1;
          // restore roughly neutral; texture carries color
          if (!m.map) m.color = new THREE.Color(0xd2b39a);
          else m.color = new THREE.Color(0xffffff);
          m.roughness = 0.55;
        }
      }
    });
  }
  if (structureRoot) structureRoot.visible = mode === "STRUCTURE" || mode === "EVIDENCE";
  if (physicsRoot) physicsRoot.visible = mode === "PHYSICS" || mode === "EVIDENCE";
}

function setupUI() {
  document.querySelectorAll("#modes button").forEach((b) => {
    b.addEventListener("click", () => applyMode(b.dataset.mode));
  });
  document.getElementById("btn-reset").addEventListener("click", () => {
    document.getElementById("region").value = "FULL";
    applyRegion("FULL");
    applyMode("HUMAN");
  });
  document.getElementById("region").addEventListener("change", (e) => applyRegion(e.target.value));
  stage.addEventListener("keydown", (e) => {
    if (e.key === "r" || e.key === "R") applyRegion("FULL");
    if (e.key === "1") applyMode("HUMAN");
    if (e.key === "2") applyMode("STRUCTURE");
    if (e.key === "3") applyMode("TISSUE");
    if (e.key === "4") applyMode("PHYSICS");
    if (e.key === "5") applyMode("EVIDENCE");
  });
}

function resize() {
  if (!renderer || !camera) return;
  const w = stage.clientWidth;
  const h = stage.clientHeight;
  renderer.setSize(w, h, false);
  camera.aspect = w / Math.max(h, 1);
  camera.updateProjectionMatrix();
}

function animate() {
  requestAnimationFrame(animate);
  const dt = clock.getDelta();
  const t = clock.elapsedTime;
  controls.update();

  if (humanRoot && !reducedMotion && currentMode === "HUMAN") {
    breathT += dt;
    if (!humanRoot.userData.baseScale) {
      humanRoot.userData.baseScale = humanRoot.scale.x;
    }
    const s = humanRoot.userData.baseScale;
    const breath = Math.sin(breathT * 1.4) * 0.004;
    humanRoot.scale.set(s, s * (1 + breath), s);
    humanRoot.rotation.y = Math.sin(t * 0.25) * 0.015;
    // subtle blink via brief opacity dip on eye-named meshes
    blinkT += dt;
    if (blinkT > 4.2) {
      blinkT = 0;
      humanRoot.traverse((o) => {
        if (o.isMesh && /eye/i.test(o.name || o.parent?.name || "")) {
          const mats = Array.isArray(o.material) ? o.material : [o.material];
          mats.forEach((m) => {
            m.userData._blink = true;
            m.transparent = true;
            m.opacity = 0.15;
            setTimeout(() => {
              m.opacity = 1;
              m.transparent = false;
            }, 90);
          });
        }
      });
    }
  }

  renderer.render(scene, camera);
  frameTimes.push(dt);
  if (frameTimes.length > 60) frameTimes.shift();
  if (frameTimes.length === 60) {
    const avg = frameTimes.reduce((a, b) => a + b, 0) / frameTimes.length;
    const fps = avg > 0 ? (1 / avg) : 0;
    perfMeta.textContent = `perf: ~${fps.toFixed(1)} fps (local sample, not universal) · LOD=${currentLod} · claim=${CLAIM}`;
  }
}

init().catch((e) => {
  console.error(e);
  poster.classList.add("on");
  canvas.style.display = "none";
  setStatus("Init failure — poster fallback. Route usable.");
  chipRuntime.textContent = "FALLBACK";
  chipLod.textContent = "POSTER";
});
