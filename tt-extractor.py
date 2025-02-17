"""
TikTok Data Extractor

This script extracts string data from a user-generated TikTok data
file. This script creates text files for detected sections of the
user's TikTok data file.

This tool accepts a .json file. This script should be run in 
the same directory as the .json file.
"""

import json
from datetime import datetime

def extract_data_list(data):
    returnList = []
    #Test for Like section
    if 'link' in dict.keys(data[0]):
        for i in data:
            returnList.append(i['link'])

    #Test for FavoriteVideoList section
    elif 'Link' in dict.keys(data[0]):
        for i in data:
            returnList.append(i['Link'])
    
    return returnList

def write_data_set(dataSet, fileName):
    current_datetime = datetime.now().strftime('%Y-%m-%d_%H%M%S_')
    f = open(current_datetime + fileName + '.txt','w', encoding='utf-8')
    for i in dataSet:
        f.write(i + '\n')
    f.close()
    print('File written:\n\t' + current_datetime + fileName + '.txt\n')

# ****BEGIN MAIN****

if __name__ == '__main__':

    filename = 'user_data_tiktok.json'
    dataDict = {}
    print('\t****TIKTOK DATA EXTRACTOR****\n')
    print('This program will:\n')
    print('\t1.) Check for a user_data_tiktok.json file')
    print('\t2.) Check the file and copy links to saved Favorites and Likes')
    print('\t3.) Write found links to Favorites and Likes text files\n\n')

    print('Notes:')
    print('\t-Please run this program in the same directory as the target .json file.')
    print('\t-The target .json data file is not modified. The file is read and data copied.')
    print('\t-Found items are checked for duplicate links to avoid data duplication.')
    print('\t-For more information and to review the source code, refer to the Github project at:\n ')
    print('\thttps://github.com/philkasper/tt-extractor')

    while True:
        try:
            option = input('Do you agree to continue? (Y/N)\n')
        except:
            print('Please enter a valid response.')
            continue
        if option not in ['Y','N','y','n','Yes','No','YES','NO','yes','no']:
            print('Please enter either Y, N, yes, no, Yes, No, YES, or NO...')
            continue

        if option in ['N','n','No','NO','no']:
            print('Exiting program...')
            break

        if option in ['Y','y','Yes','YES','yes']:
            print('Checking for file: ' + filename + '\n')
            while True:
                try:
                    with open(filename,'r') as f: 
                        print('File "'+ filename + '" found. Processing data...\n')
                        data=json.load(f)
                        if 'Favorite Videos' in dict.keys(data['Activity']):
                            print('Favorites detected...')
                            dataDict['Favorites'] = data['Activity']['Favorite Videos']['FavoriteVideoList']
                        if 'Like List' in dict.keys(data['Activity']):
                            print('Likes detected...')
                            dataDict['Likes'] = data['Activity']['Like List']['ItemFavoriteList']
                        f.close()
                        break
                except FileNotFoundError:
                    print('The file "' + filename + 'was not found.\n')
                    
                    filename = input('Please enter the full filename (type "q" or "quit" to quit):')
                    if filename in ['q', 'Q', 'quit', 'Quit','QUIT']:
                        print('Exiting program...')
                        break
                continue
            
            primeSet = set(extract_data_list(dataDict['Favorites']))
            compSet = set(extract_data_list(dataDict['Likes']))
            print(str(len(primeSet)) + " Favorites found.")
            print(str(len(compSet)) + ' Likes found.')
            print(str(len(primeSet.intersection(compSet))) + ' duplicate links found between Favorites and Likes...\n')
            
            write_data_set(primeSet,'Favorites')
            for key in dataDict.keys():
                if key == 'Favorites':
                    continue
                write_data_set(compSet.difference(primeSet), key)
                #below line for additional data extraction features later
                #primeSet = primeSet.union(compSet)
            print('Extraction of TikTok Favorite and Like links completed!\n')
            print('You may now use these text files with a video-downloading tool,\nsuch as yt-dlp to download your TikTok videos.\n')
            print('To learn more about yt-dlp , please visit their github page:\n\nhttps://github.com/yt-dlp/yt-dlp\n')
            print('Exiting program...')
            break
