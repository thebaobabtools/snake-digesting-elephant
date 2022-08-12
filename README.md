# snake-digesting-elephant

Tools related to the baobab tools logo

The intention was to create a logo as a 4x4 grid of some images in random ordering,
but I got distracted and started with creating a simplistic bicycle gif.

## A distraction from creating a DIY logo

TLDR

The result is in `resources/output/bicycle.gif`.

### Problems involved, high-level

1. Crop original image: The images are not cropped to only include the relevant part of the image.
1. Crop front- and back wheel.
1. Rotate image crops of wheels.
1. Create gif with rotating wheels.

### Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Image operations using script

#### Cropping

I have not included the original images because of size.

Using fire and the included configuration:

```bash
python main.py generate_cropped_images --config_path resources/config.yml
```

The original images are not only of the drawing so I had to crop them. To actually find the relevant boxes
within the original image, I used commands like this:

```commandline
python main.py crop_image --path 'resources/bicycle.jpeg' --x0 100 --y0 600 --x1 2800 --y1 2500
```

And to quickly see if I had the chosen the right subsection of the image, I did:

```commandline
python main.py crop_image --path 'resources/bicycle.jpeg' --x0 100 --y0 600 --x1 2800 --y1 2500 | show
```

#### Generate bicycle gif

```commandline
python main.py generate_bicycle_gif --config_path resources/config.yml
```

#### Configuration

To easily reproduce the resulting images, I have created a config file.

A next step could be to create github actions instead of this documentation.

