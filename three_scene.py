import streamlit.components.v1 as components

def render_3d_core(height: int = 300):
    html = r"""
<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>html,body{margin:0;background:transparent;overflow:hidden}canvas{display:block}#hint{position:absolute;bottom:8px;left:0;right:0;text-align:center;color:#7182a5;font:10px monospace;letter-spacing:2px;pointer-events:none}</style>
</head><body><div id="hint">DRAG TO ROTATE · SCROLL TO ZOOM</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r152/three.min.js"></script>
<script>
if(window.THREE){
const scene=new THREE.Scene();scene.fog=new THREE.FogExp2(0x080b14,.055);
const camera=new THREE.PerspectiveCamera(42,innerWidth/innerHeight,.1,100);camera.position.set(0,0,8);
const renderer=new THREE.WebGLRenderer({antialias:true,alpha:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.setSize(innerWidth,innerHeight);renderer.setClearColor(0x000000,0);document.body.appendChild(renderer.domElement);
scene.add(new THREE.AmbientLight(0x8ba8ff,1.7));const light=new THREE.PointLight(0x63f4e8,24);light.position.set(3,3,5);scene.add(light);
const group=new THREE.Group();scene.add(group);
const core=new THREE.Mesh(new THREE.IcosahedronGeometry(1.12,3),new THREE.MeshPhysicalMaterial({color:0x6b72ff,metalness:.35,roughness:.22,transmission:.12,thickness:1,emissive:0x1c276f,emissiveIntensity:.8,wireframe:false}));group.add(core);
const wire=new THREE.Mesh(new THREE.IcosahedronGeometry(1.28,2),new THREE.MeshBasicMaterial({color:0x63f4e8,wireframe:true,transparent:true,opacity:.42}));group.add(wire);
const ringMat=new THREE.MeshBasicMaterial({color:0xa78bfa,transparent:true,opacity:.75});
for(let i=0;i<3;i++){const ring=new THREE.Mesh(new THREE.TorusGeometry(1.75+i*.27,.008,8,180),new THREE.MeshBasicMaterial({color:[0x63f4e8,0xa78bfa,0xfb79b7][i],transparent:true,opacity:.7}));ring.rotation.set(i*.9,i*.6,i*.7);group.add(ring)}
const nodes=[];for(let i=0;i<18;i++){const a=i*2.399,b=Math.acos(1-2*(i+.5)/18);const p=new THREE.Vector3(2.5*Math.sin(b)*Math.cos(a),2.5*Math.sin(b)*Math.sin(a),2.5*Math.cos(b));const m=new THREE.Mesh(new THREE.SphereGeometry(.055,12,12),new THREE.MeshBasicMaterial({color:[0x63f4e8,0xa78bfa,0xfb79b7,0xb8f36b][i%4]}));m.position.copy(p);group.add(m);nodes.push(m)}
let down=false,px=0,py=0,rotX=0,rotY=0;renderer.domElement.addEventListener('pointerdown',e=>{down=true;px=e.clientX;py=e.clientY;renderer.domElement.setPointerCapture(e.pointerId)});renderer.domElement.addEventListener('pointerup',()=>down=false);renderer.domElement.addEventListener('pointermove',e=>{if(down){rotY+=(e.clientX-px)*.008;rotX+=(e.clientY-py)*.008;px=e.clientX;py=e.clientY}});renderer.domElement.addEventListener('wheel',e=>{camera.position.z=Math.max(5,Math.min(12,camera.position.z+e.deltaY*.008))},{passive:true});
function resize(){camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight)}addEventListener('resize',resize);
function animate(t){requestAnimationFrame(animate);group.rotation.y=rotY+t*.00013;group.rotation.x=rotX+Math.sin(t*.0003)*.12;core.rotation.y=t*.00035;wire.rotation.x=-t*.00022;nodes.forEach((n,i)=>{n.scale.setScalar(1+.25*Math.sin(t*.002+i))});renderer.render(scene,camera)}animate(0);
}</script></body></html>"""
    components.html(html, height=height, scrolling=False)
