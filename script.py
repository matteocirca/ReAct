# Read two .txt files and keep rows of the type:
# {'steps': 3, 'answer': 'yes', 'gt_answer': 'yes', 'question_idx': 6832, 'reward': True, 'em': True, 'f1': 1.0}
# Compare the rewards and print the number of correct answers and the number of improvements

import re
import sys


filename1_rewards = [] # filename1 is answers from react
filename2_rewards = [] # filename2 is answers from reactsr

# fail if wrong number of arguments
if len(sys.argv) != 3:
    print("Error: wrong number of arguments")
    print("Usage: python3 script.py <react_ansers> <reactsr_answers>")
    exit(1)

# read file
folder = 'trajs/'
filename1 = folder + sys.argv[1]
file = open(filename1, 'r')
lines1 = file.readlines()
file.close()

# find rewards
for line in lines1:
    if "{'steps'" in line:
        reward = re.search(r"'reward': (\w+)", line)
        if reward:
            filename1_rewards.append(reward.group(1))

# read file
filename2 = folder + sys.argv[2]
file = open(filename2, 'r')
lines2 = file.readlines()
file.close()

# find rewards
for line in lines2:
    if "{'steps'" in line:
        reward = re.search(r"'reward': (\w+)", line)
        if reward:
            filename2_rewards.append(reward.group(1))


react_rewards = filename1_rewards.copy()
reactsr_rewards = filename2_rewards.copy()

# convert to boolean
react_rewards = [True if x == 'True' else False for x in react_rewards]
reactsr_rewards = [True if x == 'True' else False for x in reactsr_rewards]

# print("react rewards: ", repr(react_rewards))
# print("reactsr rewards: ", repr(reactsr_rewards))

if len(react_rewards) != len(reactsr_rewards):
    print("Error: different number of rewards")
    print("react rewards len: ", len(react_rewards))
    print("reactsr rewards len: ", len(reactsr_rewards))
    exit(1)

print("react rewards len: ", len(react_rewards))
print("reactsr rewards len: ", len(reactsr_rewards))

tot_correct_answers = 0
tot_improvements_react = 0
tot_improvements_reactsr = 0

# compare rewards
for i in range(len(react_rewards)):
    if react_rewards[i] or reactsr_rewards[i]:
        tot_correct_answers += 1
        if react_rewards[i] == True and reactsr_rewards[i] == False:
            tot_improvements_react += 1
        if react_rewards[i] == False and reactsr_rewards[i] == True:
            tot_improvements_reactsr += 1

print("Total correct answers: " + str(tot_correct_answers))
print("Total improvements react: " + str(tot_improvements_react))
print("Total improvements reactsr: " + str(tot_improvements_reactsr))
