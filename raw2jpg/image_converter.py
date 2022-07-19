from time import sleep
from tkinter import Tk, filedialog
from os import listdir, path, makedirs
from rawpy import imread
from cv2 import cvtColor, COLOR_RGB2BGR, imwrite
from multiprocessing import Pool, freeze_support
from tqdm import tqdm


class raw2jpg:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.output_folder = path.join(folder_path, "converted")
        if not path.isdir(self.output_folder):
            makedirs(self.output_folder)
        self.raw_counter = 0

    def main(self):
        images = listdir(self.folder_path)

        image_paths = []
        for image_path in images:
            if image_path.endswith(".CR2"):
                image_paths.append(path.join(self.folder_path, image_path))
                self.raw_counter += 1

        with Pool() as p:
            r = list(tqdm(p.imap(self.save_image, image_paths), total=self.raw_counter))
        p.close()
        p.join()

    def save_image(self, image):
        raw = imread(image)
        rgb = raw.postprocess()  # a numpy RGB array
        out_img_path = path.join(self.output_folder, path.basename(image)[:-4] + ".jpg")
        out_image = cvtColor(rgb, COLOR_RGB2BGR)
        imwrite(out_img_path, out_image)
        sleep(1)


if __name__=="__main__":
    Tk().withdraw()
    folder_path = filedialog.askdirectory()
    if not folder_path:
        exit()

    freeze_support()
    converter = raw2jpg(folder_path)
    converter.main()
