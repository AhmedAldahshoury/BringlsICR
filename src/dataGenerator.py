import os, sys, subprocess

fileName = sys.argv[1]
#print("rotating: " + fileName)

#command1 = subprocess.Popen(['python', 'dataGenerator.py', file, '| tee -a output.txt'])

os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' rot_1  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' rot_2  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' rot_3  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' rot_4  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' rot_5  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' rot_-1  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' rot_-2  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' rot_-3  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' rot_-4  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' rot_-5  | tee -a output.txt ')

#print("bluring: " + fileName)

os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' blur_0.1  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' blur_0.2  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' blur_0.3  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' blur_0.4  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' blur_0.5  | tee -a output.txt ')
#print("translating 1: " + fileName)

os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_1_1  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_2_2  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_1_3  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_2_4  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_1_5  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_2_6  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_1_7  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_2_8  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_1_9  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_2_10  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_1_11  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_2_12  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_1_13  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_2_14  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_1_15  | tee -a output.txt ')
#print("translating 2: " + fileName)

os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_1_1  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_2_1  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_3_1  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_4_2  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_5_1  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_6_2  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_7_1  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_8_2  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_9_1  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_10_2  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_11_1  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_12_2  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_13_1  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_14_2  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_15_1  | tee -a output.txt ')
#print("translating 3: " + fileName)

os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_3_3  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_4_4  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_5_5  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_6_6  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_7_7  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_8_8  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_9_9  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' trans_10_10  | tee -a output.txt ')
#print("adding random noise to: " + fileName)

os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' noise_0.01  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' noise_0.02  | tee -a output.txt ')
#print("zooming: " + fileName)

os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' zoom_-3_-3_-3_-3  | tee -a output.txt ')
os.system('python -W ignore augmentation.py ../dataset/segmented/' + fileName + ' zoom_-5_-5_-5_-5  | tee -a output.txt ')
print("augmented folder (" + fileName + ") successfully")
print("--------")