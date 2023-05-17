// Import modules
import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';
import * as dat from 'dat.gui';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
// Import objects
const loader = new GLTFLoader();
const monkeyUrl = new URL('../assets/balls.gltf', import.meta.url);

// Add basic scene elements
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
    45,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
);
camera.position.set(-10, 30, 30);

const orbit = new OrbitControls(camera, renderer.domElement);
orbit.update();

// Add grid
const gridHelper = new THREE.GridHelper(30);
scene.add(gridHelper);

// Add lights
const ambientLight = new THREE.AmbientLight('white');
scene.add(ambientLight);

const mainLight = new THREE.DirectionalLight('white');
scene.add(mainLight);
const lightHelper = new THREE.DirectionalLightHelper(mainLight);
scene.add(lightHelper);


// Main body
loader.load(monkeyUrl.href,  //aanpassen naar juiste object
    function(object){
        const model = object.scene;

        const material = new THREE.MeshStandardMaterial({color: 0x00ff00});

        model.traverse(function(child){
            if(child.isMesh){
                child.material = material;
            }
        });

        scene.add(model);
        // mainLight.target = model;
    }, undefined, function(error){
    console.error(error);
});


// Add options gui
const gui = new dat.GUI();
const options = {
    gridHelper: true,
    ambientLightIntensity: 0.5,
    mainLightIntensity: 3,
    mainLightX: 0,
    mainLightY: 10,
    mainLightZ: 0,
    mainLightHelper: false
};
gui.add(options, 'gridHelper');
gui.add(options, 'ambientLightIntensity', 0, 1);
gui.add(options, 'mainLightIntensity', 0, 5);
gui.add(options, 'mainLightX', -10, 10);
gui.add(options, 'mainLightY', -10, 10);
gui.add(options, 'mainLightZ', -10, 10);
gui.add(options, 'mainLightHelper');


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

// Update view when window is resized
window.addEventListener('resize', function() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});