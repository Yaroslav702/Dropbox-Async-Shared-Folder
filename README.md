# Dropbox Folder Synchronizer

## Overview

The Dropbox Folder Synchronizer is a Python application that monitors a local folder for changes and synchronizes those changes with a corresponding folder on Dropbox. The application handles file creation, modification, deletion, and renaming. If there are more than 5 files to upload, the files are evenly split into multiple threads to speed up the upload process. Synchronization with Dropbox is done in a single thread to maintain consistency.

## Key Features

- Local Folder Watcher: Monitors a local folder for file changes (create, delete, modify, rename).
- Multi-Threaded File Upload: If the number of files exceeds 5, they are uploaded in parallel using multiple threads.
- Single-Threaded Dropbox Sync: Synchronization from Dropbox to the local folder is done in a single thread to avoid conflicts.
- Task Queue: A queue is used to manage tasks (upload, delete) and distribute them to worker threads for processing.