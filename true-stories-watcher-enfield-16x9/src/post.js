// Render pipeline: scene (MSAA, HDR) -> half-res depth of field -> composite -> bloom -> tone map -> grade.
import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { Pass, FullScreenQuad } from "three/addons/postprocessing/Pass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";

const COC_GLSL = /* glsl */ `
  #include <packing>
  uniform float uNear, uFar, uFocus, uAperture, uMaxCoc;
  float viewDepth(sampler2D d, vec2 uv) {
    float z = texture2D(d, uv).x;
    return -perspectiveDepthToViewZ(z, uNear, uFar);
  }
  // circle of confusion radius in full-res pixels
  float coc(float z) {
    return clamp(uAperture * abs(z - uFocus) / max(z, 1e-3), 0.0, uMaxCoc);
  }
`;

const VERT = /* glsl */ `
  varying vec2 vUv;
  void main() { vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }
`;

// max CoC per tile (coarse), dilated in the gather
const tileShader = {
  uniforms: { tDepth: { value: null }, uTexel: { value: new THREE.Vector2() }, uTile: { value: 16 },
    uNear: { value: 0.1 }, uFar: { value: 100 }, uFocus: { value: 5 }, uAperture: { value: 10 }, uMaxCoc: { value: 24 } },
  vertexShader: VERT,
  fragmentShader: /* glsl */ `
    varying vec2 vUv;
    uniform sampler2D tDepth; uniform vec2 uTexel; uniform float uTile;
    ${COC_GLSL}
    void main() {
      float m = 0.0;
      for (int y = 0; y < 6; y++) for (int x = 0; x < 6; x++) {
        vec2 o = (vec2(float(x), float(y)) / 5.0 - 0.5) * uTile * uTexel;
        m = max(m, coc(viewDepth(tDepth, vUv + o)));
      }
      gl_FragColor = vec4(m, 0.0, 0.0, 1.0);
    }`,
};

// half-res scatter-as-gather bokeh (after Gustafsson). rgb = blurred color, a = near-field spread
const gatherShader = {
  uniforms: { tColor: { value: null }, tDepth: { value: null }, tTile: { value: null },
    uTexel: { value: new THREE.Vector2() }, uTileTexel: { value: new THREE.Vector2() },
    uNear: { value: 0.1 }, uFar: { value: 100 }, uFocus: { value: 5 }, uAperture: { value: 10 }, uMaxCoc: { value: 24 } },
  vertexShader: VERT,
  fragmentShader: /* glsl */ `
    varying vec2 vUv;
    uniform sampler2D tColor, tDepth, tTile; uniform vec2 uTexel, uTileTexel;
    ${COC_GLSL}
    const float GOLDEN = 2.39996323;
    void main() {
      float R = 0.0;
      for (int y = -1; y <= 1; y++) for (int x = -1; x <= 1; x++)
        R = max(R, texture2D(tTile, vUv + vec2(float(x), float(y)) * uTileTexel).r);
      float zc = viewDepth(tDepth, vUv);
      float cc = coc(zc);
      vec3 col = texture2D(tColor, vUv).rgb;
      float tot = 1.0;
      float nearSpread = 0.0;
      if (R > 1.0) {
        float radius = 1.0;
        float ang = 0.0;
        for (int i = 0; i < 110; i++) {
          if (radius > R) break;
          vec2 tc = vUv + vec2(cos(ang), sin(ang)) * uTexel * radius;
          vec3 sc = texture2D(tColor, tc).rgb;
          float zs = viewDepth(tDepth, tc);
          float cs = coc(zs);
          if (zs > zc) cs = min(cs, cc * 2.0);
          float m = smoothstep(radius - 1.0, radius + 1.0, cs);
          if (zs < zc) nearSpread = max(nearSpread, m * min(cs / 3.0, 1.0));
          col += mix(col / tot, sc, m);
          tot += 1.0;
          ang += GOLDEN;
          radius += 1.6 / radius;
        }
      }
      gl_FragColor = vec4(col / tot, nearSpread);
    }`,
};

const compositeShader = {
  uniforms: { tSharp: { value: null }, tBlur: { value: null }, tDepth: { value: null },
    uNear: { value: 0.1 }, uFar: { value: 100 }, uFocus: { value: 5 }, uAperture: { value: 10 }, uMaxCoc: { value: 24 } },
  vertexShader: VERT,
  fragmentShader: /* glsl */ `
    varying vec2 vUv;
    uniform sampler2D tSharp, tBlur, tDepth;
    ${COC_GLSL}
    void main() {
      vec4 sharp = texture2D(tSharp, vUv);
      vec4 blur = texture2D(tBlur, vUv);
      float cc = coc(viewDepth(tDepth, vUv));
      float k = smoothstep(0.6, 2.2, max(cc, blur.a * 3.0));
      gl_FragColor = vec4(mix(sharp.rgb, blur.rgb, k), 1.0);
    }`,
};

const gradeShader = {
  uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uVignette: { value: 0.35 }, uGrain: { value: 0.035 },
    uLift: { value: new THREE.Vector3(0.0, 0.0, 0.0) }, uGain: { value: new THREE.Vector3(1, 1, 1) },
    uSat: { value: 1.05 }, uFade: { value: 0 }, uFadeColor: { value: new THREE.Vector3(0, 0, 0) }, uAspect: { value: 9 / 16 } },
  vertexShader: VERT,
  fragmentShader: /* glsl */ `
    varying vec2 vUv;
    uniform sampler2D tDiffuse; uniform float uTime, uVignette, uGrain, uSat, uFade, uAspect;
    uniform vec3 uLift, uGain, uFadeColor;
    float h(vec2 p) { return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
    void main() {
      vec3 c = texture2D(tDiffuse, vUv).rgb;
      c = c * uGain + uLift * (1.0 - c);
      float l = dot(c, vec3(0.2126, 0.7152, 0.0722));
      c = mix(vec3(l), c, uSat);
      vec2 q = (vUv - 0.5) * vec2(uAspect, 1.0) * 1.6;
      c *= 1.0 - uVignette * smoothstep(0.35, 1.05, dot(q, q));
      c += (h(vUv * 1000.0 + fract(uTime * 7.31)) - 0.5) * uGrain;
      c = mix(c, uFadeColor, uFade);
      gl_FragColor = vec4(c, 1.0);
    }`,
};

