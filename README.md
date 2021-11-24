# HW2
# VRDL-HW2
NCTU Selected Topics in Visual Recognition using Deep Learning Homework 2

## Hardware
The following specs were used to create the original solution.
- Ubuntu 20.04.3 LTS
- Intel(R) Core(TM) i7-8700 CPU @ 3.20GHz
- NVIDIA GeForce RTX 2070

## Preparation Data
https://drive.google.com/drive/folders/1aRWnNvirWHXXXpPPfcWlHQuzGJdXagoc

## Dataset Downloading
After downloading, the data directory is structured as:
```
+- data
  +- train  (32291)
    +- 1.png
    +- 2.png
    ...
  +- test (13068)
    +- 1.png
    +- 2.png
    ...
+- darknet
  ...

# Create the .txt for each image to indicate the class and bbx coordinate based on YOLO's format
python mat_to_yolo.py
There is train.txt  test.txt under the ./data folder, and ./data/train/*.txt  for each train image

# Create valid folder from train data and move *.png and *.txt accordingly
# Create valid.txt file to include the valid *.png file path

+- data
  +- mat_to_yolo.py
  +- train  (32291)
    +- 1.png
    +- 2.png
    ...
    +- digtiStruct.mat
  +- valid (11111)
    +- 1.png
    +- 2.png
  +- test (13068)
    +- 1.png
    +- 2.png
    ...
  +- train.txt
  +- valid.txt
  +- test.txt
  +- VRDL.data
  +- VRDL.names
+- darknet
  +- cfg
  +- backup
  +- MakeFile

  ....

# VRDL.names
0
1
2
...
9

# VRDL.data
classes= 10
train  = ../data/train/train.txt
valid = ../data/train/train.txt
names = ../data/VRDL.names
backup = backup
eval=coco

## Download YOLOv4 from github to ./darknet folder
git clone https://github.com/AlexeyAB/darknet.git

## Modify the make file
./darknet/MakeFile
GPU=1
CUDNN=1

#Modify the config file
./cfg/yolov4.cfg
[net]
batch=16   #org 64
subdivisions=8
# Training
#width=512
#height=512
width=512  # org 608 / 320
height=256  #org 608 /160
channels=3
momentum=0.949
decay=0.0005
angle=10  #org 10
saturation = 1.5
exposure = 1.5
hue=.1

[convolutional]
size=1
stride=1
pad=1
filters=45 #org 255
activation=linear

[yolo]
mask = 6,7,8
anchors = 12, 16, 19, 36, 40, 28, 36, 75, 76, 55, 72, 146, 142, 110, 192, 243, 459, 401
classes=10  #org 80


## coco format 
./darknet/src/detector.c
static int coco_ids[] = { 1,2,3,4,5,6,7,8,9,10,11,13,14,15,16,17,18,19,20,21,22,23,24,25,27,28,31,32,33,34,35,36,37,38,39,40,41,42,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,67,70,72,73,74,75,76,77,78,79,80,81,82,84,85,86,87,88,89,90 }
static int coco_ids[] = { 0,1,2,3,4,5,6,7,8,9}

static void print_cocos(  )
{
     #sprintf(buff, "{\"image_id\":%d, \"category_id\":%d, \"bbox\":[%f, %f, %f, %f], \"score\":%f},\n", image_id, coco_ids[j], bx, by, bw, bh, dets[i].prob[j]);
     sprintf(buff, "{\"image_id\":%d, \"bbox\":[%f, %f, %f, %f], \"score\":%f , \"category_id\":%d},\n", image_id, bx, by, bw, bh, dets[i].prob[j], j);
}



## Weight save under ./backup
./darknet/src/detector.c
#Modify as below
if ((iteration >= (iter_save + 1000) || iteration % 1000 == 0) ||
            (iteration >= (iter_save + 1000) || iteration % 1000 == 0) && net.max_batches < 10000)
        {

Then weight will be saved every 1000 epochs


## Compile darknet under ./darknet
make

## Train the model
./darknet detector train ../data/VRDL.data cfg/yolov4.cfg YOLOv4.conv.137 > *.log

## Loss plot with log
cd ./darknet/scripts/log_parser
python log_parser.py --source-dir ../.. --save-dir ./ --log-file *.log --show true

## mAP calculation and inference Time
# Modify the config file
./cfg/yolov4.cfg
[net]
batch=1
subdivisions=1
# Modify VRDL.data
valid = ./data/valid.txt
# run the scripts under ./darknet folder
./darknet detector map ../data/VRDL.data cfg/yolov4.cfg backup/yolov4_*.weights -points 11 -thresh 0.5 -iou_thresh 0.5
Then result will show as "mean average precision (mAP@0.50) = 0.778463, or 77.85 %"

## Inference time
#choose the best mAP based on mAP calculation result of mAP@0.50

#create result.txt file
./darknet detector test ../data/VRDL.data cfg/yolov4.cfg backup/*.weights -dont_show -ext_output < ../data/test.txt > result.txt
#execute ./data/inference_time.py
python inference_time.py
Then the result will show :
   Inference average time : 10.564775
   Inference Done!

## Generate .json file for test Data
#run script as below
./darknet detector valid ../data/VRDL.data cfg/yolov4.cfg backup/yolov4_last.weights
There will be coco*.json file under ./darknet/results folder
Rename it to answer.json and zip it

