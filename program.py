from padatious.intent_container import IntentContainer
import pickle

with open("/Users/jessicasethi/Documents/themes", "rb") as f:
    uni = pickle.load(f)


#uni = list(["goodbye", "greeting", "questions"])
container = IntentContainer('intent_cache')

for item in uni:
    file = open("/Users/jessicasethi/Documents/intent_full/" + str(item) + ".txt", "r")
    container.load_file(item, "/Users/jessicasethi/Documents/intent_full/" + str(item) + ".txt")
    file.close()

#container.add_intent('goodbye', ['See you!', 'Goodbye!'])

container.train()

with open("/Users/jessicasethi/Documents/tests", "rb") as fil:
    test_ints = pickle.load(fil)

total = len(test_ints)
correct = 0
'''
for i in range(total):
    data = container.calc_intent(test_ints[i])
    if(data.name == uni[i]):
        correct += 1
    
print(container.calc_intent('leadership obvious in the organization.'))
print(container.calc_intent("Training makes for good development"))
print(container.calc_intent("Company's trust on Human resources. Even in critical times company never though to get rid of employees to cut-off the costs. Employees also work with truthfulness and completed many projects under toughest conditions without losing hope."))
print(container.calc_intent("The HR department is lacking"))

'''
data = container.calc_intent(test_ints[0])
print(data.name)
print(uni[0])
