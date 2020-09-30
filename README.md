# ICRWI - Intelligent Character Recognition Web Interface

This is an automated web interface for handwritten text recognition.



## Citation

Please cite the following if you are using this repository in your work.

```text
Author: Ahmed R. Aldahshoury 
Title: A Web Interface for automated handwriting recognition
Year: 2019
```
## Setup

To setup the system on local device do the following:

1. Download or clone the repo to local device
2. Unzip the **Venv.zip** file
3. Open terminal (make sure you are inside the **BringlsICR** folder)
4. Run the following command to activate the virtual environment which holdes the libraries:
```
source ./venv/bin/activate  # sh, bash, ksh, or zsh\\n
```
5. Navigate to **src** folder using the following command:
```
$ cd src
```
6. **App.py** is the script responsible for running the web application. you can run it using the following command:
```
$ python app.py
```
7. You can modify the hosting port inside that script. By default the web interface is hosted on local host at port 4555. You can open the webpage on any browser using the following link :
```
127.0.0.1:4555
```

Now the system is ready for usage. 

## Customize

If you are interested in customizing the system or modifing its features, please refer to the handbook pdf file for more details about the scripts and their functions. For more details about the concepts, read my thesis paper.




## References

https://github.com/bgshih/crnn


https://github.com/githubharald/CTCWordBeamSearch
