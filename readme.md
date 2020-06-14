# BVH file reading and visualization

<video src="./demo/bvh_read_demo.mp4" width="800px" height="600px" controls="controls"></video>

### Requirment
    python3.x
    PyQt5
    PyOpneGL
    



### Code organization

    ├── README.md             <- Top-level README.
    ├── test_data            <- bvh data path.
    ├── matrix.py            <- matrix operation .
    ├── bone.py            <- bone class.
    ├── bvh.py            <- bvh read.
    ├── motionfeature_bvh.py      <- motion feature, e.g., position.
    ├── read_bvh_view_test.py      <- visualization

### visualization

    python read_bvh_view_test.py 

tips: rotation order(xyz)