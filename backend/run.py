import os 
 
data = set()
for file, fold, subfold in os.walk(os.getcwd()):
	for f in subfold: 
		if ".py" in f and not "__" in f and not "000" in f:
			data.add(f)
print(data)
print(len(data))
	

