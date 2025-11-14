import tkinter as tk
from tkinter import Button, Label, filedialog

from PIL import Image, ImageTk


# Placeholder for your model inference method
def model_inference(image_path):
    # Here, replace this stub with actual model inference code
    # For example, load the image and run your model
    print(f"Model inference called on: {image_path}")
    # Return dummy result for demonstration
    return "Projectile type: Grenade\nConfidence: 87%"


class OrdnanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ordnance Recognition Demo")
        self.root.geometry("800x600")  # Make window bigger: 800x600 pixels

        self.image_path = None  # Store path of the loaded image

        # Button to upload image
        self.upload_btn = Button(
            root, text="Upload Projectile Photo", command=self.upload_image
        )
        self.upload_btn.pack(pady=10)

        # Label to show the image
        self.image_label = Label(root)
        self.image_label.pack(pady=10)

        # Button to run recognition on loaded image
        self.recognize_btn = Button(
            root,
            text="Run Recognition",
            command=self.run_recognition,
            state=tk.DISABLED,
        )
        self.recognize_btn.pack(pady=10)

        # Label for displaying model result
        self.result_label = Label(root, text="", justify="left")
        self.result_label.pack(pady=10)

    def upload_image(self):
        # Open file dialog to select image
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if not file_path:
            return

        self.image_path = file_path

        # Load and display image
        img = Image.open(file_path)
        img.thumbnail((600, 400))  # Resize larger for display in bigger window
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk  # Keep reference to avoid garbage collection

        # Clear previous result and enable recognition button
        self.result_label.configure(text="")
        self.recognize_btn.config(state=tk.NORMAL)

    def run_recognition(self):
        if self.image_path:
            result_text = model_inference(self.image_path)
            self.result_label.configure(text=result_text)
        else:
            self.result_label.configure(text="Please upload an image first.")


if __name__ == "__main__":
    root = tk.Tk()
    app = OrdnanceApp(root)
    root.mainloop()
