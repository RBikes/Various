{
    'name': 'Website Image Lightbox',
    'category': 'Website',
    'summary': 'Allow to use classes of lightbox',
    'version': '1.0',
    'description': """Allow to use classes of lightbox
Allow to use classes of lightbox
Add a data-lightbox attribute to any image link to activate Lightbox.
For the value of the attribute, use a unique name for each image.
For example:
<a href="img/image-1.jpg" data-lightbox="image-1" 
data-title="My caption">Image #1</a>

Optional: Add a data-title attribute if you want to show a caption.
If you have a group of related images that you would like to combine 
into a set, use the same data-lightbox attribute value for all of the 
images. For example:
<a href="img/image-2.jpg" data-lightbox="roadtrip">Image #2</a>
<a href="img/image-3.jpg" data-lightbox="roadtrip">Image #3</a>
<a href="img/image-4.jpg" data-lightbox="roadtrip">Image #4</a>""",
    'author': 'Omar Castiñeira Saavedra',
    'depends': ['website'],
    'installable': True,
    'data': ['views/website_lightbox_view.xml'],
}
