window.onload = function () { // Executes an anonymous function after the page has been parsed
    var n, // For looping
        images = [], // Object container
        imageData = [ // Nested array containing data for images
            [
                {src: "/website/image/product.template/2889_d789084/image"},
                {src: "/website/image/product.template/2891_09bd536/image"}
            ],
            [
                {src: "/website/image/product.template/2891_06fe917/image"},
                {src: "/website/image/product.template/2890_530a6cb/image"}
            ],
            [
                {src: "/website/image/product.template/2892_9022063/image"},
                {src: "/website/image/product.template/2893_58b2c94/image"}
            ],
            [
                {src: "/website/image/ir.attachment/966_124c4c6/datas"},
                {src: "/website/image/ir.attachment/969_4b0708a/datas"}
            ]
        ],
        len = imageData.length, // Tells how many image elements have data in imageData array
        ImageChanger = function (item) { // Constructs an object, which changes srcs and captions of the image elements
            var imageInfo = imageData[item], // Data for the image element
                imgElement = document.getElementById('image' + item), // Reference to the image element
                imgCaption = document.getElementById('caption' + item), // Reference to the caption element
                current = 0, // Tracks the current image in image element, represents an index in imageInfo array
                changeImage = function () { // Changes path for the image element
                    current = (++current > imageInfo.length - 1) ? 0 : current; // If there are more images to show, increases the tracker by one. Otherwise resets the tracker
                    imgElement.src = imageInfo[current].src; // Sets new path to the image element
                    imgCaption.innerHTML = imageInfo[current].caption; // Sets new content to the caption
                    return;
                };

            document.getElementById('click' + item).onclick = changeImage; // Sets eventhandler for #click button
        };
    for (n = 0; n < len; n++) {
        images[n] = new ImageChanger(n); // Creates an individual ImageChanger object for each image element (whose id is 'image' + n) in the document
    }
    document.getElementById('restore').onclick = function () { // Sets eventhandler for #restore button
        var n;
        for (n = 0; n < len; n++) {
            images[n].restore(); // Invokes the restore method in every ImageChanger object
        }
        return;
    };
    return;
}