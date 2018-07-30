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

txt = []
for t in filt_uni:
	txt.append(t.split())

#make word vectors to decide similarity
from gensim.models.word2vec import Word2Vec
model = Word2Vec(txt, size=150, window=5, min_count=1, workers=10)
model.train(txt, total_examples=len(txt), epochs=10)

#create list of word vectors
vector = []
for i in range(len(txt)):
	vec = np.zeros((1,150))
	for word in txt[i]:
		vec = vec + model[word]
	vector.append(vec)

#simple clustering by threshold value
from sklearn.metrics.pairwise import cosine_similarity as sim

comb = list(combinations(np.arange(len(filt_uni)),2))

dic ={}
for i,j in comb:
		if(sim(vector[i].reshape(-1,150), vector[j].reshape(-1,150))>0.7):
			if(filt_uni[i] in dic):
			      dic[filt_uni[j]] = dic[filt_uni[i]]
			else:
			      dic[filt_uni[j]] = filt_uni[i]

nuni = []
for item in filt_uni:
	if(item in dic):
		nuni.append(dic[item])
	else:
		nuni.append(item)

# create 11 intents
'''
new = list([list([filt_uni[0]])])

for i in range(len(filt_uni)):
	vec1 = vectorize(filt_uni[i])
	countj = 0
	for j in range(len(new)):
		for k in range(len(new[j])):
			vec2 = vectorize(new[j][k])
			if(sim(vec1, vec2) > 0.3):
			      new[j].append(filt_uni[i])
			      countj += 1
			      break
		if(countj>0):
			break
	if(countj==0):
		new.append(list([filt_uni[i]]))
#
new = list([list([0])])

for i in range(len(filt_uni)):
	vec1 = vector[i]
	jdex = 0
	counter = 0
	for j in range(len(new)):
	       for k in range(len(new[j])):
		       vec2 = vector[new[j][k]]
		       if(sim(vec1, vec2) > counter):
			       counter = sim(vec1, vec2)
			       jdex = j
	if(counter > 0.5):
	       new[jdex].append(i)
	else:
	       new.append(list([i]))

for i in range(10):
	print("cluster ",i)
	for j in range(len(new[i])):
		print(filt_uni[new[i][j]])
'''

#clustering using k-means on word vectors
from sklearn.cluster import KMeans
new_vec = [vec.reshape(150,) for vec in vector]
kmeans = KMeans(n_clusters=40, random_state=0).fit(new_vec)

for i in range(10):
	print(i)
	lis = np.where(kmeans.labels_ == i)
	lis = list(lis)[0]
	for t in lis:
		print(filt_uni[t])

classes = list([2, 1, 6, 11, 2, 4, 9, 1, 10, 0])
classes.extend([11, 1, 4, 2, 11, 10, 1, 3, 11, 1])
classes.extend([7, 4, 7, 11, 8 ,4, 9, 10, 9, 9])
classes.extend([8, 1, 9, 1, 6, 6, 2, 2, 2, 2])


final = []
for i in range(len(kmeans.labels_)):
	final.append(classes[kmeans.labels_[i]])

ints = list([list([]), list([]), list([]), list([]), list([]), list([]),
             list([]), list([]), list([]), list([]), list([]), list([])])

for i in range(len(filt_ints)):
	for j in filt_ints[i]:
		ints[final[i]].append(j)

themes = list(['Recognition','Relationship with Seniors',
               'Job Satisfaction','Communication','Leadership',
               'Training and Process Orientation','Colleague Relations',
               'Personal Growth', 'Vision Alignment', 'Resources and Benefits',
               'Company Feedback', 'Others'])

for i in range(len(themes)):
	with open("/Users/jessicasethi/Documents/intents/"+str(themes[i])+".txt", "w+") as f:
		for item in ints[i]:
			try:
				f.write("%s\n" % item)
			except:
				print("error")
		f.close()
