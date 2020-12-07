# seaship detection
This project is used for the docking of seaship target detection model, including the seaship target detection model itself and related instructions.<br/>
Created by **Ze Huang** and **Sloan**.

## **Usage**
First, make sure you have installed **python 3.7** environment and downloaded this project repository.<br/>
Next, run the following command in the home directory to install the python package needed to use the model:
```
pip install -r requirements.txt
```
### Call the model locally 
Run the following command to achieve image detection locally，the model will detect the input image until the stop command is received：
```
python detect.py
```
You can also add `--confidence` to set the minimum probability to filter weak detections ; `--threshold_score` to set NMS score's threshold ; `--threshold` to set NMS' s score. **But we recommend that you should use the default values！**
### Call the model by flask
The server can run the following command In `flask` directory to open the detection port:
```
python flask_sever.py
```
The client receives the detection results by running the following commands:
```
python flask_client.py
```
## Details
### input
Input JPG format image stream to be detected if you call the model locally.<br/>
If you call the model by flask, the image input should be Base64 encoded string type.The ROI input is also a string type and set to format like 'x1, Y1, X2, Y2' if it is required, if not, set it to ' '. 
### output
For each input image, a JSON format detection result is returned.
For example,If received the following JSON format data **while call the model locally**:
```
[['speed boat', 70, 245, 157, 305, 0.9955564141273499], ['general cargo ship', 290, 125, 590, 266, 0.9976658225059509], ['speed boat', 466, 258, 537, 310, 0.9768633842468262]]
```
Each item of the JSON data is the detected ship category.<br/>
The first sub-item (for example 'speed boat') means types of ships that detected. The next four sub-items (for example 70, 245, 157, 305) represent the coordinate positions of the upper left corner and the lower right corner of the detection frame.The last term (for example 0.9955564141273499) represents confidence.<br/>
If the ship is not detected or an error occurs, an empty list is returned.<br/>
Another example，If you recieved the following JSON format data **while call the model by flask**:
```
{'result': [{'class': '6', 'pos': [84, 1, 99, 33], 'score': 0.9993637204170227}, {'class': '2', 'pos': [224, 3, 239, 31], 'score': 0.893089771270752}, {'class': '1', 'pos': [216, 1, 222, 32], 'score': 0.8865072727203369}]}
```
The`class`value refers to the identifier of seaship that identified; the `pos` value represent the coordinate positions of the upper left corner and the lower right corner of the detection frame; the `score` value represents confidence.
### model
| item | value |
|--|--|
|  **model name**|yolov3-tiny  |
|  **classes**|6  |
|  **mean map**|98.41%  |
|  **average IoU**|81.17%  |
|  **fps on CPU**|15-20  |
