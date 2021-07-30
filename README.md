# Object-Detection-for-Erasers
Object Detection by YOLO-v5
- Update (7.30): add info about project environment 

  ```bash
  cd yolov5
  pip install -r requirements.txt
  ```

  However, it will raise an error when training Yolo:

  `RuntimeError: CUDA error: no kernel image is available for execution on the device`.

  It is because `torch` version does not work on my server (RTX-3090).

  Use `pip install torch==1.7.0+cu110 torchvision==0.8.1+cu110 torchaudio===0.7.0 -f https://download.pytorch.org/whl/torch_stable.html`.

  Solved!

  Reference: https://zhuanlan.zhihu.com/p/312329530

- Update (7.29): add Yolo-v5 model and some strange eraser images
  - Pay attention to `eraser.yaml`, `train.py` and `detect.py` (I made modifications in these three files)
  
- Update (7.28): add all files in this project except Yolo-v5 model