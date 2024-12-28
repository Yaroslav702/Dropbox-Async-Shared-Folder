# Dropbox Folder Synchronizer

## Overview

The Dropbox Folder Synchronizer is a Python application that monitors a local folder for changes and synchronizes those changes with a corresponding folder on Dropbox. The application handles file creation, modification, deletion, and renaming. The files are evenly split into multiple threads to speed up the upload process.

## Key Features

- Local Folder Watcher: Monitors a local folder for file changes (create, delete, modify, rename).
- Multi-Threaded File Upload: Files are uploaded in parallel using multiple threads.
- Task Queue: A queue is used to manage tasks (upload, delete) and distribute them to worker threads for processing.
- Asynchronous Requests: Supports sending async requests to Dropbox, improving efficiency and performance.
- Flexible Configuration: Application behavior can be customized by providing parameters in a configuration file `args.json`.

## How to use?

### Prepare dropbox application

1) On https://www.dropbox.com/developers/apps select "Create app";
2) Choose an API, type of the access;
3) Name your application;
4) After the creation, select "Permission" tab and make the following points checked:
![](https://i.imgur.com/0YE2Hez.png)
5) On "Settings" tab press "Generate access token" button;

### Prepare working environment

1) Clone the new repository using git clone command to your local machine:
```
> git clone https://github.com/Yaroslav702/Dropbox-Async-Shared-Folder.git async-dropbox-folder
> cd sync-dropbox-folder
```
2) Install all the required libraries (It is better to prepare venv before the installation):
```
> pip install -r requirements.txt
```
3) Fill the `args.json` file;
4) Run the script
```
> python3 main.py --config 'args.json'
```