function mat(def) {
  return new THREE.ShaderMaterial({
    uniforms: THREE.UniformsUtils.clone(def.uniforms),
    vertexShader: def.vertexShader,
    fragmentShader: def.fragmentShader,
    depthTest: false,
    depthWrite: false,
  });
}

class SceneDofPass extends Pass {
  constructor(scene, camera, w, h, scale) {
    super();
    this.scene = scene;
    this.camera = camera;
    this.scale = scale;
    this.needsSwap = true;
    const depthTexture = new THREE.DepthTexture(w, h);
    depthTexture.type = THREE.UnsignedIntType;
    this.sceneRT = new THREE.WebGLRenderTarget(w, h, { type: THREE.HalfFloatType, samples: 4, depthTexture });
    const hw = Math.ceil(w / 2), hh = Math.ceil(h / 2);
    this.TILE = 16;
    this.tileRT = new THREE.WebGLRenderTarget(Math.ceil(w / this.TILE), Math.ceil(h / this.TILE), { type: THREE.HalfFloatType });
    this.halfRT = new THREE.WebGLRenderTarget(hw, hh, { type: THREE.HalfFloatType });
    this.tileMat = mat(tileShader);
    this.gatherMat = mat(gatherShader);
    this.compMat = mat(compositeShader);
    this.tileMat.uniforms.uTexel.value.set(1 / w, 1 / h);
    this.tileMat.uniforms.uTile.value = this.TILE;
    this.gatherMat.uniforms.uTexel.value.set(1 / hw, 1 / hh);
    this.gatherMat.uniforms.uTileTexel.value.set(1 / this.tileRT.width, 1 / this.tileRT.height);
    this.quad = new FullScreenQuad(null);
    this.focus = 5;
    this.aperture = 0; // CoC px at full 1080 width; 0 = everything sharp
    this.maxCoc = 26;
  }
  setCoc(m, halfRes) {
    const u = m.uniforms;
    u.uNear.value = this.camera.near;
    u.uFar.value = this.camera.far;
    u.uFocus.value = this.focus;
    // gather runs in half-res pixels, the others in full-res pixels of this target
    const k = this.scale * (halfRes ? 0.5 : 1);
    u.uAperture.value = this.aperture * k;
    u.uMaxCoc.value = this.maxCoc * k;
  }
  render(renderer, writeBuffer) {
    renderer.setRenderTarget(this.sceneRT);
    renderer.clear();
    renderer.render(this.scene, this.camera);
    const depth = this.sceneRT.depthTexture;
    if (this.aperture <= 0.01) {
      this.quad.material = this.compMat;
      this.setCoc(this.compMat, false);
      this.compMat.uniforms.uAperture.value = 0;
      this.compMat.uniforms.tSharp.value = this.sceneRT.texture;
      this.compMat.uniforms.tBlur.value = this.sceneRT.texture;
      this.compMat.uniforms.tDepth.value = depth;
    } else {
      this.setCoc(this.tileMat, false);
      this.tileMat.uniforms.tDepth.value = depth;
      renderer.setRenderTarget(this.tileRT);
      this.quad.material = this.tileMat;
      this.quad.render(renderer);

      this.setCoc(this.gatherMat, true);
      this.gatherMat.uniforms.tColor.value = this.sceneRT.texture;
      this.gatherMat.uniforms.tDepth.value = depth;
      this.gatherMat.uniforms.tTile.value = this.tileRT.texture;
      // tile values are full-res px; gather radius is half-res px
      this.gatherMat.uniforms.uMaxCoc.value = this.maxCoc * this.scale * 0.5;
      renderer.setRenderTarget(this.halfRT);
      this.quad.material = this.gatherMat;
      this.quad.render(renderer);

      this.setCoc(this.compMat, false);
      this.compMat.uniforms.tSharp.value = this.sceneRT.texture;
      this.compMat.uniforms.tBlur.value = this.halfRT.texture;
      this.compMat.uniforms.tDepth.value = depth;
      this.quad.material = this.compMat;
    }
    renderer.setRenderTarget(this.renderToScreen ? null : writeBuffer);
    this.quad.render(renderer);
  }
}

// gather samples the tile texture in half-res px: scale its stored full-res values
gatherShader.fragmentShader = gatherShader.fragmentShader.replace(
  "R = max(R, texture2D(tTile, vUv + vec2(float(x), float(y)) * uTileTexel).r);",
  "R = max(R, 0.5 * texture2D(tTile, vUv + vec2(float(x), float(y)) * uTileTexel).r);",
);

export function createPipeline(renderer, scene, camera, W, H, scale) {
  const composer = new EffectComposer(renderer, new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType }));
  composer.setPixelRatio(1);
  composer.setSize(W, H);
  const scenePass = new SceneDofPass(scene, camera, W, H, scale);
  composer.addPass(scenePass);
  const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), 0.35, 0.55, 0.92);
  composer.addPass(bloom);
  composer.addPass(new OutputPass());
  const grade = new ShaderPass(gradeShader);
  composer.addPass(grade);
  return { composer, scenePass, bloom, grade };
}
