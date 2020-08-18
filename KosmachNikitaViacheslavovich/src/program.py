
import numpy as np
import cv2 as cv
import math
import warnings

def euclidean_distance2D(x1, y1, x2, y2):
    return math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))

def find_most_remote_points(contour):
    
    contour_number = len(contour)
    distance_matrix = np.zeros([contour_number, contour_number])
    distance_matrix[:] = np.nan 
    for i in range(0, len(contour)):
        x = contour[i][0][0];
        y = contour[i][0][1];
        for j in range(i + 1, len(contour)):
            tempX = contour[j][0][0]
            tempY = contour[j][0][1]
            distance_matrix[i][j] = euclidean_distance2D(x, y, tempX, tempY)
    
    max_distance_position = np.where(distance_matrix == np.nanmax(distance_matrix))
    max_distance_coordinates = list(zip(max_distance_position[0], max_distance_position[1]))
    
    distance_matrix[max_distance_position[0][0], :] = np.nan
    distance_matrix[:, max_distance_position[0][0]] = np.nan
    distance_matrix[max_distance_position[1][0], :] = np.nan
    distance_matrix[:, max_distance_position[1][0]] = np.nan
    
    with warnings.catch_warnings(): 
        warnings.filterwarnings('ignore')
        min_distance_vector = np.nanmin(distance_matrix, 0)
        tolerance = np.nanmean(min_distance_vector);
        if np.isnan(tolerance):
            tolerance = 0;
    
    result = {}
    result["max_distance_coordinates"] = max_distance_coordinates
    result["tolerance"] = tolerance;
    #print(result)
    
    return result

def determine_circle(curve, tolerance):
    
    length_curve = len(curve)
    arc_perimeter = 0;
    point_number = cv.arcLength(curve, False)
    first_point = 0
    half_curve = length_curve // 2
        
    # Determine center of circle and radius
    x1 = curve[first_point][0][0]
    y1 = curve[first_point][0][1]
    x2 = curve[half_curve ][0][0]
    y2 = curve[half_curve ][0][1]
    x3 = curve[-1         ][0][0]
    y3 = curve[-1         ][0][1]
    
    A = x2 - x1
    B = y2 - y1
    C = x3 - x1
    D = y3 - y1
    E = (A * (x1 + x2)) + (B * (y1 + y2))
    F = (C * (x1 + x3)) + (D * (y1 + y3))
    G = 2 * ((A * (y3 - y2)) - (B * (x3 - x2)))
    
    if  G > 0:
        Cx = ((D * E) - (B * F)) / G
        Cy = ((A * F) - (C * E)) / G
        R = math.sqrt(math.pow(x1 - Cx, 2) + math.pow(y1 - Cy, 2))
         
        if tolerance < R / 2:                
            # Create equation of circle 
            circle_equation = lambda x, y: ((math.pow(x - Cx, 2) + math.pow(y - Cy, 2) >= math.pow(R - tolerance, 2)) and 
                                            (math.pow(x - Cx, 2) + math.pow(y - Cy, 2) <= math.pow(R + tolerance, 2)))
            
            # Find the most suitable circle
            continuous_start = 0;
            
            for i in range(0, length_curve):
                if not circle_equation(curve[i][0][0], curve[i][0][1]):
                    if continuous_start != i:
                        temp_perimeter = cv.arcLength(curve[continuous_start : i - 1], False);
                        if (arc_perimeter < temp_perimeter):
                            arc_perimeter = temp_perimeter
                    continuous_start = i + 1;
            
            if continuous_start == 0:
                arc_perimeter = cv.arcLength(curve, False);
            
    return (arc_perimeter / point_number) * 100

