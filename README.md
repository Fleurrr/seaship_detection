# seaship detection
This project is used for the docking of seaship target detection model, including the seaship target detection model itself and related instructions.<br/>
Created by **Ze Huang**.

## **Usage**
First, make sure you have installed **python 3.7** environment and downloaded this project repository.<br/>
Next, run the following command in the home directory to install the python package needed to use the model:
```
pip install -r requirements.txt
```
Run the following command to achieve image detection，the model will detect the input image until the stop command is received：
```
python detect.py
```
You can also add `--confidence` to set the minimum probability to filter weak detections ; `--threshold_score` to set NMS score's threshold ; `--threshold` to set NMS' s score. 
## Details
### input
Input JPG format image stream to be detected.
### output
For each input image, a JSON format detection result is returned.
For example,If received the following JSON format data:
```
[['speed boat', 70, 245, 157, 305, 0.9955564141273499], ['general cargo ship', 290, 125, 590, 266, 0.9976658225059509], ['speed boat', 466, 258, 537, 310, 0.9768633842468262]]
```
Each item of the JSON data is the detected ship category.<br/>
The first sub-item (for example 'speed boat') means types of ships that detected. The next four sub-items (for example 70, 245, 157, 305) represent the coordinate positions of the upper left corner and the lower right corner of the detection frame.The last term (for example 0.9955564141273499) represents confidence.<br/>
If the ship is not detected or an error occurs, an empty list is returned
### model
|  |  |
|--|--|
|  **model name**|yolov3-tiny  |
|  **classes**|6  |
|  **mean map**|98.41%  |
|  **average IoU**|81.17%  |
|  **fps on CPU**|15-20  |
