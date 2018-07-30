from padatious.intent_container import IntentContainer
import pickle

container = IntentContainer('intent_cache')

themes = list(['Recognition','Relationship with Seniors',
               'Job Satisfaction','Communication','Leadership',
               'Training and Process Orientation','Colleague Relations',
               'Personal Growth', 'Vision Alignment', 'Resources and Benefits',
               'Company Feedback', 'Others'])


for item in themes:
    file = open("/Users/jessicasethi/Documents/intents/" + str(item) + ".txt", "r")
    container.load_file(item, "/Users/jessicasethi/Documents/intents/" + str(item) + ".txt")
    file.close()

container.train()

with open("/Users/jessicasethi/Documents/testing", "rb") as f:
    tests = pickle.load(f)
'''
total = len(tests)
count = 0

for item in tests:
    data = container.calc_intent(item[0])
    if(data.name == item[1]):
        count += 1
    else:
        print(data.sent)
        print(data.conf)
        print(item[1])
        print(data.name)
print(count, " out of ", total)
'''
total = len(tests)
count = 0

for item in tests:
    datal = container.calc_intents(item[0])
    if(any(x .name== item[1] for x in datal)):
        count += 1
    print(item[0])
    sor = sorted(datal, key = lambda x: x.conf, reverse = True)
    for lem in sor:
        if(lem.conf > 0):
            print(lem.conf,"\t", lem.name)
        else:
            break

print(count, " out of ", total)

'''
l = container.calc_intents('regular training programs are effective in improvement')
for item in l:
    if(item.conf > 0):
        print(item.name, item.conf)
'''
