import pandas as pd
import numpy as np
import re
import os


class Analyzer:

    def __init__(self, csv_path, csv_type, apk_name):
        custom_header = []
        if csv_type == "drawable":
            custom_header = [
                "apk_name",
                "none",
                "drawable_dir_name",
                "drawable_dir_size",
                "root_tag",
                "shape_type",
                "state",
                "drawable_attr",
            ]
            self.output_path = "./analyzed/drawable"
        elif csv_type == "layout":
            custom_header = [
                "apk_name",
                "none",
                "layout_dir_name",
                "layout_dir_size",
                "root_tag",
                "component_id",
                "component_type",
                "component_text",
            ]
            self.output_path = "./analyzed/layout"
        elif csv_type == "value":
            custom_header = [
                "apk_name",
                "none",
                "value_dir_name",
                "value_dir_size",
                "root_tag",
                "file_type",
                "style_name",
                "attr_name",
                "attr_value",
            ]
            self.output_path = "./analyzed/value"

        self.output(1, {"apk": apk_name}, csv_type)
        self.df = pd.read_csv(csv_path, header=None, names=custom_header)

    def analyze_drawable(self):
        dir_name2size = {}
        root_tag_counter = {}
        shape_type_counter = {}
        state_counter = {}
        for index, row in self.df.iterrows():
            # 1. drawable_dir_size
            dir_name = row["drawable_dir_name"]
            if dir_name not in dir_name2size:
                dir_name2size[dir_name] = row["drawable_dir_size"]
            # 2. root_tag
            root_tag = row["root_tag"]
            if root_tag not in root_tag_counter:
                root_tag_counter[root_tag] = 1
            else:
                root_tag_counter[root_tag] += 1
            # 3. shape_type
            shape_type = row["shape_type"]
            if shape_type not in shape_type_counter:
                shape_type_counter[shape_type] = 1
            else:
                shape_type_counter[shape_type] += 1
            # 4. state
            state = row["state"]
            if state not in state_counter:
                state_counter[state] = 1
            else:
                state_counter[state] += 1
        self.output(2, dir_name2size, "dir_size")
        self.output(2, root_tag_counter, "root_tag")
        self.output(2, shape_type_counter, "shape_type")
        self.output(2, state_counter, "state")

    def output(self, level, _dict, type):
        _dict = dict(sorted(_dict.items(), key=lambda x: str(x[0])))
        prefix = "-" * level + " [" + type + "] "
        with open(self.output_path, "a") as f:
            for key, value in _dict.items():
                f.write(str(prefix) + str(key) + ": " + str(value) + "\n")

    def analyze_layout(self):
        dir_name2size = {}
        root_tag_counter = {}
        component_type_counter = {}
        text_counter = {"nan": 0, "filled": 0}
        for index, row in self.df.iterrows():
            # 1. drawable_dir_size
            dir_name = row["layout_dir_name"]
            if dir_name not in dir_name2size:
                dir_name2size[dir_name] = row["layout_dir_size"]
            # 2. root_tag
            root_tag = self.categorize_android_component_by_keyword(row["root_tag"])
            if root_tag not in root_tag_counter:
                root_tag_counter[root_tag] = 1
            else:
                root_tag_counter[root_tag] += 1
            # 3. component_type_counter
            component_type = self.categorize_android_component_by_keyword(
                row["component_type"]
            )
            if component_type not in component_type_counter:
                component_type_counter[component_type] = 1
            else:
                component_type_counter[component_type] += 1
            # 4. text_counter
            text = row["component_text"]
            if text == "N/A":
                text_counter["nan"] += 1
            else:
                text_counter["filled"] += 1

        self.output(2, dir_name2size, "dir_size")
        self.output(2, root_tag_counter, "root_tag")
        self.output(2, component_type_counter, "component_type")
        self.output(2, text_counter, "text")

    def analyze_value(self):
        dir_name2size = {}
        root_tag_counter = {}
        file_type_counter = {}
        attr_type_counter = {}
        security_counter = {"security": 0}
        SECURITY_KEYWORDS = [
            "password",
            "key",
            "token",
            "secret",
            "api",
            "credentials",
            "auth",
            "login",
            "passcode",
            "access",
            "username",
            "pin",
            "oauth",
            "encryption",
            "decryption",
            "private",
            "public",
            "certificate",
            "ssh",
            "tls",
            "ssl",
            "bearer",
            "authorization",
            "secure",
            "security",
            "sensitive",
            "confidential",
            "risk",
            "malware",
            "vulnerability",
            "exploit",
            "threat",
            "attack",
            "mitigation",
            "data",
            "protection",
            "firewall",
            "intrusion",
            "monitoring",
            "detection",
            "malicious",
            "safeguard",
            "backup",
            "restore",
            "token",
        ]
        for index, row in self.df.iterrows():
            # 1. drawable_dir_size
            dir_name = row["value_dir_name"]
            if dir_name not in dir_name2size:
                dir_name2size[dir_name] = row["value_dir_size"]
            # 2. root_tag
            root_tag = self.categorize_android_component_by_keyword(row["root_tag"])
            if root_tag not in root_tag_counter:
                root_tag_counter[root_tag] = 1
            else:
                root_tag_counter[root_tag] += 1
            # 3. component_type_counter
            file_type = row["file_type"]
            if file_type not in file_type_counter:
                file_type_counter[file_type] = 1
            else:
                file_type_counter[file_type] += 1
            # 4. text_counter
            attr_type = self.categorize_attr_by_keyword(row["attr_name"])
            if attr_type not in attr_type_counter:
                attr_type_counter[attr_type] = 1
            else:
                attr_type_counter[attr_type] += 1
            # 5. security_counter
            attr_name = row["attr_name"]
            atrr_value = row["attr_value"]
            if any(
                keyword in str(attr_name).lower() for keyword in SECURITY_KEYWORDS
            ) or any(
                keyword in str(atrr_value).lower() for keyword in SECURITY_KEYWORDS
            ):
                security_counter["security"] += 1
        self.output(2, dir_name2size, "dir_size")
        self.output(2, root_tag_counter, "root_tag")
        self.output(2, file_type_counter, "file_type")
        self.output(2, attr_type_counter, "attr_type")
        self.output(2, security_counter, "security")

    def categorize_android_component_by_keyword(self, component_type):
        categories = {
            "Layout": r"(Layout|Coordinator|Drawer|Constraint|Frame|Linear|Relative|Table|Grid|CardView|ViewPager|ScrollView|HorizontalScrollView|RecyclerView|ListView|GridView|ExpandableListView)",
            "Text Control": r"(Text|EditText|AutoCompleteTextView|TextInputLayout|TextInputEditText)",
            "Button": r"(Button|ImageButton|FloatingActionButton|ToggleButton|Switch|SwitchCompat|RadioButton|CheckBox|CompoundButton|MaterialButton)",
            "Image View": r"(ImageView|CircleImageView)",
            "Input Control": r"(EditText|SearchView|Spinner|RatingBar|SeekBar)",
            "Picker": r"(DatePicker|TimePicker|CalendarView)",
            "Display Control": r"(ProgressBar|SeekBar|RatingBar|Chronometer|TextClock)",
            "Container": r"(ScrollView|HorizontalScrollView|ViewPager|ViewPager2|RecyclerView|ListView|GridView|ExpandableListView)",
            "Advanced View": r"(RecyclerView|ViewPager|WebView|SurfaceView|GLSurfaceView|TextureView)",
        }

        for category, pattern in categories.items():
            if re.search(pattern, str(component_type), re.IGNORECASE):
                return category

        return "Unknown"

    def categorize_attr_by_keyword(self, attr_name):
        categories = {
            "UI": [
                "color",
                "background",
                "font",
                "text",
                "style",
                "theme",
                "layout",
                "icon",
            ],
            "Action": ["click", "press", "swipe", "tap", "gesture"],
            "Input": ["input", "field", "form", "edit", "type"],
            "Media": ["image", "video", "audio", "media", "sound", "photo"],
            "Network": ["network", "connection", "internet", "wifi", "data"],
            "Storage": ["save", "load", "cache", "file", "storage"],
            "Notification": ["notify", "alert", "message", "notification"],
            "Permission": ["permission", "access", "grant", "deny"],
            "Security": ["security", "encrypt", "decrypt", "auth", "login", "password"],
            "Other": [],  # Miscellaneous for anything not matching above
        }
        for category, keywords in categories.items():
            if any(keyword in str(attr_name).lower() for keyword in keywords):
                return category
        return "Other"


