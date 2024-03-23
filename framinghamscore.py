class FraminghamScore:
    def __init__(self):
        self.age_points_male = {
            (30, 34): -9, (35, 39): -4, (40, 44): 0, (45, 49): 3,
            (50, 54): 6, (55, 59): 7, (60, 64): 8, (65, 69): 8, (70, 74): 8
        }

        self.age_points_female = {
            (30, 34): -1, (35, 39): 0, (40, 44): 1, (45, 49): 2,
            (50, 54): 3, (55, 59): 4, (60, 64): 5, (65, 69): 6, (70, 74): 7
        }

        self.cholesterol_points_male = {
            (0, 159): -1, (160, 199): 0, (200, 239): 1, (240, 279): 1, (280, float('inf')): 3
        }

        self.cholesterol_points_female = {
            (0, 159): -3, (160, 199): 0, (200, 239): 1, (240, 279): 2, (280, float('inf')): 3
        }

        self.hdl_points_male = {
            (0, 34): 5, (35, 44): 2, (45, 49): 1, (50, 59): 0, (60, float('inf')): -3
        }

        self.hdl_points_female = {
            (0, 34): 2, (35, 44): 1, (45, 49): 0, (50, 59): 0, (60, float('inf')): -1
        }

        self.systolic_bp_points_male = {
            "optimal": -4, "normal": 0, "high normal": 1, "stage I hypertension": 2, "stage II hypertension": 3
        }

        self.systolic_bp_points_female = {
            "optimal": 0, "normal": 0, "high normal": 1, "stage I hypertension": 2, "stage II hypertension": 3
        }

    def get_cholesterol_points(self, age, cholesterol, gender):
        if gender == "M":
            cholesterol_points = self.cholesterol_points_male
        else:
            cholesterol_points = self.cholesterol_points_female

        for age_range, points in cholesterol_points.items():
            if age_range[0] <= cholesterol <= age_range[1]:
                return points
        return 0

    def calculate_framingham_score(self, age, total_cholesterol, hdl, blood_pressure, diabetic, smoker, gender):
        if gender == "M":
            age_points = self.age_points_male
            hdl_points = self.hdl_points_male
            systolic_bp_points = self.systolic_bp_points_male
        else:
            age_points = self.age_points_female
            hdl_points = self.hdl_points_female
            systolic_bp_points = self.systolic_bp_points_female

        age_pt = next((points for age_range, points in age_points.items() if age_range[0] <= age <= age_range[1]), 0)
        chol_pt = self.get_cholesterol_points(age, total_cholesterol, gender)
        hdl_pt = next((points for hdl_range, points in hdl_points.items() if hdl_range[0] <= hdl <= hdl_range[1]), 0)
        sys_bp_pt = systolic_bp_points.get(blood_pressure, 0)
        diabetes_pt = 4 if diabetic else 0
        smoker_pt = 2 if smoker else 0

        total_points = age_pt + chol_pt + hdl_pt + sys_bp_pt + diabetes_pt + smoker_pt

        return total_points
