# Simple Linear Regression by Pythorch:
You can study SLR definition in SLR project folder; and also:
PyTorch is an open source machine learning library that specializes in tensor computations, automatic differentiation, and GPU acceleration. For those reasons, PyTorch is one of the most popular deep learning libraries.

## My Project:
* Dataset : My dataset is the one i used for the SLR project >>> LINK : https://cdn.scribbr.com/wp-content/uploads//2020/02/income.data_.zip
### Code :
* step_1 : Read the dataset and set the properties and labels in the x_data,y_data values as a tensor. 
* step_2 : defining nn.linear regression class of torch library with  input size of features.
* step_3 : set other parameters, like: Learning reat, batch size, number of epoch and etc.
* step_4 : define model,criterion,optimizer. i used to MSE loss function for criterion, and Adam method for optimizer.
* step_5 : In the main part of the code i have implemented two "for" loops. in each iteration of the inner loop, i give a batch size of data to the input of the model. finally, using the mimimum and maximum data and the line equation obtained from the model, i plotted the final line.

* important point : you have to tion tha parameters (Learning reat, batch size,n_epoch) according to your dataset.


##### figures:

<img src="data/Figure_1.png" width="1200" height="600">
<img src="data/Figure_2.png" width="1200" height="600">
<img src="data/Figure_3.png" width="1200" height="600">

