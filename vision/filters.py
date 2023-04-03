import pyrealsense2 as rs


# returns realsense's hole filling filter function
def hole_filling():
    hole_filling = rs.hole_filling_filter()

    def filter(frame):
        return hole_filling.process(frame)
    
    return filter