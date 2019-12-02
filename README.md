# Introduction
My first repo playing around with Keras. Still waiting on my CoreX Chroma eGPU to run heavier models.

## CNN
Simply convolutional neural network that is trained on images of cats and dogs.   

first layer -> convolution (32 filters, 3x3) + ReLu  
second layer -> MaxPooling (2x2)  
Third layer -> convolution (64 filters, 3x3) + ReLu  
Fourth layer -> MaxPooling (2x2)  
-> Flatten convolution output  
Fifth layer -> ANN 128 neuron input + ReLu  
Sixth layer -> ANN 32 neuron fully connected layer + ReLu  
Final layer -> single neruon output for binary classification with a sigmoid activation function. Also tested with softmax.   

I used an adam optimizer (similar but not really stochastic gradient descent)
The loss function is binary cross entropy. There is also a 50% dropout in the ANN.  

The model is trained on 8000 images of cats and dogs, and tested on 2000. Max accuracy in 91%.   

## Future work 
Add cross validation  
Expand binary detection to multiple class detections  
Train model on coffee capsules and test on robotic arm with single predictions  


