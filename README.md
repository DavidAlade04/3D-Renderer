# Python 3D Renderer

<div align="center">
  <img src="https://github.com/DavidAlade04/3D-Renderer/blob/master/demo/3D%20Renderer.gif?raw=true" alt="3D Render Demo" width="600"/>
</div>

## Overview
A lightweight, custom-built 3D rendering engine developed entirely in Python. Rather than relying on heavy external game engines, this project explores the core mathematical and computational foundations of 3D graphics by implementing rendering systems, spatial transformations, and geometric interactions from scratch. 
(From the 500 lines or less book)

It serves as a practical deep dive into spatial mechanics, matrix operations, and rendering pipelines.

## Core Features
* **Hierarchical Scene Graph:** Manages complex 3D environments and nested object relationships (`scene.py`, `hierarchicalnode.py`).
* **Spatial Transformations:** Handles the underlying mathematics for translating, rotating, and scaling objects in 3D space (`transformation.py`).
* **Interactive Camera:** Implements a trackball camera system for fluid, user-controlled viewport rotation and exploration (`trackball.py`, `interaction.py`).
* **Primitive Generation:** Procedural generation of foundational 3D geometry, including spheres, cubes, and composite models like snow figures (`primitive.py`, `cube.py`, `sphere.py`).
* **Collision Detection:** Utilizes Axis-Aligned Bounding Boxes (AABB) for efficient spatial calculations and object interaction (`aabb.py`).
