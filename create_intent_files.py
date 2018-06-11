file = "/Users/jessicasethi/Documents/Theming_Raw_Data.xlsx"
df1 = pd.read_excel(file)
df1 = df1.values
df2 = pd.read_excel(file, sheet_name = 1)
df2 = df2.values
#similarly for df3 and 4


them = np.concatenate((df1[:,1], df1[:,3]), axis = 0)
them = np.concatenate((them, df1[:,5]), axis = 0)

vals = np.concatenate((df1[:,0], df1[:,2]), axis = 0)
vals = np.concatenate((vals, df1[:,4]), axis = 0)
#add rest of the data

#remove "Na" etc as well
indices = np.where(them=="N.A.")
them = np.delete(them, indices)
vals = np.delete(vals, indices)

#remove nans
indices = np.where(them!=them)
them = np.delete(them, indices)
vals = np.delete(vals, indices)

#remove empty themes
indices = np.where(them==' ')
them = np.delete(them, indices)
vals = np.delete(vals, indices)

nan_indices=[]
for i in range(len(them)):
	if(isinstance(them[i], str)==False):
		nan_indices.append(i)
them = np.delete(them, nan_indices)
vals = np.delete(vals, nan_indices)

them = list(them)

#do these changes on df1
them = [(line.split('-', 1)[0]).split(',',1)[0] for line in them]
them = [re.sub(r'[^\w\s]','',x) for x in them]
them = [x.strip().lower() for x in them]
them = np.array(them)
#do these changes on df1

uni = set(them)
uni = list(uni)

intents = []
for sent in uni:
	coli = list(vals[them==sent])
	intents.append(coli)

'''
for sent in uni:
	coli = []
	coli = coli + list(df1[df1[:,1]==sent,0])
	coli = coli + list(df1[df1[:,3]==sent,2])
	coli = coli + list(df1[df1[:,5]==sent,4])
	intents.append(coli)
'''


filt_uni = []
filt_ints = []
for i in range(len(intents)):
	if(len(intents[i]) > 2):
		filt_uni.append(uni[i])
		filt_ints.append(intents[i])
		
del filt_uni[0]
del filt_ints[0]

#create intent files for program

train_ints = []
test_ints = []

for i in range(len(filt_ints)):
	test_ints.append((filt_ints[i])[0])
	train_ints.append((filt_ints[i])[1:len(filt_ints[i])])


for i in range(len(filt_uni)):
	with open("/Users/jessicasethi/Documents/intent_full/"+str(filt_uni[i])+".txt", "w+") as f:
		for item in train_ints[i]:
			try:
				f.write("%s\n" % item)
			except:
				print("error")
		f.close()

with open("/Users/jessicasethi/Documents/themes", "wb") as f:
	pickle.dump(filt_uni, f)

with open("/Users/jessicasethi/Documents/tests", "wb") as f:
	pickle.dump(test_ints, f)

'''
for i in range(len(uni)):
	with open("/Users/jessicasethi/Documents/intent_full/"+str(uni[i])+".txt", "w+") as f:
		for item in intents[i]:
			f.write("%s\n" % item)
		f.close()

#create the file with intent names
with open("/Users/jessicasethi/Documents/clean_themes", "wb") as f:
	pickle.dump(uni, f)

# find themes used more than once (in first sheet)
freq_intents = []
for revs in intents:
	if(len(revs)>1):
		freq_intents.append(revs)

frq_uni = [uni[i] for i in frq_index]
'''
