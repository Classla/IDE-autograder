# pylint: disable=all

import requests

# from test_resources.sample_request_bodies import input_output, unit_test
import json

# Define the URL of the FastAPI endpoint
URL = "http://localhost:8000/unit_test/"

input_output = {
    "block_uuid": "6baf28a8-60d0-433a-a64c-1dd9fa1a64f2",
    "test_uuid": "fd1dcbb7-6334-40b5-a29b-a30cdf872aa8",
    "timeout": 30,
    "student_files": {
        "main.py": "def mult(num1, num2):\n    return num1*num2\n\nnum = int(input())\nprint(num*num)"
    },
    "language": "python",
    "autograding_config": {"total_points": 3, "point_calculation": "all_or_nothing"},
    "unit_test_config": {},
    "unit_test_files": {
        "test.py": "\nfrom main import * # import everything from student's main\nimport unittest # import unittest framework\n\nclass Classla_Unit_Test(unittest.TestCase):\n    '''\n    You can add sample tests here, and create multiple functions.\n    Students will see the names of these functions when they fail,\n    so if you would like to make names descriptive to help them you can.\n    '''\n    def test_mult(self):\n        self.assertEquals(mult(4,5) == 20)\n        self.assertEquals(mult(2,3) == 6)\n"
    },
}

input_output = {
    "block_uuid": "bd4a9540-b5b5-4027-badb-cff7d55604aa",
    "test_uuid": "646ed7f5-1b13-482b-add8-5d67f9352241",
    "timeout": 30,
    "student_files": {
        "main.py": 'def mult(num1, num2):\n    return num1*num2\n\nprint("hello!")\nprint(mult(2,2))'
    },
    "language": "python",
    "autograding_config": {"total_points": 1, "point_calculation": "all_or_nothing"},
    "unit_test_config": {},
    "unit_test_files": {
        "test.py": 'from main import * \nimport unittest # import unittest framework\nclass Classla_Unit_Test(unittest.TestCase):\n    def test_if_code(self):\n        f = open("/app/main.py", "r")\n        lines = f.readlines()\n        f.close()\n        self.assertEquals(lines > 5)'
    },
}

