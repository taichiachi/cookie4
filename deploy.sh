#!/bin/bash

# Initialize a new Git repository
git init

# Add all files to the repository
git add .

# Commit the changes
git commit -m "Initial commit"

# Add the remote repository URL
git remote add origin https://github.com/taichiachi/cookie4.git

# Push the changes to the remote repository
git push -u origin main
