"""
Lighting effect demonstration examples with adjustable parameters
"""

# run_example = false

import math

from PySide6 import QtWidgets, QtGui, QtCore
from wgpu.gui.qt import WgpuWidget
import pygfx as gfx


class LightViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Light_viewer")
        self.resize(800, 600)
        self.wgpu_widget = WgpuWidget(max_fps=60)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(self.wgpu_widget, 1)
        main_layout.addSpacing(10)

        self.btn_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(self.btn_layout)

        self.setLayout(main_layout)

        self.init_scene()
        self.init_gui()

    def init_gui(self):

        self.mesh_flat_checkbox = self.create_checkbox(
            "Flat Shading", self.mesh.material, "flat_shading"
        )

        self.mesh_flat_checkbox = self.create_checkbox(
            "Wireframe", self.mesh.material, "wireframe"
        )

        self.mesh_rotate_checkbox = self.create_checkbox("Auto Rotate")

        self.mesh_color_btn = self.create_color_btn(
            "Material", self.mesh.material, "color"
        )

        self.mesh_specular_btn = self.create_color_btn(
            "Specular", self.mesh.material, "specular"
        )

        self.mesh_emissive_btn = self.create_color_btn(
            "Emissive", self.mesh.material, "emissive"
        )

        self.create_slider("Shininess", 1, 100, self.mesh.material, "shininess")

        self.add_split()

        self.point_light1_move = self.create_checkbox("Auto Move")

        self.point_light1_checkbox = self.create_checkbox(
            "Point Light 1",
            self.point_light1,
            "visible",
            toggle=[
                self.create_color_btn(
                    "Color",
                    self.point_light1,
                    "color",
                    lambda c: setattr(self.point_light1_helper.material, "color", c),
                ),
                self.create_slider(
                    "Intensity", 0, 2, self.point_light1, "intensity", step=0.01
                ),
                self.point_light1_move,
            ],
            index=self.btn_layout.indexOf(self.point_light1_move),
        )

        self.add_split()

        self.point_light2_move = self.create_checkbox("Auto Move")
        self.point_light2_checkbox = self.create_checkbox(
            "Point Light 2",
            self.point_light2,
            "visible",
            toggle=[
                self.create_color_btn(
                    "Color",
                    self.point_light2,
                    "color",
                    lambda c: setattr(self.point_light2_helper.material, "color", c),
                ),
                self.create_slider(
                    "Intensity", 0, 2, self.point_light2, "intensity", step=0.01
                ),
                self.point_light2_move,
            ],
            index=self.btn_layout.indexOf(self.point_light2_move),
        )

        self.add_split()

        self.directional_light_checkbox = self.create_checkbox(
            "Directional Light",
            self.directional_light,
            "visible",
            index=self.btn_layout.count(),
            toggle=[
                self.create_color_btn(
                    "Color",
                    self.directional_light,
                    "color",
                    lambda c: setattr(
                        self.directional_light_helper.material, "color", c
                    ),
                ),
                self.create_slider(
                    "Intensity", 0, 2, self.directional_light, "intensity", step=0.01
                ),
            ],
        )

        self.add_split()

        self.ambient_light_checkbox = self.create_checkbox(
            "Ambient Light",
            self.ambient_light,
            "visible",
            index=self.btn_layout.count(),
            toggle=[
                self.create_color_btn("Color", self.ambient_light, "color"),
                self.create_slider(
                    "Intensity", 0, 2, self.ambient_light, "intensity", step=0.01
                ),
            ],
        )

        self.btn_layout.addStretch(1)

    def add_split(self):
        self.btn_layout.addSpacing(5)
        self.btn_layout.addWidget(QtWidgets.QLabel("-----------------------"))
        self.btn_layout.addSpacing(5)

    def create_color_btn(self, name, target, property, callback=None):
        layout = QtWidgets.QHBoxLayout()

        layout.addWidget(QtWidgets.QLabel(name))

        color_btn = QtWidgets.QPushButton()
        color_btn.setStyleSheet("background-color: %s" % getattr(target, property).hex)

        def set_color():
            color = QtWidgets.QColorDialog.getColor(
                QtGui.QColor(getattr(target, property).hex)
            )
            if color.isValid():
                color_btn.setStyleSheet("background-color: %s" % color.name())
                setattr(target, property, color.name())
                if callback:
                    callback(color.name())

        color_btn.clicked.connect(set_color)

        layout.addWidget(color_btn)
        self.btn_layout.addLayout(layout)
        return color_btn

    def create_checkbox(
        self, name, target=None, property=None, callback=None, toggle=[], index=None
    ):
        checkbox = QtWidgets.QCheckBox(name)

        if target and property:
            checkbox.setChecked(bool(getattr(target, property)))

        def set_property(*args):
            if target and property:
                setattr(target, property, checkbox.isChecked())
            for e in toggle:
                e.setEnabled(checkbox.isChecked())
            if callback:
                callback(checkbox.isChecked())

        checkbox.toggled.connect(set_property)

        set_property()
        if index is not None:
            self.btn_layout.insertWidget(index, checkbox)
        else:
            self.btn_layout.addWidget(checkbox)
        return checkbox

    def create_slider(self, name, min, max, target, property, step=1, callback=None):
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel(name))
        slide = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slide.setMinimum(min / step)
        slide.setMaximum(max / step)
        # slide.setSingleStep(step)
        val = getattr(target, property)
        slide.setValue(val / step)

        if isinstance(step, float):
            val_label = QtWidgets.QLabel(f"{float(val):3.2f}")
        else:
            val_label = QtWidgets.QLabel(f"{int(val):03d}")

        layout.addWidget(val_label)

        def set_value(value):
            value = value * step
            if isinstance(step, float):
                val_label.setText(f"{float(value):3.2f}")
            else:
                val_label.setText(f"{int(value):03d}")
            setattr(target, property, value)
            if callback:
                callback(value)

        slide.valueChanged.connect(set_value)

        layout.addWidget(slide)

        self.btn_layout.addLayout(layout)
        return slide

    def init_scene(self):
        renderer = gfx.renderers.WgpuRenderer(self.wgpu_widget)
        scene = gfx.Scene()
        self.scene = scene

        self.mesh = gfx.Mesh(
            # gfx.box_geometry(20, 20, 20),
            gfx.torus_knot_geometry(10, 3, 128, 32),
            material=gfx.MeshPhongMaterial(color="#00aaff"),
        )

        # mesh.rotation.set_from_euler(gfx.linalg.Euler(math.pi / 6, math.pi / 6))
        scene.add(self.mesh)

        # Point Light1
        point_light1 = gfx.PointLight("#ffffff")
        self.point_light1 = point_light1
        point_light1.position.x = 25
        point_light1.position.y = 20

        light_sp = gfx.sphere_geometry(1)

        self.point_light1_helper = create_pointlight_helper(point_light1, light_sp)
        scene.add(point_light1)

        # Point Light2
        point_light2 = gfx.PointLight("#80ff80")
        self.point_light2 = point_light2
        point_light2.visible = False
        point_light2.position.x = -25
        point_light2.position.y = 20

        self.point_light2_helper = create_pointlight_helper(point_light2, light_sp)
        scene.add(point_light2)

        # Directional light
        directional_light = gfx.DirectionalLight("#ffff00")
        self.directional_light = directional_light
        directional_light.visible = False
        directional_light.position.x = -25
        directional_light.position.y = 20

        self.light3_helper = create_directionallight_helper(directional_light, 20)
        scene.add(directional_light)

        # Ambient light
        self.ambient_light = gfx.AmbientLight()
        scene.add(self.ambient_light)

        camera = gfx.PerspectiveCamera(70, 16 / 9)
        camera.position.z = 50

        controller = gfx.OrbitController(camera.position.clone())
        controller.add_default_event_handlers(renderer, camera)

        t1 = 0
        t2 = 0
        scale = 30

        point_light1.position.x = math.sin(t1 + math.pi / 3) * scale
        point_light1.position.y = math.sin(t1 + 1) * 5 + 15
        point_light1.position.z = math.cos(t1 + math.pi / 3) * scale

        point_light2.position.x = math.sin(t2 - math.pi / 3) * scale
        point_light2.position.y = math.sin(t2 + 2) * 5 + 15
        point_light2.position.z = math.cos(t2 - math.pi / 3) * scale

        def animate():
            if self.mesh_rotate_checkbox.isChecked():
                rot = gfx.linalg.Quaternion().set_from_euler(
                    gfx.linalg.Euler(0.01, 0.02)
                )
                self.mesh.rotation.multiply(rot)

            controller.update_camera(camera)

            nonlocal t1, t2, scale

            if self.point_light1_move.isChecked() and self.point_light1.visible:
                t1 += 0.01
                point_light1.position.x = math.sin(t1 + math.pi / 3) * scale
                point_light1.position.y = math.sin(t1 + 1) * 5 + 15
                point_light1.position.z = math.cos(t1 + math.pi / 3) * scale

            if self.point_light2_move.isChecked() and self.point_light2.visible:
                t2 += 0.02
                point_light2.position.x = math.sin(t2 - math.pi / 3) * scale
                point_light2.position.y = math.sin(t2 + 2) * 5 + 15
                point_light2.position.z = math.cos(t2 - math.pi / 3) * scale

            # light1.position.x = math.cos(t) * math.cos(3*t) * scale
            # light1.position.y = math.cos(3*t) * math.sin(t) * scale
            # light1.position.z = math.sin(3*t) * scale

            renderer.render(scene, camera)
            renderer.request_draw()

        renderer.request_draw(animate)


def create_pointlight_helper(light, geometry=None):
    if geometry is None:
        geometry = gfx.sphere_geometry(1)

    helper = gfx.Mesh(
        geometry,
        gfx.MeshBasicMaterial(color=light.color.hex),
    )
    light.add(helper)
    return helper


def create_directionallight_helper(light, length):
    helper = gfx.Line(
        gfx.Geometry(
            positions=[
                [1, 0, 0],
                [1, 0, 1],
                [-1, 0, 0],
                [-1, 0, 1],
                [0, 1, 0],
                [0, 1, 1],
                [0, -1, 0],
                [0, -1, 1],
            ]
        ),
        gfx.LineArrowMaterial(color=light.color.hex),
    )

    helper.look_at(light.position)
    helper.scale.z = length
    light.add(helper)
    return helper


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = LightViewer()
    window.show()
    app.exec()
