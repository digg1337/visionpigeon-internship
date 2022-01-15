1.
I would use a simplified version of K-means algorithm. At the beginning I would select 'K' constant centroids that would represent the colour bins. The next step would be assigning an image to his nearest centroid (colour) based on the selected metric.

The question is if it would not be appropirate to do some preprocessing first. The preprocessing which I would do is again - K-means clustering. I would preprocess each image using K-means clustering in such way that only the most dominant colours would remain present.

In conclusion, I would:
1) Preprocess image to contain only its most dominant colours
2) Assign image to closest predefined centroid which represents the final colour

2.
The question is how the similarity between product is defined. Generally I would use the K-NN algorithm and using this algorithm I would find 10 closest products. The advantage is that i choose what 'similarity' is, because I choose the metric function.

Maybe there would be appropirate to do some preprocessing first. At first, I would like to have all images with the same size and also I would like to keep the size as small as possible, because of performance.

In conclusion, I would:
1) Shrink the images to same size
2) Build K-NN classifier
2) Find 10 nearest neighbours of the image using our classifier