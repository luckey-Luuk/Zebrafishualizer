// Import modules
import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';
import * as dat from 'dat.gui';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {STLLoader} from 'three/examples/jsm/loaders/STLLoader.js';
// Import objects
const loader = new STLLoader();
const modelUrl = new URL('../assets/mesh.stl', import.meta.url);
const modelUrl_t0 = new URL('../assets/mesh_t0.stl', import.meta.url);
const modelUrl_t1 = new URL('../assets/mesh_t1.stl', import.meta.url);
const modelUrl_t2 = new URL('../assets/mesh_t2.stl', import.meta.url);
const modelUrl_t3 = new URL('../assets/mesh_t3.stl', import.meta.url);
const modelUrl_t4 = new URL('../assets/mesh_t4.stl', import.meta.url);
const modelUrl_t5 = new URL('../assets/mesh_t5.stl', import.meta.url);

// Add basic scene elements
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
    45,
    window.innerWidth / window.innerHeight,
    0.1,
    5000
);
camera.position.set(0, 800, 0);

const orbit = new OrbitControls(camera, renderer.domElement);
orbit.update();

// Add grid
const gridHelper = new THREE.GridHelper(500, 20);
scene.add(gridHelper);

// Add lights
const ambientLight = new THREE.AmbientLight('white');
scene.add(ambientLight);

const mainLight = new THREE.PointLight('white');
scene.add(mainLight);
const lightHelper = new THREE.PointLightHelper(mainLight);
scene.add(lightHelper);


// Add model
// //gltf
// loader.load(modelUrl.href,
//     function(object){
//         const model = object.scene;

//         const material = new THREE.MeshStandardMaterial({color: 0x00ff00});

//         model.traverse(function(child){
//             if(child.isMesh){
//                 child.material = material;
//             }
//         });

//         scene.add(model);
//     }, undefined, function(error){
//     console.error(error);
// });

//stl
// loader.load(modelUrl_t0,
//     function (geometry) {
//         const material = new THREE.MeshStandardMaterial({color: 0x00ff00});
//         const mesh = new THREE.Mesh(geometry, material);

//         mesh.rotation.x = -Math.PI / 2;
//         scene.add(mesh);
//     }, undefined, function (error) {
//         console.error(error);
// });

// loader.load(modelUrl_t1,
//     function (geometry) {
//         const material = new THREE.MeshStandardMaterial({color: 0x00ff00});
//         const mesh = new THREE.Mesh(geometry, material);

//         mesh.rotation.x = -Math.PI / 2;
//         scene.add(mesh);
//     }, undefined, function (error) {
//         console.error(error);
// });

// loader.load(modelUrl_t2,
//     function (geometry) {
//         const material = new THREE.MeshStandardMaterial({color: 0x00ff00});
//         const mesh = new THREE.Mesh(geometry, material);

//         mesh.rotation.x = -Math.PI / 2;
//         scene.add(mesh);
//     }, undefined, function (error) {
//         console.error(error);
// });

// loader.load(modelUrl_t3,
//     function (geometry) {
//         const material = new THREE.MeshStandardMaterial({color: 0x00ff00});
//         const mesh = new THREE.Mesh(geometry, material);

//         mesh.rotation.x = -Math.PI / 2;
//         scene.add(mesh);
//     }, undefined, function (error) {
//         console.error(error);
// });

// loader.load(modelUrl_t4,
//     function (geometry) {
//         const material = new THREE.MeshStandardMaterial({color: 0x00ff00});
//         const mesh = new THREE.Mesh(geometry, material);

//         mesh.rotation.x = -Math.PI / 2;
//         scene.add(mesh);
//     }, undefined, function (error) {
//         console.error(error);
// });

loader.load(modelUrl_t5,
    function (geometry) {
        const material = new THREE.MeshStandardMaterial({color: 0x00ff00});
        const mesh = new THREE.Mesh(geometry, material);

        mesh.rotation.x = -Math.PI / 2;
        scene.add(mesh);
    }, undefined, function (error) {
        console.error(error);
});

// Add options gui
const gui = new dat.GUI();
const options = {
    gridHelper: false,
    ambientLightIntensity: 0.1,
    mainLightIntensity: 2,
    mainLightX: 0,
    mainLightY: 25,
    mainLightZ: 0,
    mainLightHelper: false
};
gui.add(options, 'gridHelper');
gui.add(options, 'ambientLightIntensity', 0, 1);
gui.add(options, 'mainLightIntensity', 0, 5);
gui.add(options, 'mainLightX', -250, 250);
gui.add(options, 'mainLightY', -50, 50);
gui.add(options, 'mainLightZ', -250, 250);
gui.add(options, 'mainLightHelper');
gui.close();


// Animation loop
function animate(time) {
    gridHelper.visible = options.gridHelper;

    ambientLight.intensity = options.ambientLightIntensity;

    mainLight.intensity = options.mainLightIntensity;
    mainLight.position.set(options.mainLightX, options.mainLightY, options.mainLightZ);
    lightHelper.visible = options.mainLightHelper;


    renderer.render(scene, camera);
}
renderer.setAnimationLoop(animate);

// Making a slideshow
var i=0;
var timesteps = [];
var time = 1000;

timestep[0] = modelUrl_t0;
timestep[1] = modelUrl_t1;
timestep[2] = modelUrl_t2;

function ChangeTimestep(){
    loader.load(timestep[i],
        function (geometry) {
            const material = new THREE.MeshStandardMaterial({color: 0x00ff00});
            const mesh = new THREE.Mesh(geometry, material);
    
            mesh.rotation.x = -Math.PI / 2;
            scene.add(mesh);
        }, undefined, function (error) {
            console.error(error);
    });

    if(i < timestep.length - 1){
        i++;
        console.log(i);
    }
    else{
        i = 0;
    }
    setTimeout("ChangeTimestep()", time)
}

window.onload = ChangeTimestep;



// Update view when window is resized
window.addEventListener('resize', function() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});