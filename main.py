import os
import sys
import cv2
import csv
import numpy as np
import matplotlib.pyplot as plt

def run():

    folder_name = sys.argv[1]
    
    profiles_x = {}
    profiles_y = {}
    
    image_files = [file for file in os.listdir(folder_name) if file.endswith("jpg")]

    for file in image_files:
        
        path = os.path.join(folder_name, file)
        
        img = cv2.imread(path)
        
        profile_x, profile_y = get_mid_profiles(img)
        
        profiles_x[file] = profile_x
        profiles_y[file] = profile_y
    
    profiles_x = use_lambda_as_key(profiles_x)
    profiles_y = use_lambda_as_key(profiles_y)
    
    show_profile_single(profiles_x, "500")
    show_profiles(profiles_x, freq=7)
    show_profiles(profiles_y)
    
    # save_profiles_csv(folder_name, profiles_x, profiles_y)

def use_lambda_as_key(old_dict, sort=True):
    
    new_dict = {}
    
    for old_key in old_dict:
        
        new_key = "".join(filter(lambda x: x.isdigit(), map(str, old_key)))
        
        new_dict.update({new_key: old_dict[old_key]})
        
    if sort:
        
        new_dict = dict(sorted(new_dict.items()))
        
    return new_dict

def save_profiles_csv(folder_name, profiles_x, profiles_y):
    
    x_output_name = os.path.join(folder_name, "x-profiles.csv")
    y_output_name = os.path.join(folder_name, "y-profiles.csv")

    write_data(x_output_name, profiles_x)
    write_data(y_output_name, profiles_y)
    
def write_data(path, data):
    
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
    
        # Write the header row
        writer.writerow(data.keys())
        
        # Write the data rows
        writer.writerows(zip(*data.values()))            

def show_psf(img):

    cv2.imshow("PSF", img)

    cv2.waitKey(0)

def get_mid_profiles(img):

    width = img.shape[0]
    height = img.shape[1]

    mid_line_x = int(round(width/2))
    mid_line_y = int(round(height/2))

    profile_x = img[:, mid_line_x]
    profile_y = img[mid_line_y, :]
    
    profile_x = [x[0] for x in profile_x]
    profile_y = [y[0] for y in profile_y]

    return profile_x, profile_y

def show_profile_single(profiles, key):

    fig, ax = plt.subplots()
 
    plt.plot(profiles[key])

    ax.set_title(key+"nm")
    ax.set_xlabel("Pixels (1deg/512)")
    ax.set_ylabel("Intensity 0-255")
    plt.show()
    
def show_profiles(profiles, freq=None):

    fig, ax = plt.subplots()
    for i, key in enumerate(profiles):
        
        if freq != None:
            if i%freq != 0:
                continue
            
        plt.plot(profiles[key], label=key+"nm")

    legend_without_duplicate_labels(ax)
    ax.set_xlabel("Pixels (1deg/512)")
    ax.set_ylabel("Intensity 0-255")
    plt.show()
    
def legend_without_duplicate_labels(ax):
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
    ax.legend(*zip(*unique))
    
if __name__ == '__main__':
    run()