if __name__ == "__main__":
    root_dir = os.getenv("LITEAPPS_ROOT")
    decompiled_dir = os.path.join(root_dir, "static_analyze/decompiled")
    amount = 0
    decompiled_dir_list = []
    for root, dirs, files in os.walk(decompiled_dir):
        for d in dirs:
            amount += 1
            decompiled_dir_list.append(int(d))
        break
    decompiled_dir_list = sorted(decompiled_dir_list)
    cnt = 0
    with open("./analyzed/drawable", "w") as f:
        f.write("")
    with open("./analyzed/layout", "w") as f:
        f.write("")
    with open("./analyzed/value", "w") as f:
        f.write("")

    for _d in decompiled_dir_list:
        d = str(_d)
        print(f"progress: {cnt}/{amount}")
        if not os.path.exists(f"./extracted_drawable/{d}_drawable.csv"):
            continue
        analyzer = Analyzer(
            f"./extracted_drawable/{d}_drawable.csv",
            "drawable",
            f"{d}.apk",
        )
        analyzer.analyze_drawable()
        if not os.path.exists(f"./extracted_layout/{d}_layout.csv"):
            continue
        analyzer = Analyzer(
            f"./extracted_layout/{d}_layout.csv",
            "layout",
            f"{d}.apk",
        )
        analyzer.analyze_layout()
        if not os.path.exists(f"./extracted_value/{d}_value.csv"):
            continue
        analyzer = Analyzer(
            f"./extracted_value/{d}_value.csv",
            "value",
            f"{d}.apk",
        )
        analyzer.analyze_value()
        cnt += 1
