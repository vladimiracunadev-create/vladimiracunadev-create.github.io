import * as THREE from 'three';

// ----------------------------------------------------------------------------------
// CONFIGURADOR DE LA ESCENA (ILUMINACIÓN, ARQUITECTURA Y NATURALEZA PROCEDURAL)
// ----------------------------------------------------------------------------------

export function setupScene(scene) {
    // 1. Luces de Ambiente (Evolucionan a lo largo del camino, pero empezamos con tono base)
    const hemiLight = new THREE.HemisphereLight(0x1e293b, 0x020617, 0.7);
    hemiLight.position.set(0, 50, 0);
    scene.add(hemiLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 0.4);
    dirLight.position.set(-20, 40, 20);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 1024;
    dirLight.shadow.mapSize.height = 1024;
    dirLight.shadow.camera.near = 0.5;
    dirLight.shadow.camera.far = 150;
    dirLight.shadow.camera.left = -30;
    dirLight.shadow.camera.right = 30;
    dirLight.shadow.camera.top = 30;
    dirLight.shadow.camera.bottom = -150;
    scene.add(dirLight);

    // 2. Materiales Arquitectónicos Principales
    const floorMaterial = new THREE.MeshStandardMaterial({
        color: 0x0f172a, // Slate profundo, casi asfalto
        roughness: 0.2,
        metalness: 0.5
    });

    const wallMaterial = new THREE.MeshStandardMaterial({
        color: 0x1e293b,
        roughness: 0.8,
        metalness: 0.2
    });

    // Materiales de Naturaleza / Entorno Procedural
    const dirtMaterial = new THREE.MeshStandardMaterial({ color: 0x3f2e21, roughness: 0.9, metalness: 0.0 });
    const grassMaterial = new THREE.MeshStandardMaterial({ color: 0x166534, roughness: 0.8, metalness: 0.0 }); // Verde bosque
    const rockMaterial = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.7, metalness: 0.1, flatShading: true }); // Gris piedra
    const trunkMaterial = new THREE.MeshStandardMaterial({ color: 0x451a03, roughness: 0.9, metalness: 0 }); // Marrón tronco
    const foliageMaterial = new THREE.MeshStandardMaterial({ color: 0x064e3b, roughness: 0.8, metalness: 0.1, flatShading: true }); // Verde oscuro pino

    const numStations = 24;
    const zOffset = -25;
    const floorLength = Math.abs((numStations + 1) * zOffset);

    // 3. El Suelo Principal (Pasillo Limpio)
    const trackWidth = 24; // Ancho del terreno principal
    const floorGeometry = new THREE.PlaneGeometry(trackWidth, floorLength);
    const floor = new THREE.Mesh(floorGeometry, floorMaterial);
    floor.rotation.x = -Math.PI / 2;
    floor.position.z = (numStations * zOffset) / 2;
    floor.receiveShadow = true;
    scene.add(floor);

    // Terreno exterior (Tierra/Pasto desordenado)
    const outerTerrainGeo = new THREE.PlaneGeometry(120, floorLength + 50, 40, 100);
    // Perturbar los vértices para que parezca terreno irregular
    const positions = outerTerrainGeo.attributes.position;
    for (let i = 0; i < positions.count; i++) {
        // En los bordes centrales (el pasillo), mantener altura 0 o bajarlo, afuera subirlo
        const x = positions.getX(i);
        if (Math.abs(x) > trackWidth / 2 - 2) {
            const noise = Math.random() * 2 - 1;
            positions.setZ(i, Math.abs(x) * 0.15 + noise); // Z es "arriba" antes de rotar
        } else {
            positions.setZ(i, -0.5); // Ligeramente bajo el pasillo
        }
    }
    outerTerrainGeo.computeVertexNormals();

    const terrain = new THREE.Mesh(outerTerrainGeo, dirtMaterial);
    terrain.rotation.x = -Math.PI / 2;
    terrain.position.y = -0.1; // Debajo del asfalto
    terrain.position.z = (numStations * zOffset) / 2;
    terrain.receiveShadow = true;
    scene.add(terrain);

    // 4. Construcción de la Galería y Entorno Aleatorio
    const archesGroup = new THREE.Group();
    const envGroup = new THREE.Group(); // Grupo para elementos fuera del camino

    // Geometrías reusables
    const rockGeo = new THREE.DodecahedronGeometry(1, 1);
    const trunkGeo = new THREE.CylinderGeometry(0.3, 0.5, 3, 5);
    const foliageGeo = new THREE.ConeGeometry(2, 6, 5);
    const bushGeo = new THREE.IcosahedronGeometry(1.5, 0);

    for (let i = 0; i < numStations; i++) {
        const stationZ = i * zOffset;

        // -- ARQUITECTURA DEL PASILLO --
        const leftWall = new THREE.Mesh(new THREE.BoxGeometry(1, 15, 6), wallMaterial);
        leftWall.position.set(-10, 7.5, stationZ);
        leftWall.castShadow = true; leftWall.receiveShadow = true;
        archesGroup.add(leftWall);

        const rightWall = new THREE.Mesh(new THREE.BoxGeometry(1, 15, 6), wallMaterial);
        rightWall.position.set(10, 7.5, stationZ);
        rightWall.castShadow = true; rightWall.receiveShadow = true;
        archesGroup.add(rightWall);

        const roof = new THREE.Mesh(new THREE.BoxGeometry(20, 1, 2), wallMaterial);
        roof.position.set(0, 15.5, stationZ);
        roof.castShadow = true;
        archesGroup.add(roof);

        // Color progresivo de neón (Del Azul al Morado)
        const progress = i / numStations;
        const colorCromo = new THREE.Color().setHSL(0.6 - (progress * 0.2), 0.8, 0.5); // Azul -> Violeta -> Magenta
        const neonMaterial = new THREE.MeshBasicMaterial({ color: colorCromo });

        // Tiras LED y Piscinas de luz
        if (i > 0 && i < numStations - 1) {
            const spotLight = new THREE.SpotLight(colorCromo, 25);
            spotLight.position.set(-6, 14, stationZ);
            spotLight.target.position.set(-6, 0, stationZ);
            spotLight.angle = Math.PI / 7;
            spotLight.penumbra = 0.8;
            spotLight.distance = 25;
            scene.add(spotLight);
            scene.add(spotLight.target);

            const decoPanel = new THREE.Mesh(new THREE.PlaneGeometry(0.2, 10), neonMaterial);
            decoPanel.position.set(-9.4, 5, stationZ);
            archesGroup.add(decoPanel);

            const decoPanelR = new THREE.Mesh(new THREE.PlaneGeometry(0.2, 10), neonMaterial);
            decoPanelR.position.set(9.4, 5, stationZ);
            archesGroup.add(decoPanelR);
        }

        // -- ENTORNO PROCEDURAL EXTERIOR (Naturaleza / Ruinas) --
        // Generar racimos de objetos a los lados
        const numObjects = Math.floor(Math.random() * 6) + 3; // 3 a 8 objetos por lado por estación

        for (let side = -1; side <= 1; side += 2) { // Lado Izquierdo (-1) y Derecho (1)
            for (let j = 0; j < numObjects; j++) {
                // Distancia fuera del camino: entre 12 y 40 unidades
                const rndX = side * (14 + Math.random() * 25);
                // Distancia a lo largo del pasillo, con cierta laxitud
                const rndZ = stationZ + (Math.random() * zOffset * 1.5) - (zOffset * 0.75);

                const type = Math.random(); // Qué generamos?

                if (type < 0.4) {
                    // Árbol Low Poly (Pino)
                    const treeHeight = 3 + Math.random() * 4;
                    const scale = 0.5 + Math.random() * 1.5;

                    const trunk = new THREE.Mesh(trunkGeo, trunkMaterial);
                    trunk.position.set(rndX, treeHeight / 2, rndZ);
                    trunk.scale.set(scale, scale, scale);
                    trunk.castShadow = true;

                    const leaves = new THREE.Mesh(foliageGeo, foliageMaterial);
                    leaves.position.set(rndX, treeHeight * scale + (3 * scale), rndZ);
                    leaves.scale.set(scale, scale, scale);
                    // rotación leve para no ser iguales
                    leaves.rotation.y = Math.random() * Math.PI;
                    leaves.rotation.x = (Math.random() - 0.5) * 0.1;
                    leaves.castShadow = true;

                    envGroup.add(trunk);
                    envGroup.add(leaves);

                } else if (type < 0.7) {
                    // Rocas / Estructuras de Piedra
                    const rock = new THREE.Mesh(rockGeo, rockMaterial);
                    const scale = 1 + Math.random() * 3;
                    rock.scale.set(scale, scale * (0.5 + Math.random()), scale);
                    rock.position.set(rndX, scale / 2, rndZ);
                    rock.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI);
                    rock.castShadow = true;
                    rock.receiveShadow = true;
                    envGroup.add(rock);
                } else {
                    // Arbustos o "Gramos" grandes
                    const bush = new THREE.Mesh(bushGeo, grassMaterial);
                    const scale = 0.5 + Math.random();
                    bush.scale.set(scale * 2, scale, scale * 2);
                    bush.position.set(rndX, scale / 2, rndZ);
                    bush.rotation.y = Math.random() * Math.PI;
                    bush.castShadow = true;
                    envGroup.add(bush);
                }
            }
        }
    }

    scene.add(archesGroup);
    scene.add(envGroup);

    // 5. Muro final de clausura iluminado
    const endWall = new THREE.Mesh(new THREE.BoxGeometry(30, 25, 2), wallMaterial);
    endWall.position.set(0, 12.5, (numStations - 1) * zOffset - 20);
    endWall.receiveShadow = true;
    scene.add(endWall);

    const endNeon = new THREE.Mesh(new THREE.BoxGeometry(4, 4, 1), new THREE.MeshBasicMaterial({ color: 0xffffff, emissive: 0xdb2777 }));
    endNeon.position.set(0, 10, (numStations - 1) * zOffset - 19);
    scene.add(endNeon);

    const endLight = new THREE.PointLight(0xdb2777, 100, 150); // Pinkish al final
    endLight.position.set(0, 10, (numStations - 1) * zOffset - 15);
    scene.add(endLight);

    // 6. Polvo volumétrico / Luciérnagas (Esparcidas ampliamente)
    const params = { count: 2000 };
    const particlesGeo = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(params.count * 3);
    const particleColors = new Float32Array(params.count * 3);

    for (let i = 0; i < params.count * 3; i += 3) {
        particlePositions[i] = (Math.random() - 0.5) * 80;     // Distribuido a lo ancho
        particlePositions[i + 1] = Math.random() * 20;         // Altura
        particlePositions[i + 2] = Math.random() * ((numStations) * zOffset) * 1.2;

        particleColors[i] = Math.random() * 0.4 + 0.1;
        particleColors[i + 1] = Math.random() * 0.8 + 0.2;
        particleColors[i + 2] = Math.random() * 0.5 + 0.5;
    }

    particlesGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    particlesGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));

    const particlesMat = new THREE.PointsMaterial({
        size: 0.15,
        vertexColors: true,
        transparent: true,
        opacity: 0.6,
        // Cambiar mapa no es posible sin assets locales, usamos size pequeño brillante
    });
    scene.add(new THREE.Points(particlesGeo, particlesMat));
}
