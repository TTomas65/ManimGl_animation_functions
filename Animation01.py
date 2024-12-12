from manimlib import *
import numpy as np

class Epicycloid(Scene):
    def setup(self):
        self.number_of_lines = 400
        self.gradient_colors = [ORANGE, YELLOW, BLUE]
        self.end_value = 40
        self.total_time = 40
        # Forgási beállítások
        self.rotation_axis = RIGHT  # Választható: OUT (Z tengely), RIGHT (X tengely), UP (Y tengely)
        self.rotation_speed = 0.3
        # 3D beállítások - külön skálázás mindhárom tengelyre
        self.height_scale = {
            'x': 2.0,  # X irányú kiemelés (RIGHT)
            'y': 2.0,  # Y irányú kiemelés (UP)
            'z': 0.0   # Z irányú kiemelés (OUT)
        }

    def construct(self):
        self.setup()
        # Create circle in the center
        circle = Circle().set_height(FRAME_HEIGHT*0.9)
        circle.move_to(ORIGIN)
        
        mod_tracker = ValueTracker(0)
        lines = self.get_m_mod_n_objects(circle, mod_tracker.get_value())
        lines.add_updater(
            lambda mob: mob.become(
                self.get_m_mod_n_objects(circle, mod_tracker.get_value())
            )
        )

        # Create a rotation updater for the entire pattern
        pattern = VGroup(circle, lines)
        pattern.add_updater(
            lambda m, dt: m.rotate(
                angle=self.rotation_speed * dt,
                axis=self.rotation_axis,
                about_point=ORIGIN
            )
        )

        # Add circle and lines instantly
        self.add(pattern)
        
        # Animate the value tracker quickly
        self.play(
            ApplyMethod(
                mod_tracker.set_value, 
                self.end_value,
                run_time=self.total_time,
                rate_func=linear
            )
        )

    def get_m_mod_n_objects(self, circle, x, y=None):
        if y is None:
            y = self.number_of_lines
        lines = VGroup()
        for i in range(y):
            # Kezdőpont a körön
            start_point = circle.point_from_proportion((i%y)/y)
            
            # Végpont számítása
            end_prop = ((i*x)%y)/y
            base_end_point = circle.point_from_proportion(end_prop)
            
            # A végpont kiemelése a térben mindhárom irányban
            angle = end_prop * 2 * PI
            offset = np.array([
                self.height_scale['x'] * np.sin(angle),  # X irányú kiemelés
                self.height_scale['y'] * np.cos(angle),  # Y irányú kiemelés
                self.height_scale['z'] * np.sin(angle)   # Z irányú kiemelés
            ])
            end_point = base_end_point + offset
            
            # Vonal létrehozása
            line = Line(start_point, end_point).set_stroke(width=1)
            lines.add(line)
            
        lines.set_color_by_gradient(*self.gradient_colors)
        return lines