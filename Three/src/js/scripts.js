// Import modules
import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';
import * as dat from 'dat.gui';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {STLLoader} from 'three/examples/jsm/loaders/STLLoader.js';
// Import objects
const loader = new STLLoader();
const modelUrl = new URL('../assets/conn.stl', import.meta.url);
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

// Add variables
let currentMesh;
let stlPaths = [];
stlPaths[0] = modelUrl_t0;
stlPaths[1] = modelUrl;
stlPaths[2] = modelUrl_t2;
stlPaths[3] = modelUrl_t3;
stlPaths[4] = modelUrl_t4;
stlPaths[5] = modelUrl_t5;
let currentStlIndex = 0;
const clock = new THREE.Clock();

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

// Add options gui
const gui = new dat.GUI();
const options = {
    gridHelper: false,
    ambientLightIntensity: 0.1,
    mainLightIntensity: 2,
    mainLightX: 0,
    mainLightY: 25,
    mainLightZ: 0,
    mainLightHelper: false,
    timeStepDelay: 1,
    isPaused: false
};

gui.add(options, 'gridHelper');
gui.add(options, 'ambientLightIntensity', 0, 1);
gui.add(options, 'mainLightIntensity', 0, 5);
gui.add(options, 'mainLightX', -250, 250);
gui.add(options, 'mainLightY', -50, 50);
gui.add(options, 'mainLightZ', -250, 250);
gui.add(options, 'mainLightHelper');
gui.add(options, 'timeStepDelay', 0.1, 2 ,0.1);
gui.add(options, 'isPaused');
gui.close();


// Animation loop
function animate(time) {

    gridHelper.visible = options.gridHelper;

    ambientLight.intensity = options.ambientLightIntensity;

    mainLight.intensity = options.mainLightIntensity;
    mainLight.position.set(options.mainLightX, options.mainLightY, options.mainLightZ);
    lightHelper.visible = options.mainLightHelper;


    renderer.render(scene, camera);

    const delta = clock.getDelta(); // start the clock

    if (options.isPaused){
        options.timeStepDelay = 1000
    }
    if (options.isPaused == false){
        clock.start
    }

    if (clock.elapsedTime >= options.timeStepDelay) {
        currentStlIndex = (currentStlIndex + 1) % stlPaths.length; // Increment the index and loop back if necessary
        loadSTL(stlPaths[currentStlIndex]);
        clock.start(); // Reset the clock
    }
}

 renderer.setAnimationLoop(animate);


function loadSTL(stlPath) {
    // Remove the previous mesh, if any
    if (currentMesh) {
        scene.remove(currentMesh);
    }

    // Load the new STL file
    loader.load(stlPath,
        function (geometry) {
            const material = new THREE.MeshStandardMaterial({color: 0x00ff00});
            const mesh = new THREE.Mesh(geometry, material);
    
            mesh.rotation.x = -Math.PI / 2;
            scene.add(mesh);
            currentMesh = mesh;
        }, undefined, function (error) {
            console.error(error);
    });
}


window.onload = animate();

// Update view when window is resized
window.addEventListener('resize', function() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});