"""
Plots multiple images in one graph
==================================

Or a kind of *gallery*.
Let's first get a list of images.
"""
import os
from pyensae.datasource import download_data
zipname = "dog-cat-pixabay.zip"
if not os.path.exists("images"):
    os.mkdir("images")
res = download_data(zipname, whereTo="images")
print(res)

#################################
# Let's take the first ten images.

imgs = res[:10]

#################################
# And the gallery.

from mlinsights.plotting import plot_gallery_images
txts = ["img%d" % i for i in range(len(imgs))]
plot_gallery_images(imgs, txts)