input_output = {
    "block_uuid": "aba5fcc4-4c75-401d-a6c0-6a6bf4cb4651",
    "test_uuid": "c99961e0-317e-43b6-950b-2863c27e3183",
    "timeout": 4,
    "student_files": {
        "main.py": "\n\n\n# NO PEEKING :)\n\n\n\n\n\n\n\n\n\n\n\n\n\nfrom pydraw import *\n\n# We are going to use random\nimport random\n\nscreen = Screen(800, 600)\n\n# Initialize some colors and margins to use later\nscreen.red_color = Color(255,0,0)\nscreen.green_color = Color('green')\nscreen.blue_color = Color(0,0,255)\n\nbox_width = screen.width()/3 * 0.8\nbox_height = screen.height()/3 * 0.8\n\n# Create our frames\nleft_frame = Rectangle(screen, 0, 0, screen.width()/3, screen.height()/3, fill=False, border=Color('black'))\nleft_frame.moveto(0, screen.height()/2 - left_frame.height()/2)\nmiddle_frame = Rectangle(screen, 0, 0, screen.width()/3, screen.height()/3, fill=False, border=Color('black'))\nmiddle_frame.moveto(screen.width()/3, screen.height()/2 - middle_frame.height()/2)\nright_frame = Rectangle(screen, 0, 0, screen.width()/3, screen.height()/3, fill=False, border=Color('black'))\nright_frame.moveto(screen.width() * (2/3), screen.height()/2 - right_frame.height()/2)\n\n# Create our boxes\nleft_box = Rectangle(screen, 0, 0, box_width, box_height, Color('white'))\nleft_box.border(Color(0,0,0), 5)\nmiddle_box = Rectangle(screen, 0, 0, box_width, box_height, Color('white'))\nmiddle_box.border(Color('black'), 5)\nright_box = Rectangle(screen, 0, 0, box_width, box_height, Color('white'))\nright_box.border(Color('black'), 5)\n\n# Move our boxes to the correct location\nleft_box.center(left_frame.center())\nmiddle_box.center(middle_frame.center())\nright_box.center(right_frame.center())\n\n# Create our score variables and text to display them\nrules = Text(screen, 'Red = 1 point, Green = 2 points, Blue = 3 points', 0, 0, size=15)\nscore_text = Text(screen, 'Current Score: 0 | Total Score: 0', 0, 0, size = 40)\n\n# Center/align text objects\nrules.moveto(screen.width()/2, 40)\nrules.move(-rules.width()/2, 0)\n\nscore_text.moveto(screen.width()/2, 75)\nscore_text.move(-score_text.width()/2, 0)\n\n# Initialize score variables to 0\nscore_text.current_score = 0\nscore_text.total_score = 0\n\n# When the mouse is clicked ->\ndef mousedown(location, button):\n    # Set current_score to 0\n    score_text.current_score = 0\n\n    # Generate 3 random numbers\n    something = random.randint(1,3)\n    random_2 = random.randint(1,3)\n    random_3 = random.randint(1,3)\n\n    # Change the color of corresponding box depending on random number\n    if something == 1:\n        left_box.color(screen.red_color)\n        score_text.current_score += 1\n    elif something == 2:\n        left_box.color(screen.green_color)\n        score_text.current_score += 2\n    else:\n        left_box.color(screen.blue_color)\n        score_text.current_score += 3\n\n    if random_2 == 1:\n        middle_box.color(screen.red_color)\n        score_text.current_score += 1\n    elif random_2 == 2:\n        middle_box.color(screen.green_color)\n        score_text.current_score += 2\n    else: # random_2 == 3:\n        middle_box.color(screen.blue_color)\n        score_text.current_score += 3\n    \n    if random_3 == 1:\n        right_box.color(screen.red_color)\n        score_text.current_score += 1\n    elif random_3 == 2:\n        right_box.color(screen.green_color)\n        score_text.current_score += 2\n    else: # random_3 == 3:\n        right_box.color(screen.blue_color)\n        score_text.current_score += 3\n\n    # Update scores and text\n    score_text.total_score += score_text.current_score\n    score_text.text(f'Current Score: {score_text.current_score} | Total Score: {score_text.total_score}')\n\n    # Recenter text\n    score_text.moveto(screen.width()/2, 75)\n    score_text.move(-score_text.width()/2, 0)\n\n    # Check if total score is over 50, if it is, reset everything\n    if score_text.total_score > 50:\n        left_box.color(Color('white'))\n        middle_box.color(Color('white'))\n        right_box.color(Color('white'))\n\n        score_text.total_score = 0\n        score_text.current_score = 0\n\n        # Update and recenter text\n        score_text.text(f'Current Score: {score_text.current_score} | Total Score: {score_text.total_score}')\n\n        score_text.moveto(screen.width()/2, 75)\n        score_text.move(-score_text.width()/2, 0)\n\nscreen.listen()\nscreen.stop()"
    },
    "language": "python",
    "autograding_config": {"total_points": 1, "point_calculation": "all_or_nothing"},
    "unit_test_config": {},
    "unit_test_files": {
        "test.py": '\n# import everything from student\'s main\nimport unittest # import unittest framework\n\nclass Classla_Unit_Test(unittest.TestCase):\n    def setUp(self):\n        # Setup code here (if required, replace the \'pass\')\n        with open(\'main.py\', \'r\') as fr:\n            lines = fr.readlines()\n            # Search for line to remove\n            count = 0\n            remove_lines = []\n            for line in lines:\n                count += 1\n                if line.find("screen.stop()") != -1:\n                    remove_lines.append(count)\n            # Opening in writing mode \n            with open(\'main.py\', \'w\') as fw:\n                line_num = 1\n                for line in lines:\n                    # We want to remove line with text we searched for\n                    if line_num not in remove_lines:\n                        fw.write(line)\n                    line_num += 1\n\n    def tearDown(self):\n        # Teardown code here (if required, replace the \'pass\')\n        pass\n\n    def test_default_case(self):\n        # Your test case logic here (replace the example assertion below)\n        global count\n        import main\n        import pydraw\n        import math\n        count =0\n        \n        # Checking location and dimensions of each frame\n        if math.isclose(main.left_frame.location().x(), 0):\n            count += 1\n        if math.isclose(main.left_frame.location().y(), main.screen.height()/2 - main.left_frame.height()/2):\n            count += 1\n\n        if math.isclose(main.middle_frame.location().x(), main.middle_frame.width()):\n            count += 1\n        if math.isclose(main.middle_frame.location().y(), main.screen.height()/2 - main.left_frame.height()/2):\n            count += 1\n\n        if math.isclose(main.right_frame.location().x(), main.middle_frame.width()*2):\n            count += 1\n        if math.isclose(main.middle_frame.location().y(), main.screen.height()/2 - main.left_frame.height()/2):\n            count += 1\n    \n        # Checking color and border of frames\n        if main.left_frame.color().name() == "white" or main.left_frame.fill() == False or main.right_frame.color() == (pydraw.Color(255,255,255)):\n            count += 1\n        if main.middle_frame.color().name() == "white" or main.middle_frame.fill() == False or main.middle_frame.color() == (pydraw.Color(255,255,255)):\n            count += 1\n        if main.right_frame.color().name() == "white" or main.right_frame.fill() == False or main.right_frame.color() == (pydraw.Color(255,255,255)):\n            count += 1\n        if main.left_frame.border().name() == "black" or main.left_frame.border() == pydraw.Color(0,0,0):\n             count += 1\n        if main.middle_frame.border().name() == "black" or main.middle_frame.border() == pydraw.Color(0,0,0):\n             count += 1\n        if main.right_frame.border().name() == "black" or main.right_frame.border() == pydraw.Color(0,0,0):\n             count += 1\n\n        print(count)\n        self.assertTrue(count > 11)\n\n\n'
    },
}

# from main import * # import everything from student's main
# # import unittest # import unittest framework
# class Classla_Unit_Test(unittest.TestCase):
#     def test_if_code(self):
#         f = open(\"main.py\", \"r\")
#         lines = f.readlines()
#         f.close()
#         self.assertEquals(lines > 5)
# # if student wrote more than 1 line of code


# Send a POST request to the FastAPI endpoint
response = requests.post(URL, json=input_output, timeout=10)

# Print the response from the server
print(json.dumps(response.json(), indent=4))
