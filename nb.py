'''
Rahool Paliwal rpaliwal 110570213
Shahzeb Patel shahpatel 110369918
'''

import math
train_data_unit = []
test_data_unit = []
prior_prob = [0 for i in range(10)]
line_count=0
number_count=0

train_labels = open('traininglabels.txt')

full_train_data = {}

''' read training data and store in dictionary based on actual number '''
with open('trainingimages.txt') as train_data:
    for line in train_data:
        line_count += 1
        line = list(line.strip('\n'))
        for i in range(len(line)):
            if line[i] == ' ':
                line[i] = 0
            elif line[i] == '+':
                line[i] = 1
            elif line[i] == '#':
                line[i] = 1

        '''consider only two features. White space as 0 and others as 1'''

        train_data_unit.append(line)

        if line_count%28 == 0:
            number = int(train_labels.readline().strip('\n'))
            if not full_train_data.has_key(number):
                full_train_data[number] = []
            full_train_data[number].append(train_data_unit)
            train_data_unit = []

'''calculate prior probability for all classifiers'''
for key in full_train_data:
    length = len(full_train_data[key])
    prior_prob[key] = math.log(len(full_train_data[key])/5000.0, 2)

final_data_dict = {}

grid_count = 0

'''calculate total number of times 0s and 1s appear in training data per digit'''
for key, value in full_train_data.items():
    data_dict = {}
    data_dict[0] = [[0 for col in range(28)] for row in range(28)]
    data_dict[1] = [[0 for col in range(28)] for row in range(28)]
    for grid in value:
        grid_count += 1

        for i in range(28):
            for j in range(28):
                if grid[i][j] == 0:
                    data_dict[0][i][j] += 1
                elif grid[i][j] == 1:
                    data_dict[1][i][j] += 1

    if final_data_dict.has_key(key):
        final_data_dict[key].append(data_dict)
    else:
        final_data_dict[key] = data_dict

train_labels.close()
line_count=0

final_answer = [0 for i in range(1000)]

'''predict number based on prior probability and calculated probability of each cell from training data'''
def predict_number(image):
    digit_prob = [0 for i in range(10)]


    for x in range(10):
        probability_0 = 0
        probability_1 = 0
        digit_prob[x] += prior_prob[x]
        for i in range(28):
            for j in range(28):
                if image[i][j] == 0:
                    probability_0 = float(final_data_dict[x][0][i][j])/len(full_train_data[x])
                    if probability_0 == 0:
                        probability_0 = 0.0001 #handle zero count
                    digit_prob[x] = digit_prob[x] + math.log(probability_0,2)
                elif image[i][j] == 1:
                    probability_1 = float(final_data_dict[x][1][i][j])/len(full_train_data[x])
                    if probability_1 == 0:
                        probability_1 = 0.0001 #handle zero count
                    digit_prob[x] = digit_prob[x] + math.log(probability_1,2)

    index = digit_prob.index(max(digit_prob))

    return index

test_labels = open('testlabels.txt')

actual_number_count = [0 for i in range(10)]
predicted_count = [0 for i in range(10)]

'''parse test data and split into 28x28 blocks to feed to predict function'''
with open('testimages.txt') as test_data:
    for line in test_data:
        line_count += 1
        line = list(line.strip('\n'))
        for i in range(len(line)):
            if line[i] == ' ':
                line[i] = 0
            elif line[i] == '+':
                line[i] = 1
            elif line[i] == '#':
                line[i] = 1

        test_data_unit.append(line)

        if line_count%28 == 0:
            actual_number = int(test_labels.readline().strip('\n'))
            actual_number_count[actual_number] = actual_number_count[actual_number] + 1

            digit = predict_number(test_data_unit)
            test_data_unit = []

            predicted_count[digit] = predicted_count[digit] + 1

'''calculate overall accuracy and digitwise accuracy'''
accuracy = [0.0 for x in range(10)]
difference = 0.0
for i in range(10):
    digit_difference = 0.0
    digit_difference = abs(actual_number_count[i]-predicted_count[i])
    difference += digit_difference
    accuracy[i] = float((actual_number_count[i]-digit_difference))/actual_number_count[i]

'''
overall accuracy = (total samples - total errors)/total samples
digitwise accuracy = (total number of times digit occurs - digitwise errors)/total number of times digit occurs
'''

print "Overall Accuracy", float((1000-difference)/1000), "\n"

for i in range(10):
    print "Classifier: ",i, " Accuracy: ", accuracy[i]



