import datetime
import glob
import os
from pathlib import Path

import git # pip install gitpython
from PIL import Image #pip install Pillow


def crop(input_img, coords, output_img):
    """
    @param input_img: Path and name of the image to crop
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    @param saved_location: Path and name of the cropped image to save
    """
    image_obj = Image.open(input_img)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(output_img)


if __name__ == '__main__':
    home = str(Path.home())
    img_dir = os.path.join(home, 'Dropbox', 'Apps', 'Test')
    repo_dir = os.path.join(img_dir, 'test')

    # yyyymmdd = datetime.datetime.today().strftime('%Y%m%d')
    # img_file_name = ''.join([yyyymmdd, '.jpg'])
    img_files = glob.glob(os.path.join(img_dir, '*.jpg'))
    img_files += glob.glob(os.path.join(img_dir, '*.png'))
    img_files.sort(key=os.path.getmtime)
    last_modified_img = img_files[-1]
    img_modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(last_modified_img)).date()
    today_date = datetime.datetime.today().date()

    # REFs: https://stackoverflow.com/q/1456269
    # https://gitpython.readthedocs.io/en/stable/tutorial.html#handling-remotes
    repo = git.Repo(repo_dir)
    repo.remotes.origin.pull() # first, try to sync the repo with remote

    if img_modified_date == today_date:
        for img_coord in [('a.png', (100, 100, 101, 375)), # big box
                          ('b.png', (522, 81, 812, 370)), # b c
                          ('c.png', (40, 580, 1294, 618))]: #(22, 630, 1310, 669))]: # three colors
            output_img = os.path.join(repo_dir , img_coord[0])
            print("Starting to crop the image at:", last_modified_img)
            crop(last_modified_img, img_coord[1], output_img)
            print("Wrote cropped image at:", output_img)
            repo.git.add(img_coord[0])
            print("This image file is added to git repo:", img_coord[0])

        repo.git.commit(m="Test commit")
        print("Committed recently added image files.")
        repo.remotes.origin.push()
        print("Pushed committed image files to remote repo.")
        print(repo.git.status())
        print("Image cropped and committed to the Github repo.\n")
    else:
        print("No image with modified date set to TODAY found.\n")