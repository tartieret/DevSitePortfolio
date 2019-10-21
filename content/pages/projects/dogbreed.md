Title: Dog Breed Detector
Date: 2019-04-11 00:00
Authors: me
Summary: Deep learning project to detect dog breeds in images
Template: project_detail
save_as: projects/breed-detector.html
Technologies:python,jupyter,keras,numpy,scikit-learn,flask,javascript,bootstrap4
Images:projects\dogbreed1.png,projects\dogbreed2.png,projects\dogbreed3.png
repository:https://github.com/tartieret/DogBreedDetector
video:

## Project description

In this project, I built a pipeline that can be used within a web or mobile app to process real-world, user-supplied images. Given an image of a dog, the algorithm will identify an estimate of the canine’s breed. If supplied an image of a human, the code will identify the resembling dog breed.

In the first part of the project, I worked in a Jupyter notebook to perform the following steps:

1. Use Haar feature-based cascade classifiers to detect human faces in images
2. Use a pre-trained (on ImageNet) ResNet-50 model to detect dogs in images
3. Design a CNN architecture to identify dog breeds
4. Use Transfer Learning from VGG16 to identify dog breeds
5. Use Transfer Learning from GoogLeNet to identify dog breeds

My own CNN architecture (step 3) reached a 35.76% accuracy on the test set, well above the minimum requirements for the project (1%). It was trained for 4 hours on a GPU. However, using transfer learning from the Inception/GoogLeNet was very successful with a final accuracy of 80.5%.

Check the [Jupyter notebook](https://github.com/tartieret/DogBreedDetector/blob/master/dog_app.ipynb) for more details.

## Web application

In a second step, I built a Flask web application to serve the model through a Bootstrap/JQuery web interface. The full code is available [on Github](https://github.com/tartieret/DogBreedDetector).
