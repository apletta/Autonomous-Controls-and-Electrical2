####################################################################################
# ZEDStereoCam: Package for connecting to a ZED stereo camera
#
# Simplifies official ZED python wrapper for retrieving image and depth data from camera



####################################################################################

import pyzed.sl as sl
import numpy as np


class ZED:

    zed = None

    left_image_zed = sl.Mat()
    right_image_zed = sl.Mat()
    depth_image_zed = sl.Mat()
    depth_data_zed = sl.Mat()


    runtime = sl.RuntimeParameters()

    resolution = sl.RESOLUTION.RESOLUTION_HD720 # Default
    fps = 30 # Default
    depthMode = sl.DEPTH_MODE.DEPTH_MODE_PERFORMANCE # Default
    fillMode = sl.SENSING_MODE.SENSING_MODE_STANDARD # Default


    def __init__(self, res='720p', quality=0, fill=False):

        self.zed = sl.Camera()
        init = sl.InitParameters()

        if res == '1080p':
            self.resolution = sl.RESOLUTION.RESOLUTION_HD1080
            self.fps = 30

        elif res == '720p':
            self.resolution = sl.RESOLUTION.RESOLUTION_HD720
            self.fps = 60

        elif res == 'VGA':
            self.resolution = sl.RESOLUTION.RESOLUTION_VGA
            self.fps = 100

        else:
            print('RESOLUTION NOT SUPPORTED: DEFAULTING TO (HD720)')



        if quality == 0:
            self.depthMode = sl.DEPTH_MODE.DEPTH_MODE_PERFORMANCE

        elif quality == 1:
            self.depthMode = sl.DEPTH_MODE.DEPTH_MODE_MEDIUM

        elif quality == 2:
            self.depthMode = sl.DEPTH_MODE.DEPTH_MODE_QUALITY

        elif quality == 3:
            self.depthMode = sl.DEPTH_MODE.DEPTH_MODE_ULTRA

        else:
            print('DEPTH MODE NOT SUPPORTED: DEFAULTING TO (PERFORMANCE)')



        if fill is False:
            self.fillMode = sl.SENSING_MODE.SENSING_MODE_STANDARD

        elif fill is True:
            self.fillMode = sl.SENSING_MODE.SENSING_MODE_FILL

        else:

            print('FILL MODE NOT SUPPORTED: DEFAULTING TO (NO FILL)')


        init.camera_resolution = sl.RESOLUTION.RESOLUTION_HD720
        init.depth_mode = sl.DEPTH_MODE.DEPTH_MODE_PERFORMANCE
        init.coordinate_units = sl.UNIT.UNIT_METER
        init.camera_fps = 100

        if self.zed.open(init) != sl.ERROR_CODE.SUCCESS:
            print('ZED NOT FOUND')
            #print(repr(err))
            self.zed.close()
            exit(1)

        else:
            print('ZED CONNECTED')


        self.zed_info = zed.get_camera_information().calibration_parameters
        # Set ZED's runtime parameters to default and depth fill mode
        self.runtime.sensing_mode = self.fillMode
        #self.read_lock = threading.Lock()
        #self.start()
    
    def start(self):

        updateThread = threading.Thread(target=self.update)
        updateThread.start()

    # Main thread to continuously retrieve latest images/data from ZED
    # Not used, causes main thread to hang
    def update(self):
        #print('working')
        #while self.zed.grab(self.runtime) == sl.ERROR_CODE.SUCCESS:
	    #with self.read_lock:

	        #print('also working')
                err = self.zed.grab(self.runtime)
                if err == sl.ERROR_CODE.SUCCESS:
                    self.zed.retrieve_image(self.left_image_zed, sl.VIEW.VIEW_LEFT)
                    self.zed.retrieve_image(self.right_image_zed, sl.VIEW.VIEW_RIGHT)
                    self.zed.retrieve_image(self.depth_image_zed, sl.VIEW.VIEW_DEPTH)
                    self.zed.retrieve_measure(self.depth_data_zed, sl.MEASURE.MEASURE_DEPTH)


    # Returns image from ZED's left camera
    def getLeftImage(self):
        if self.zed.grab(self.runtime) == sl.ERROR_CODE.SUCCESS:
            self.zed.retrieve_image(self.left_image_zed, sl.VIEW.VIEW_LEFT)
        return self.left_image_zed.get_data()


    # Returns image from ZED's right camera
    def getRightImage(self):
        if self.zed.grab(self.runtime) == sl.ERROR_CODE.SUCCESS:
            self.zed.retrieve_image(self.right_image_zed, sl.VIEW.VIEW_RIGHT)
        return self.right_image_zed.get_data()


    # Returns depth disparity image from ZED
    def getDepthImage(self):
        if self.zed.grab(self.runtime) == sl.ERROR_CODE.SUCCESS:
            self.zed.retrieve_image(self.depth_image_zed, sl.VIEW.VIEW_DEPTH)
        return self.depth_image_zed.get_data()


    # Returns raw depth point cloud map generated by ZED
    def getDepthMap(self):
        if self.zed.grab(self.runtime) == sl.ERROR_CODE.SUCCESS:
            self.zed.retrieve_measure(self.depth_data_zed, sl.MEASURE.MEASURE_DEPTH)
        return self.depth_data_zed.get_data()


    # Returns distance in meters of specified pixel (x,y) in image
    def getDepth(self,x,y):
        if self.zed.grab(self.runtime) == sl.ERROR_CODE.SUCCESS:
            self.zed.retrieve_measure(self.depth_data_zed, sl.MEASURE.MEASURE_DEPTH)
        # Y and X axis are switched for ZED's point cloud data
        return self.depth_data_zed.get_value(y,x)

    # Returns the horizontal field of view (FOV) in degrees of one of ZED's sensors
    def getFOV(self):
        return self.zed_info.left_cam.h_fox

    def getFocalLength(self):
        return self.zed_info.left_cam.fx

    def getWidth(self):
        return zed.get_resolution().width

    def getHeight(self):
        return zed.get_resolution().height
