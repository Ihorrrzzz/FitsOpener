import tkinter as tk
from tkinter import filedialog, Toplevel
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FitsViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FITS File Viewer")

        # Get screen width and height
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        # Set window size to maximum screen resolution
        self.geometry(f"{self.screen_width}x{self.screen_height}")

        self.open_button = tk.Button(self, text="Choose Files", command=self.open_files)
        self.open_button.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

        self.calibration_button = tk.Button(self, text="Set Calibration", command=self.set_calibration)
        self.calibration_button.grid(row=0, column=1, padx=10, pady=10, sticky='nw')

        self.upload_to_BHTOM_button = tk.Button(self, text="Upload to BHTOM", command=self.upload_to_BHTOM)
        self.upload_to_BHTOM_button.grid(row=0, column=2, padx=10, pady=10, sticky='nw')

        self.clear_button = tk.Button(self, text="Clear", command=self.clear_windows)
        self.clear_button.grid(row=0, column=3, padx=10, pady=10, sticky='nw')

        self.window_count = 0  # To track the number of opened windows for cascading effect
        self.open_windows = []  # To keep track of all opened Toplevel windows

        # Bind minimize and restore events to handle topmost attribute
        self.bind("<Unmap>", self.on_minimize)
        self.bind("<Map>", self.on_restore)

    def open_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("FITS files", "*.fits *.fit")])
        for file_path in file_paths:
            self.display_fits(file_path)

    def display_fits(self, file_path):
        window = Toplevel(self)
        window.title(f"FITS File: {file_path}")
        window.attributes('-topmost', True)  # Keep the window always on top

        # Calculate cascading position
        x_offset = 15 * self.window_count
        y_offset = 15 * self.window_count
        window.geometry(f"600x600+{x_offset}+{y_offset}")
        self.window_count += 1
        self.open_windows.append(window)  # Track the opened window

        hdul = fits.open(file_path)
        info_text = tk.Text(window, height=5)
        info_text.pack(fill=tk.BOTH, expand=True)
        info_text.insert(tk.END, hdul.info(output=False))

        image_data = hdul[0].data

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(image_data, cmap='gray', aspect='auto')
        ax.set_title("FITS Image")
        plt.axis('off')  # Hide axes for better space usage

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        hdul.close()

    def lift_window(self, event):
        window = event.widget.winfo_toplevel()
        for win in self.open_windows:
            win.attributes('-topmost', False)
        window.attributes('-topmost', True)

    def close_window(self, window):
        self.open_windows.remove(window)
        window.destroy()
        self.window_count -= 1

    def on_minimize(self, event):
        # Set the -topmost attribute of all Toplevel windows to False
        for window in self.open_windows:
            window.withdraw()
            window.attributes('-topmost', False)

    def on_restore(self, event):
        # Set the -topmost attribute of all Toplevel windows to True
        for window in self.open_windows:
            window.deiconify()
            window.attributes('-topmost', True)

    def clear_windows(self):
        # Close all opened Toplevel windows
        for window in self.open_windows:
            window.destroy()
        self.open_windows.clear()
        self.window_count = 0  # Reset window count

    def set_calibration(self):
        # This function can be expanded to handle calibration settings
        print("Set Calibration button clicked")

    def upload_to_BHTOM(self):
        # This function can be expanded to handle calibration settings
        print("Upload to BHTOM button clicked")

if __name__ == "__main__":
    app = FitsViewer()
    app.mainloop()
