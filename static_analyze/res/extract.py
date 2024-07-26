from xml.etree import ElementTree as ET


import os


class ResAnalyze:

    def __init__(self, res_path, apk_name, coarse_grained=True):
        self.res_path = res_path
        self.coarse_grained = coarse_grained
        self.apk_name = apk_name
        self.component_counts = {}
        self.drawable_counts = {
            "shape": 0,
            "selector": 0,
            "layer-list": 0,
            "other_xml": 0,
            "non_xml": 0,
        }
        self.file_counts = {
            "strings.xml": 0,
            "colors.xml": 0,
            "dimens.xml": 0,
            "styles.xml": 0,
            "arrays.xml": 0,
            "other": 0,
        }

    def list_files_in_dir(self, directory):
        """List all files in a directory."""
        return [
            os.path.join(directory, file)
            for file in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, file))
        ]

    def write2csv_layout(self, record_type, record_str):
        if record_type == "layout":
            csv_path = "./extracted_layout/" + self.apk_name + "_layout.csv"
        elif record_type == "drawable":
            csv_path = "./extracted_drawable/" + self.apk_name + "_drawable.csv"
        elif record_type == "value":
            csv_path = "./extracted_value/" + self.apk_name + "_value.csv"
        else:
            reutrn
        with open(csv_path, "a") as f:
            f.write(record_str + "\n")

    def analyze_layout_files(self, layout_dir):
        """Analyze layout XML files."""
        layout_files = self.list_files_in_dir(layout_dir)
        layout_files = sorted(layout_files, key=lambda x: os.path.basename(x))
        layout_dir_name = os.path.basename(layout_dir)
        layout_dir_size = sum(
            os.path.getsize(layout_file) for layout_file in layout_files
        )
        for layout_file in layout_files:
            try:
                tree = ET.parse(layout_file)
                root = tree.getroot()

                if self.coarse_grained:
                    for elem in root.iter():
                        if elem is not root:
                            component_type = elem.tag
                            component_type = component_type.split(".")[-1]
                            if component_type in self.component_counts:
                                self.component_counts[component_type] += 1
                            else:
                                self.component_counts[component_type] = 1
                else:
                    root_tag = root.tag
                    for elem in root.iter():
                        if elem is not root:
                            component_type = elem.tag
                            component_id = elem.attrib.get(
                                "{http://schemas.android.com/apk/res/android}id", "N/A"
                            )
                            component_text = elem.attrib.get(
                                "{http://schemas.android.com/apk/res/android}text",
                                "N/A",
                            )
                            self.write2csv_layout(
                                "layout",
                                f"{self.apk_name.replace(',','-')},layout,{layout_dir_name.replace(',','-')},{str(layout_dir_size).replace(',','-')},{root_tag.replace(',','-')},{component_id.replace(',','-')},{component_type.replace(',','-')},{component_text.replace(',','-')}",
                            )
            except ET.ParseError as e:
                print(f"Error parsing {layout_file}: {e}")

    def analyze_drawable_files(self, drawable_dir):
        """Analyze drawable files."""
        drawable_files = self.list_files_in_dir(drawable_dir)
        drawable_dir_name = os.path.basename(drawable_dir)
        drawable_dir_size = sum(
            os.path.getsize(drawable_file) for drawable_file in drawable_files
        )

        if self.coarse_grained:
            for drawable_file in drawable_files:
                file_name = os.path.basename(drawable_file)

                if file_name.endswith(".xml"):
                    try:
                        tree = ET.parse(drawable_file)
                        root = tree.getroot()

                        if root.tag == "shape":
                            self.drawable_counts["shape"] += 1
                        elif root.tag == "selector":
                            self.drawable_counts["selector"] += 1
                        elif root.tag == "layer-list":
                            self.drawable_counts["layer-list"] += 1
                        else:
                            self.drawable_counts["other_xml"] += 1

                    except ET.ParseError as e:
                        print(f"Error parsing {drawable_file}: {e}")
                else:
                    self.drawable_counts["non_xml"] += 1

        else:
            for drawable_file in drawable_files:
                file_name = os.path.basename(drawable_file)
                file_size = os.path.getsize(drawable_file)

                # print(f"Drawable file: {file_name}")
                # print(f"File size: {file_size} bytes")

                if file_name.endswith(".xml"):
                    try:
                        tree = ET.parse(drawable_file)
                        root = tree.getroot()
                        root_tag = root.tag
                        # Extracting information based on root tag type
                        if root.tag == "shape":
                            shape_type = root.attrib.get(
                                "{http://schemas.android.com/apk/res/android}shape",
                                "N/A",
                            )
                            self.write2csv_layout(
                                "drawable",
                                f"{apk_name.replace(',','-')},drawable,{drawable_dir_name.replace(',','-')},{str(drawable_dir_size).replace(',','-')},{root_tag.replace(',','-')},{shape_type.replace(',','-')},N/A,N/A",
                            )
                        elif root.tag == "selector":
                            for item in root.findall("item"):
                                # fouced, pressed, selected, enabled, window_focused
                                state = "N/A"
                                if (
                                    item.attrib.get(
                                        "{http://schemas.android.com/apk/res/android}state_fouced"
                                    )
                                    == "true"
                                    or item.attrib.get(
                                        "{http://schemas.android.com/apk/res/android}state_pressed"
                                    )
                                    == "true"
                                    or item.attrib.get(
                                        "{http://schemas.android.com/apk/res/android}state_selected"
                                    )
                                    == "true"
                                    or item.attrib.get(
                                        "{http://schemas.android.com/apk/res/android}state_enabled"
                                    )
                                    == "true"
                                    or item.attrib.get(
                                        "{http://schemas.android.com/apk/res/android}state_window_focused"
                                    )
                                    == "true"
                                ):
                                    state = "true"
                                drawable = item.attrib.get(
                                    "{http://schemas.android.com/apk/res/android}drawable",
                                    "N/A",
                                )
                                self.write2csv_layout(
                                    "drawable",
                                    f"{apk_name.replace(',','-')},drawable,{drawable_dir_name.replace(',','-')},{str(drawable_dir_size).replace(',','-')},{root_tag.replace(',','-')},N/A,{state.replace(',','-')},{drawable.replace(',','-')}",
                                )

                        elif root.tag == "layer-list":
                            for item in root.findall("item"):
                                drawable = item.attrib.get(
                                    "{http://schemas.android.com/apk/res/android}drawable",
                                    "N/A",
                                )
                                self.write2csv_layout(
                                    "drawable",
                                    f"{apk_name.replace(',','-')},drawable,{drawable_dir_name.replace(',','-')},{str(drawable_dir_size).replace(',','-')},{root_tag.replace(',','-')},N/A,N/A,{drawable.replace(',','-')}",
                                )
                        else:
                            self.write2csv_layout(
                                "drawable",
                                f"{apk_name.replace(',','-')},drawable,{drawable_dir_name.replace(',','-')},{str(drawable_dir_size).replace(',','-')},other,N/A,N/A,N/A",
                            )
                    except ET.ParseError as e:
                        print(f"Error parsing {drawable_file}: {e}")
                # else:
                # print("Non-XML drawable file")

    def analyze_values_files(self, values_dir):
        """Analyze values XML files."""
        values_files = self.list_files_in_dir(values_dir)
        values_dir_name = os.path.basename(values_dir)
        values_dir_size = sum(
            os.path.getsize(values_file) for values_file in values_files
        )

        for values_file in values_files:
            file_name = os.path.basename(values_file)
            file_size = os.path.getsize(values_file)

            if self.coarse_grained:
                # Coarse-grained analysis
                # print(f"File: {file_name}, Size: {file_size} bytes")
                if file_name in self.file_counts:
                    self.file_counts[file_name] += 1
                else:
                    self.file_counts["other"] += 1
            else:
                # print(f"Analyzing values file: {file_name}")
                try:
                    tree = ET.parse(values_file)
                    root = tree.getroot()
                    root_tag = root.tag
                    if file_name == "strings.xml":
                        self.file_counts["strings.xml"] += 1
                        for string in root.findall("string"):
                            name = string.attrib.get("name", "N/A")
                            value = string.text
                            self.write2csv_layout(
                                "value",
                                f"{apk_name.replace(',','-')},value,{values_dir_name.replace(',','-')},{str(values_dir_size).replace(',','-')},{root_tag.replace(',','-')},string,N/A,{name.replace(',','-')},{str(value).replace(',','-')}",
                            )
                    elif file_name == "colors.xml":
                        self.file_counts["colors.xml"] += 1
                        for color in root.findall("color"):
                            name = color.attrib.get("name", "N/A")
                            value = color.text
                            self.write2csv_layout(
                                "value",
                                f"{apk_name.replace(',','-')},value,{values_dir_name.replace(',','-')},{str(values_dir_size).replace(',','-')},{root_tag},colors,N/A,{name.replace(',','-')},{str(value).replace(',','-')}",
                            )
                    elif file_name == "dimens.xml":
                        self.file_counts["dimens.xml"] += 1
                        for dimen in root.findall("dimen"):
                            name = dimen.attrib.get("name", "N/A")
                            value = dimen.text
                            self.write2csv_layout(
                                "value",
                                f"{apk_name.replace(',','-')},value,{values_dir_name.replace(',','-')},{str(values_dir_size).replace(',','-')},{root_tag},dimens,N/A,{name.replace(',','-')},{str(value).replace(',','-')}",
                            )
                    elif file_name == "styles.xml":
                        self.file_counts["styles.xml"] += 1
                        for style in root.findall("style"):
                            style_name = style.attrib.get("name", "N/A")
                            for item in style.findall("item"):
                                property_name = item.attrib.get("name", "N/A")
                                value = item.text
                                self.write2csv_layout(
                                    "value",
                                    f"{apk_name.replace(',','-')},value,{values_dir_name.replace(',','-')},{str(values_dir_size).replace(',','-')},{root_tag.replace(',','-')},styles,{style_name.replace(',','-')},{property_name.replace(',','-')},{str(value).replace(',','-')}",
                                )
                    elif file_name == "arrays.xml":
                        self.file_counts["arrays.xml"] += 1
                        for array in root.findall("string-array"):
                            name = array.attrib.get("name", "N/A")
                            for item in array.findall("item"):
                                value = item.text
                                self.write2csv_layout(
                                    "value",
                                    f"{apk_name.replace(',','-')},value,{values_dir_name.replace(',','-')},{str(values_dir_size).replace(',','-')},{root_tag},arrays,N/A,{name.replace(',','-')},{str(value).replace(',','-')}",
                                )
                    else:
                        self.file_counts["other"] += 1
                        for child in root:
                            name = child.attrib.get("name", "N/A")
                            value = child.text
                            self.write2csv_layout(
                                "value",
                                f"{apk_name.replace(',','-')},value,{values_dir_name.replace(',','-')},{str(values_dir_size).replace(',','-')},{root_tag},other,N/A,{name.replace(',','-')},{str(value).replace(',','-')}",
                            )
                except ET.ParseError as e:
                    print(f"Error parsing {values_file}: {e}")

    def analyze(self):
        for root, dirs, files in os.walk(self.res_path):
            for _dir in dirs:
                if _dir.startswith("layout"):
                    layout_dir = os.path.join(root, _dir)
                    self.analyze_layout_files(layout_dir)
                elif _dir.startswith("drawable"):
                    drawable_dir = os.path.join(root, _dir)
                    self.analyze_drawable_files(drawable_dir)
                if _dir.startswith("values"):
                    values_dir = os.path.join(root, _dir)
                    self.analyze_values_files(values_dir)

        if self.coarse_grained:
            self.output()

    def output(self):
        print("Component counts:")
        for component, count in self.component_counts.items():
            print(f" - {component}: {count}")

        print("Drawable counts:")
        for drawable, count in self.drawable_counts.items():
            print(f" - {drawable}: {count}")

        print("File counts:")
        for file_type, count in self.file_counts.items():
            print(f" - {file_type}: {count}")


if __name__ == "__main__":
    root_dir = os.getenv("LITEAPPS_ROOT")
    decompiled_dir = os.path.join(root_dir, "static_analyze/decompiled")
    os.system("rm ./extracted_layout/*")
    os.system("rm ./extracted_drawable/*")
    os.system("rm ./extracted_value/*")
    amount = 0
    for root, dirs, files in os.walk(decompiled_dir):
        amount = len(dirs)
        print(dirs)
        break
    cnt = 0

    for root, dirs, files in os.walk(decompiled_dir):
        for _dir in dirs:
            print(f"progress: {cnt}/{amount}")
            apk_name = str(_dir)
            res_path = os.path.join(root, _dir, "res")
            res_analyze = ResAnalyze(res_path, apk_name, coarse_grained=False)
            res_analyze.analyze()
            cnt += 1
        break