def determine_line(curve, tolerance):
    
    length_curve = len(curve)
    valid_perimeter = 0
    point_number = cv.arcLength(curve, False)
    cnt = 0
    continuous_start = 0
    step = np.max([length_curve // 2, 2])
    while (cnt + step < length_curve):
        
        # Determine center of circle and radius
        x1 = curve[cnt    ][0][0]
        y1 = curve[cnt    ][0][1]
        x2 = curve[cnt + step][0][0]
        y2 = curve[cnt + step][0][1]
         
        # Create equation of circle 
        line_equation = lambda x, y: (x + tolerance >= (((y - y1) * (x2 - x1)) / (y2 - y1)) + x1 and 
                                     x - tolerance <= (((y - y1) * (x2 - x1)) / (y2 - y1)) + x1)
        
        # Find the most suitable line
        for i in range(cnt + 1, length_curve):
            if not line_equation(curve[i][0][0], curve[i][0][1]):
                break
        
        arc_perimeter = cv.arcLength(curve[continuous_start : i], False);
        continuous_start = i
        
        if arc_perimeter > valid_perimeter:
            valid_perimeter = arc_perimeter 
        cnt = i + 1;
        
    return (valid_perimeter / point_number) * 100

def run_program(image_name, DEBUG_MODE = False):
    
    GRAY_THRESHOLD = 60
    SAMPLE_THRESHOLD = 15
    TOLERANCE_FACTOR = 2
    
    img = cv.imread(image_name)
    if img is None:
        print(" ".join(['Could not open or find the image', image_name]))
        return None
    
    # Find contours
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, thresh = cv.threshold(gray_img, GRAY_THRESHOLD, 255, 0)
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    # Check contours
    delete_index = [];
    for i in range(len(contours)):
        if len(contours[i]) < SAMPLE_THRESHOLD:
            delete_index.append(i)
            contours[i] = []
    if len(delete_index) == len(contours):
        print("Warning:: Could not determine contours in the image!")
        return None
    with warnings.catch_warnings(): 
        warnings.filterwarnings('ignore')
        if delete_index:
            while [] in contours:
                contours.remove([])
        
    # Find the most remote points in curves
    tolerance_vector = []
    remoute_points = []
    for contour in contours:
        temp = find_most_remote_points(contour)
        remoute_points.append(temp['max_distance_coordinates'])
        tolerance_vector.append(temp['tolerance']) 
        
    # Print found points
    if DEBUG_MODE:
        for i in range(len(remoute_points)):
            cv.circle(img, tuple(contours[i][remoute_points[i][0][0]][0]), 2, (0,0,255), 3)
            cv.circle(img, tuple(contours[i][remoute_points[i][0][1]][0]), 2, (0,0,255), 3)
        
    # Create curves
    curves = [None] * len(contours)
    for i in range(len(contours)):
        start = remoute_points[i][0][0]
        end = remoute_points[i][0][1] + 1
        curves[i] = np.empty((end - start, 1, 2), np.intc)
        cnt = 0
        for j in range(start, end):
            curves[i][cnt] = contours[i][j]
            cnt = cnt + 1                
                
    # Determine percent of circle and lines in curves and decision make
    result_percent = [];
    for i in range(len(curves)):
        circle_percent = determine_circle(curves[i], tolerance_vector[i] * TOLERANCE_FACTOR)
        line_percent = determine_line(curves[i], tolerance_vector[i] * TOLERANCE_FACTOR)
        result_percent.append(circle_percent - line_percent)
    valid_curve_position = result_percent.index(max(result_percent))
    
    result = {"length": cv.arcLength(curves[valid_curve_position], False)};
    print(" ".join(["Result: ", result.__str__(), 'pixels']))
    
    if DEBUG_MODE:
        cv.polylines(img, [curves[valid_curve_position]], False, (255, 0, 0), 2)
        #cv.polylines(img, [curves[5]], False, (255, 0, 0), 2)
        print(" ".join(["Result percent:", result_percent.__str__()]))
        cv.imshow("Result: " + image_name, img)
        cv.waitKey()
        cv.destroyAllWindows()
    
    return result
    
if __name__ == '__main__':
    
    DEBUG_MODE = True
    temp_list = ['image_1.jpg', 'image_2.jpg', 'test_3.png', 'test_4.jpg', 'test_5.jpg', 'test_6.png']
    #temp_list = ['image_1.jpg']
    for element in temp_list:
        run_program(element, DEBUG_MODE)
    
    import timeit
    s = """\
tempList = ['image_1.jpg', 'image_2.jpg', 'test_3.png', 'test_4.jpg', 'test_5.jpg', 'test_6.png']
import program
for element in tempList:
    program.run_program(element, False)
    """
    print(timeit.timeit(stmt=s, number=100))
    
    
    
