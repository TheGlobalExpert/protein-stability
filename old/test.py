import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from res_tools import res_in_range, get_ASA


#----Parameters----#

residue_range = 5

#----Load and prepare dataset----#

dataset = pd.read_csv("HotMusic_dataset.csv")


for i in range(dataset.shape[0]):
	try:
		dataset.loc[i, "Temp"] = int(dataset.loc[i, "Temp"])
		dataset.loc[i, "ddG"] = float(dataset.loc[i, "ddG"])
	except:
		dataset.drop(i, inplace=True)
dataset.reset_index(inplace=True)

variations = list(dataset["Variation"])

for i, variation in enumerate(variations):
	dataset.loc[i,"wt"] = variation[0]
	dataset.loc[i,"mut"] = variation[-1]
	dataset.loc[i,"location"] = variation[1:-1]

#----Create features and labels----#

x = np.zeros([dataset.shape[0], 43])
y = np.zeros([dataset.shape[0]])

AAs = ["A","R","N","D","C","E","Q","G","H","I","L","K","M","F","P","S","T","W","Y","V"]

for i in range(dataset.shape[0]):
	print(dataset.loc[i])
	x[i, AAs.index(dataset.loc[i,"wt"])] = -1
	x[i, AAs.index(dataset.loc[i,"mut"])] = 1
	x[i, 20] = dataset.loc[i,"Temp"]
	x[i, 21] = dataset.loc[i,"pH "]
	x[i, 22] = get_ASA(dataset.loc[i,"PDB"][:4], dataset.loc[i,"location"])
	x[i, 23:] = res_in_range(dataset.loc[i,"PDB"][:4], dataset.loc[i,"location"], residue_range)

	if dataset.loc[i, "ddG"] < 0:
		y[i] = 1
	else:
		pass

np.save("x2.npy", x)
np.save("y2.npy", y)

x = np.load("x2.npy")
y = np.load("y2.npy")

print(x)
print(y)


#----Model----#


model = Sequential()

model.add(Dense(10))
model.add(Activation("relu"))

model.add(Dense(1))
model.add(Activation("sigmoid"))

model.compile(loss="binary_crossentropy",
			optimizer="adam",
			metrics=["accuracy"])

model.fit(x, y, batch_size=32, epochs=50, validation_split=0.1)

predictions = model.predict(x)

for i in range(len(predictions)):
	print(y[i])
	print(predictions[i])
