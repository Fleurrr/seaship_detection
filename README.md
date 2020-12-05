# seaship detection
This project is used for the docking of seaship target detection model, including the seaship target detection model itself and related instructions.
Created by **Ze Huang**.

## **Usage**
First, make sure you have installed **python 3.7** environment and downloaded this project repository.
Next, run the following instructions in the home directory to install the python package needed to use the model:
```
pip install -r requirements.txt
```
Run the following command to achieve image detection：
```
python detect.py --<file path>
```
## Details
### input
Input JPG format image stream to be detected.
### output
For each input image, a JSON format detection result is returned.
For example,If received the following JSON format data:
```
[['speed boat', 70, 245, 157, 305, 0.9955564141273499], ['general cargo ship', 290, 125, 590, 266, 0.9976658225059509], ['speed boat', 466, 258, 537, 310, 0.9768633842468262]]
```
Each item of the JSON data is the detected ship category.
The first sub-item (for example 'speed boat') means types of ships that detected. The next four sub-items (for example 70, 245, 157, 305) represent the coordinate positions of the upper left corner and the lower right corner of the detection frame.The last term (for example 0.9955564141273499) represents confidence.
If the ship is not detected or an error occurs, an empty list is returned
### model
