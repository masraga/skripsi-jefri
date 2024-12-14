from helpers.lbp import train_model
from helpers.haar import crop_image

print("Preprocessing data")
crop_image()
print("Training data")
train_model(is_train=True)
print("Application ready to use")