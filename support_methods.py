# support method to draw images as subplots
from collections import namedtuple
from colorama import Fore, Style
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

Subplot = namedtuple('Subplot', ['image', 'cmap', 'title'])


def draw_subplots(subplots, n_rows, n_cols, figsize=(10, 10)):
    fig, ax = plt.subplots(n_rows, n_cols, figsize=figsize)
    for i in range(len(subplots)):
        subplot = subplots[i]
        ax[i].imshow(subplot.image, cmap=subplot.cmap)
        ax[i].set_title(subplot.title)
        # remove axis ticks
        ax[i].axis('off')
    plt.show()


def convert_float_to_uint8(img):
    return (img).astype(np.uint8)


def convert_png_to_jpg(png):
    # reduce channels from 4 to 3 and convert to uint8
    png_to_jpg = png[:, :, :3] * 255
    return convert_float_to_uint8(png_to_jpg)


# to print the first and last row's 6 pixels of the center columns of the images for comparison
def print_6_first_and_last_rows_center_pixels(images, indexes):
    tabular_data = []
    for i in range(len(images)):
        image = images[i]
        center_column_index = int(image.shape[1] / 2)
        center_range = [center_column_index - 3, center_column_index + 3]
        last_row_inex = image.shape[0] - 1
        tabular_data.append([indexes[i], [image[0, center_range[0]:center_range[1], :]], [
                            image[last_row_inex, center_range[0]:center_range[1], :]]])
    tabulated = tabulate(tabular_data, headers=[
                         'Image', '6 pixels of the first row', '6 pixels of the last row'], tablefmt='fancy_grid')
    print(tabulated)


# to print description
def print_pixels_comparison_description(image1, image2):
    print(f'6 center pixels of {Fore.RED}the first row {Style.RESET_ALL}of {Fore.RED}{image1} image {Style.RESET_ALL}is the same as\n'
          f'6 center pixels of {Fore.GREEN}the last row {Style.RESET_ALL}of {Fore.GREEN}{image2} image{Style.RESET_ALL} '
          f'but {Fore.BLUE}in the reverse{Style.RESET_ALL} order.\nThe same about 6 center pixels of the last row of {image1} image '
          f'and 6 center pixels of the first row of {image2} image.')


# to plot histogram
def plot_histogram(regular_average, weighted_average):
    plt.hist(regular_average.ravel(), bins=256, color='purple', alpha=0.5)
    plt.hist(weighted_average.ravel(), bins=256, color='yellow', alpha=0.5)
    plt.rcParams['figure.figsize'] = (15, 5)
    plt.xlabel('Intensity Value')
    plt.ylabel('Count')
    plt.legend(['Regular Average', 'Weighted Average'])
    plt.xticks(np.arange(0, 256, 25))
    plt.show()


def threshold_image(img, threshold):
    return (img > threshold).astype('uint8') * 255
