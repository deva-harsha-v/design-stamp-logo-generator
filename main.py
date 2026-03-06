import math
from tkinter import *
from tkinter import filedialog, colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk


class LogoCreator:

    CANVAS_SIZE = 700

    def __init__(self, root):

        self.root = root
        self.root.title("Logo Creator Pro")
        self.root.geometry("1200x850")
        self.root.configure(bg="#1e1e1e")

        self.text = "Your Logo"
        self.font_size = 80
        self.font_color = "#ffffff"
        self.bg_color = "#1e90ff"

        self.font_path = None
        self.icon_image = None
        self.generated_logo = None

        self.shape_choice = IntVar(value=1)

        self.build_ui()
        self.generate_logo()

    # -----------------------
    # UI
    # -----------------------

    def build_ui(self):

        control_frame = Frame(self.root, bg="#2c2c2c", width=300)
        control_frame.pack(side=LEFT, fill=Y, padx=15, pady=15)

        preview_frame = Frame(self.root, bg="#1e1e1e")
        preview_frame.pack(side=RIGHT, expand=True)

        Label(
            control_frame,
            text="Logo Settings",
            bg="#2c2c2c",
            fg="white",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # TEXT
        Label(control_frame, text="Logo Text", bg="#2c2c2c", fg="white").pack()

        self.text_entry = Entry(control_frame, width=25)
        self.text_entry.insert(0, self.text)
        self.text_entry.pack(pady=5)

        # Live text update
        self.text_entry.bind("<KeyRelease>", lambda e: self.generate_logo())

        # FONT SIZE
        Label(control_frame, text="Font Size", bg="#2c2c2c", fg="white").pack()

        self.font_slider = Scale(
            control_frame,
            from_=20,
            to=200,
            orient=HORIZONTAL,
            command=self.update_font_size
        )

        self.font_slider.set(self.font_size)
        self.font_slider.pack()

        # COLORS
        Button(control_frame, text="Font Color", command=self.choose_font_color).pack(pady=5)
        Button(control_frame, text="Background Color", command=self.choose_bg_color).pack(pady=5)

        # FONT + ICON
        Button(control_frame, text="Choose Font", command=self.choose_font).pack(pady=5)
        Button(control_frame, text="Upload Icon", command=self.upload_icon).pack(pady=5)

        # SHAPES
        Label(control_frame, text="Shape", bg="#2c2c2c", fg="white").pack(pady=10)

        shapes = [
            ("Circle", 1),
            ("Rectangle", 2),
            ("Triangle", 3),
            ("Hexagon", 4),
            ("Pentagon", 5),
            ("Octagon", 6)
        ]

        for name, val in shapes:

            Radiobutton(
                control_frame,
                text=name,
                variable=self.shape_choice,
                value=val,
                bg="#2c2c2c",
                fg="white",
                selectcolor="#2c2c2c",
                command=self.generate_logo
            ).pack(anchor="w")

        Button(control_frame, text="Generate Logo", command=self.generate_logo).pack(pady=10)
        Button(control_frame, text="Save Logo", command=self.save_logo).pack(pady=10)

        # CANVAS
        self.canvas = Canvas(
            preview_frame,
            width=self.CANVAS_SIZE,
            height=self.CANVAS_SIZE,
            bg="white",
            highlightthickness=0
        )

        self.canvas.pack(pady=30)

    # -----------------------
    # FONT SIZE UPDATE
    # -----------------------

    def update_font_size(self, value):

        self.font_size = int(value)
        self.generate_logo()

    # -----------------------
    # COLORS
    # -----------------------

    def choose_font_color(self):

        color = colorchooser.askcolor()[1]

        if color:
            self.font_color = color
            self.generate_logo()

    def choose_bg_color(self):

        color = colorchooser.askcolor()[1]

        if color:
            self.bg_color = color
            self.generate_logo()

    # -----------------------
    # FILES
    # -----------------------

    def choose_font(self):

        path = filedialog.askopenfilename(
            filetypes=[("Font files", "*.ttf *.otf")]
        )

        if path:
            self.font_path = path
            self.generate_logo()

    def upload_icon(self):

        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg")]
        )

        if path:

            try:
                self.icon_image = Image.open(path).convert("RGBA")
                self.generate_logo()

            except:
                print("Invalid image")

    # -----------------------
    # SHAPE GENERATOR
    # -----------------------

    def polygon_points(self, sides, center, radius):

        cx, cy = center

        return [
            (
                cx + radius * math.cos(2 * math.pi * i / sides),
                cy + radius * math.sin(2 * math.pi * i / sides)
            )
            for i in range(sides)
        ]

    def draw_shape(self, draw, size):

        w, h = size
        center = (w // 2, h // 2)
        r = w // 3

        shape = self.shape_choice.get()

        if shape == 1:

            draw.ellipse([center[0]-r, center[1]-r, center[0]+r, center[1]+r], fill=self.bg_color)

        elif shape == 2:

            draw.rectangle([100, 100, w-100, h-100], fill=self.bg_color)

        elif shape == 3:

            points = [
                (center[0], center[1]-r),
                (center[0]-r, center[1]+r),
                (center[0]+r, center[1]+r)
            ]

            draw.polygon(points, fill=self.bg_color)

        elif shape == 4:

            draw.polygon(self.polygon_points(6, center, r), fill=self.bg_color)

        elif shape == 5:

            draw.polygon(self.polygon_points(5, center, r), fill=self.bg_color)

        elif shape == 6:

            draw.polygon(self.polygon_points(8, center, r), fill=self.bg_color)

    # -----------------------
    # LOGO GENERATION
    # -----------------------

    def generate_logo(self):

        self.text = self.text_entry.get()
        self.font_size = self.font_slider.get()

        size = (self.CANVAS_SIZE, self.CANVAS_SIZE)

        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        self.draw_shape(draw, size)

        # FONT FIX
        try:

            if self.font_path:
                font = ImageFont.truetype(self.font_path, self.font_size)

            else:
                font = ImageFont.truetype("DejaVuSans-Bold.ttf", self.font_size)

        except:

            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), self.text, font=font)

        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

        x = (size[0] - tw) // 2
        y = (size[1] - th) // 2

        # SHADOW
        draw.text((x+4, y+4), self.text, font=font, fill="black")

        # TEXT
        draw.text((x, y), self.text, font=font, fill=self.font_color)

        # ICON
        if self.icon_image:

            icon = self.icon_image.resize((120, 120))

            img.paste(
                icon,
                (size[0]//2 - 60, size[1]//2 - 200),
                icon
            )

        self.generated_logo = img
        self.display_logo()

    # -----------------------
    # DISPLAY
    # -----------------------

    def display_logo(self):

        preview = self.generated_logo.resize((self.CANVAS_SIZE, self.CANVAS_SIZE))

        self.tk_img = ImageTk.PhotoImage(preview)

        self.canvas.delete("all")

        self.canvas.create_image(
            self.CANVAS_SIZE//2,
            self.CANVAS_SIZE//2,
            image=self.tk_img
        )

    # -----------------------
    # SAVE
    # -----------------------

    def save_logo(self):

        if not self.generated_logo:
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")]
        )

        if path:
            self.generated_logo.save(path)


# -----------------------
# MAIN
# -----------------------

if __name__ == "__main__":

    root = Tk()
    app = LogoCreator(root)
    root.mainloop()
