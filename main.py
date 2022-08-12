from PIL import Image
import imageio
import fire
import yaml


def crop_image(path: str, x0: int, y0: int, x1: int, y1: int):
    im = Image.open(path)
    box = (x0, y0, x1, y1)
    return im.crop(box)


def size_image(path: str):
    im = Image.open(path)
    return im.size


def rotate_boxes(im: Image, boxes, rotation):
    new_im = Image.new("RGBA", im.size)
    new_im.paste(im)
    for box in boxes:
        box_region = im.crop(box)
        box_region_rotated = box_region.rotate(rotation)
        new_im.paste(box_region_rotated, (box[0], box[1]))
    return new_im.convert('RGB')


def merge_horizontal(im1, im2):
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGBA", (w, h))

    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))

    return im


def merge_vertical(im1, im2):
    w = max(im1.size[0], im2.size[0])
    h = im1.size[1] + im2.size[1]
    im = Image.new("RGBA", (w, h))

    im.paste(im1)
    im.paste(im2, (0, im1.size[1]))

    return im


def config_as_dict(config_path):
    with open(config_path, 'r') as s:
        try:
            config = yaml.safe_load(s)
            return config
        except yaml.YAMLError as exc:
            raise exc


def generate_cropped_images(config_path: str):
    config = config_as_dict(config_path)
    thumbnail_size = config['thumbnail']['size']
    for im in config['crop_images']:
        cropped = crop_image(im['path'], im['x0'], im['y0'], im['x1'], im['y1'])
        cropped.thumbnail((thumbnail_size['x'], thumbnail_size['y']))
        cropped.save(im['out_path'])


def generate_bicycle_gif(config_path: str):
    config = config_as_dict(config_path)['bicycle_gif']
    im_path = config['bicycle_image_path']
    im = Image.open(im_path)
    wheels = config['wheels']
    wheel_boxes = [(wheel['x0'], wheel['y0'], wheel['x1'], wheel['y1']) for wheel in wheels]
    rotation_images = [rotate_boxes(im, wheel_boxes, rotation) for rotation in config['rotations']]
    imageio.mimsave(config['gif_out_path'], rotation_images, duration=config['duration'])


if __name__ == '__main__':
    fire.Fire()
