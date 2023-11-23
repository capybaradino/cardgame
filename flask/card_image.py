from PIL import Image, ImageFilter

ALLOWED_EXTENSIONS = set(["png", "jpg"])
ALLOWED_FORMATS = set(["PNG", "JPEG"])


def checksize(tmpfile):
    im = Image.open(tmpfile)
    if im is None:
        return False
    if not im.format in ALLOWED_FORMATS:
        return False
    if (im.width != 600) | (im.height != 800):
        return False

    return True
