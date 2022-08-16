import torch
import csv
import os
import cv2 
from PIL import Image 
import numpy as np
import pandas as pd
from torch.autograd import Variable
import matplotlib.pyplot as plt

 
class LinearRegressionModel(torch.nn.Module):

	def __init__(self, input_size,outpot_size,):
		super(LinearRegressionModel, self).__init__()
		self.linear = torch.nn.Linear(input_size, outpot_size) # One in and one out

	def forward(self, x):
		y_pred = self.linear(x)
		return y_pred

def generate_video():
	image_folder = '../data/figures/' 
	outpot_path = '../data/outpot'
	os.makedirs(outpot_path, exist_ok=True)
	video_name = os.path.join(outpot_path, " my_model_output.avi")
	images = [img for img in os.listdir(image_folder)
			  if img.endswith(".jpg") or
				 img.endswith(".jpeg") or
				 img.endswith("png")]
	images = sorted(images,key=lambda fname: int(fname.split('.')[0]))
	frame = cv2.imread(os.path.join(image_folder, images[0]))
	height, width, layers = frame.shape  
	video = cv2.VideoWriter(video_name, 0, 1, (width, height)) 
	for image in images: 
		video.write(cv2.imread(os.path.join(image_folder, image))) 
	cv2.destroyAllWindows() 
	video.release()  

def visualize(point_lists,xp,y_data,i,epo,n_epoch):
	ax = plt.axes(projection ='3d')
	color,alpha = ("y",0.2)
	if epo==n_epoch-1:
		color,alpha = ("b",0.5)
	ax.plot_surface(point_lists[0][0], point_lists[1][0], point_lists[2][0], alpha=alpha, color=color)
	ax.scatter3D(xp[:,0], xp[:,1],y_data,c="r")
	ax.set_xlim([0, 85])
	ax.set_ylim([0, 35])
	ax.set_zlim([0, 30])
	ax.set_title("This dataset have two independed features (x1,x2)\nand one depended variable (Y)")
	ax.set_xlabel('X1',fontsize=20,labelpad=12)
	ax.set_ylabel('X2',fontsize=20,labelpad=12)
	ax.set_zlabel('Y',fontsize=20, labelpad=12)
	save_frames_path = "../data/figures"
	os.makedirs(save_frames_path, exist_ok=True)
	ax.figure.savefig(save_frames_path + "/" + str(i) +  ".png")
	ax.destroyAllWindows()
	print("sived figure :",i)
			
def drow_surface(tetha_0, tetha_12, point_lists):
	xx, yy = np.meshgrid(range(-5,80), range(-5,35))
	z = (-tetha_12[0] * xx - tetha_12[1] * yy - tetha_0) * 1. /(-1)
	point_lists[0].append(xx)
	point_lists[1].append(yy)
	point_lists[2].append(z)

def read_data(dirc):
	df = pd.read_csv(dirc)
	columns = df.columns.values
	x = df.loc[:,columns[1]:columns[columns.shape[0]-2]]
	y = df.loc[:,columns[-1]]
	x =  x.values.reshape(x.shape[0],x.shape[1])
	y =  y.values.reshape(y.shape[0],1)
	x_data = Variable(torch.Tensor(x))
	y_data = Variable(torch.Tensor(y))
	return x_data , y_data

x_data , y_data = read_data('../data/heart.data.csv')
xp = x_data # >> for plot;beacuse x_data must be shuffle
# define parameters
input_size, output_size = (x_data.shape[1],y_data.shape[1])
learning_rate = 0.01
n_epoch = 300
batch_size = 25
EIO = 25             # Every itreation once plot
iteration = int(x_data.shape[0]/batch_size)

#define model
our_model = LinearRegressionModel(input_size,output_size)
criterion = torch.nn.MSELoss(size_average = True)
optimizer = torch.optim.Adam(our_model.parameters(), lr = learning_rate)
i = 0
for epoch in range(n_epoch):
	start,stop = (0,0)
	for iteer in range(iteration):
		X = x_data[0+start:batch_size+stop]
		Y = y_data[0+start:batch_size+stop]
		pred_y = our_model(X)
		loss = criterion(pred_y, Y)
		optimizer.zero_grad()
		loss.backward()
		optimizer.step()
		# print('epoch {}, iteration {}, loss {}'.format(epoch, iteer, loss.item()))
	x_data = x_data[torch.randperm(x_data.size()[0])]  # shuffle data
	if epoch %EIO==0 or epoch==n_epoch-1:
		# print("=============================================")
		point_lists = [[],[],[]]
		tetha_0 = our_model.linear.bias.tolist()[0]
		tetha_12 = our_model.linear.weight.tolist()[0]
		# print("Intereptc:",tetha_0,"\nCoefficients(tetha_1....tetha2):",tetha_12)
		drow_surface(tetha_0, tetha_12, point_lists)
		print("=============================================")
		visualize(point_lists,xp,y_data,i,epoch,n_epoch)
		i+=1

print("=================== Model trained ========================")
generate_video()

'''
Intereptc: 15.01642374536851 
Coefficients(theta_1 ... theta_n): [-0.20059503  0.17741778]
'''