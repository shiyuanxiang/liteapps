def compare_layout():
    with open("layout_analyzed", "r") as f:
        lines = f.readlines()
        is_full = 0
        full_dir_size = 0
        full_root_tag_button = 0
        full_root_tag_layout = 0
        full_component_type_av = 0
        full_component_type_bt = 0
        full_component_type_dc = 0
        full_component_type_iv = 0
        full_component_type_layout = 0
        full_component_type_picker = 0
        full_component_type_tc = 0
        full_text_filled = 0

        lite_dir_size = 0
        lite_root_tag_button = 0
        lite_root_tag_layout = 0
        lite_component_type_av = 0
        lite_component_type_bt = 0
        lite_component_type_dc = 0
        lite_component_type_iv = 0
        lite_component_type_layout = 0
        lite_component_type_picker = 0
        lite_component_type_tc = 0
        lite_text_filled = 0

        for line in lines:
            if line.startswith("- [layout]"):
                is_full += 1
                if is_full % 2 == 1 and is_full != 1:
                    apk_name = line.split(":")[1].split("_")[0]
                    print(f"[apk_name]: {apk_name}")
                    if lite_dir_size > full_dir_size:
                        print("[dir_size]: ", lite_dir_size, " > ", full_dir_size)
                    if lite_root_tag_button > full_root_tag_button:
                        print(
                            "[root_tag] Button: ",
                            lite_root_tag_button,
                            " > ",
                            full_root_tag_button,
                        )
                    if lite_root_tag_layout > full_root_tag_layout:
                        print(
                            "[root_tag] Layout: ",
                            lite_root_tag_layout,
                            " > ",
                            full_root_tag_layout,
                        )
                    if lite_component_type_av > full_component_type_av:
                        print(
                            "[component_type] Advanced View: ",
                            lite_component_type_av,
                            " > ",
                            full_component_type_av,
                        )
                    if lite_component_type_bt > full_component_type_bt:
                        print(
                            "[component_type] Button: ",
                            lite_component_type_bt,
                            " > ",
                            full_component_type_bt,
                        )
                    if lite_component_type_dc > full_component_type_dc:
                        print(
                            "[component_type] Display Control: ",
                            lite_component_type_dc,
                            " > ",
                            full_component_type_dc,
                        )
                    if lite_component_type_iv > full_component_type_iv:
                        print(
                            "[component_type] Image View: ",
                            lite_component_type_iv,
                            " > ",
                            full_component_type_iv,
                        )
                    if lite_component_type_layout > full_component_type_layout:
                        print(
                            "[component_type] Layout: ",
                            lite_component_type_layout,
                            " > ",
                            full_component_type_layout,
                        )
                    if lite_component_type_picker > full_component_type_picker:
                        print(
                            "[component_type] Picker: ",
                            lite_component_type_picker,
                            " > ",
                            full_component_type_picker,
                        )
                    if lite_component_type_tc > full_component_type_tc:
                        print(
                            "[component_type] Text Control: ",
                            lite_component_type_tc,
                            " > ",
                            full_component_type_tc,
                        )
                    if lite_text_filled > full_text_filled:
                        print(
                            "[text_filled]: ", lite_text_filled, " > ", full_text_filled
                        )

                    print("-------------------------------------------------")

                    full_dir_size = 0
                    full_root_tag_button = 0
                    full_root_tag_layout = 0
                    full_component_type_av = 0
                    full_component_type_bt = 0
                    full_component_type_dc = 0
                    full_component_type_iv = 0
                    full_component_type_layout = 0
                    full_component_type_picker = 0
                    full_component_type_tc = 0
                    full_text_filled = 0

                    lite_dir_size = 0
                    lite_root_tag_button = 0
                    lite_root_tag_layout = 0
                    lite_component_type_av = 0
                    lite_component_type_bt = 0
                    lite_component_type_dc = 0
                    lite_component_type_iv = 0
                    lite_component_type_layout = 0
                    lite_component_type_picker = 0
                    lite_component_type_tc = 0
                    lite_text_filled = 0
            if is_full % 2 == 1:
                if line.startswith("-- [dir_size]"):
                    full_dir_size += int(line.split(":")[1])
                elif line.startswith("-- [root_tag] Button"):
                    full_root_tag_button += int(line.split(":")[1])
                elif line.startswith("-- [root_tag] Layout"):
                    full_root_tag_layout += int(line.split(":")[1])
                elif line.startswith("-- [component_type] Advanced View"):
                    full_component_type_av += int(line.split(":")[1])
                elif line.startswith("-- [component_type] Button"):
                    full_component_type_bt += int(line.split(":")[1])
                elif line.startswith("-- [component_type] Display Control"):
                    full_component_type_dc += int(line.split(":")[1])
                elif line.startswith("-- [component_type] Image View"):
                    full_component_type_iv += int(line.split(":")[1])
                elif line.startswith("-- [component_type] Layout"):
                    full_component_type_layout += int(line.split(":")[1])
                elif line.startswith("-- [component_type] Picker"):
                    full_component_type_picker += int(line.split(":")[1])
                elif line.startswith("-- [component_type] Text Control"):
                    full_component_type_tc += int(line.split(":")[1])
                elif line.startswith("-- [text_filled]"):
                    full_text_filled += int(line.split(":")[1])
            else:
                if line.startswith("-- [dir_size]"):
                    lite_dir_size += int(line.split(":")[1])
                elif line.startswith("-- [root_tag] Button"):
                    lite_root_tag_button += int(line.split(":")[1])
                elif line.startswith("-- [root_tag] Layout"):
                    lite_root_tag_layout += int(line.split(":")[1])
                elif line.startswith("-- [component_type] Advanced View"):
                    lite_component_type_av += int(line.split(":")[1])
                elif line.startswith("-- [component_type] Button"):
                    lite_component_type_bt += int(line.split(":")[1])
                elif line.startswith("-- [component_type] Display Control"):
                    lite_component_type_dc += int(line.split(":")[1])
                elif line.startswith("-- [component_type] Image View"):
                    lite_component_type_iv += int(line.split(":")[1])
                elif line.startswith("-- [component_type] Layout"):
                    lite_component_type_layout += int(line.split(":")[1])
                elif line.startswith("-- [component_type] Picker"):
                    lite_component_type_picker += int(line.split(":")[1])
                elif line.startswith("-- [component_type] Text Control"):
                    lite_component_type_tc += int(line.split(":")[1])
                elif line.startswith("-- [text_filled]"):
                    lite_text_filled += int(line.split(":")[1])


def compare_value():
    with open("value_analyzed", "r") as f:
        lines = f.readlines()
        is_full = 0
        full_dir_size = 0
        full_dir_count = 0
        full_file_type_arrays = 0
        full_file_type_colors = 0
        full_file_type_dimens = 0
        full_file_type_string = 0
        full_file_type_styles = 0
        full_attr_type_action = 0
        full_attr_type_input = 0
        full_attr_type_media = 0
        full_attr_type_network = 0
        full_attr_type_notification = 0
        full_attr_type_other = 0
        full_attr_type_permission = 0
        full_attr_type_security = 0
        full_attr_type_storage = 0
        full_attr_type_ui = 0
        full_security = 0

        lite_dir_size = 0
        lite_dir_count = 0
        lite_file_type_arrays = 0
        lite_file_type_colors = 0
        lite_file_type_dimens = 0
        lite_file_type_string = 0
        lite_file_type_styles = 0
        lite_attr_type_action = 0
        lite_attr_type_input = 0
        lite_attr_type_media = 0
        lite_attr_type_network = 0
        lite_attr_type_notification = 0
        lite_attr_type_other = 0
        lite_attr_type_permission = 0
        lite_attr_type_security = 0
        lite_attr_type_storage = 0
        lite_attr_type_ui = 0
        lite_security = 0

        is_full = 0
        for line in lines:
            if line.startswith("- [value] apk:"):
                is_full += 1
                if is_full % 2 == 1 and is_full != 1:
                    apk_name = line.split(":")[1].split("_")[0]
                    print(f"[apk_name]: {line}")
                    if lite_dir_size > full_dir_size:
                        print("[dir_size]: ", lite_dir_size, " > ", full_dir_size)
                    if lite_dir_count > full_dir_count:
                        print("[dir_count]: ", lite_dir_count, " > ", full_dir_count)
                    if lite_file_type_arrays > full_file_type_arrays:
                        print(
                            "[file_type] Arrays: ",
                            lite_file_type_arrays,
                            " > ",
                            full_file_type_arrays,
                        )
                    if lite_file_type_colors > full_file_type_colors:
                        print(
                            "[file_type] Colors: ",
                            lite_file_type_colors,
                            " > ",
                            full_file_type_colors,
                        )
                    if lite_file_type_dimens > full_file_type_dimens:
                        print(
                            "[file_type] Dimens: ",
                            lite_file_type_dimens,
                            " > ",
                            full_file_type_dimens,
                        )
                    if lite_file_type_string > full_file_type_string:
                        print(
                            "[file_type] String: ",
                            lite_file_type_string,
                            " > ",
                            full_file_type_string,
                        )
                    if lite_file_type_styles > full_file_type_styles:
                        print(
                            "[file_type] Styles: ",
                            lite_file_type_styles,
                            " > ",
                            full_file_type_styles,
                        )
                    if lite_attr_type_action > full_attr_type_action:
                        print(
                            "[attr_type] Action: ",
                            lite_attr_type_action,
                            " > ",
                            full_attr_type_action,
                        )
                    if lite_attr_type_input > full_attr_type_input:
                        print(
                            "[attr_type] Input: ",
                            lite_attr_type_input,
                            " > ",
                            full_attr_type_input,
                        )
                    if lite_attr_type_media > full_attr_type_media:
                        print(
                            "[attr_type] Media: ",
                            lite_attr_type_media,
                            " > ",
                            full_attr_type_media,
                        )
                    if lite_attr_type_network > full_attr_type_network:
                        print(
                            "[attr_type] Network: ",
                            lite_attr_type_network,
                            " > ",
                            full_attr_type_network,
                        )
                    if lite_attr_type_notification > full_attr_type_notification:
                        print(
                            "[attr_type] Notification: ",
                            lite_attr_type_notification,
                            " > ",
                            full_attr_type_notification,
                        )
                    if lite_attr_type_other > full_attr_type_other:
                        print(
                            "[attr_type] Other: ",
                            lite_attr_type_other,
                            " > ",
                            full_attr_type_other,
                        )
                    if lite_attr_type_permission > full_attr_type_permission:
                        print(
                            "[attr_type] Permission: ",
                            lite_attr_type_permission,
                            " > ",
                            full_attr_type_permission,
                        )
                    if lite_attr_type_security > full_attr_type_security:
                        print(
                            "[attr_type] Security: ",
                            lite_attr_type_security,
                            " > ",
                            full_attr_type_security,
                        )
                    if lite_attr_type_storage > full_attr_type_storage:
                        print(
                            "[attr_type] Storage: ",
                            lite_attr_type_storage,
                            " > ",
                            full_attr_type_storage,
                        )
                    if lite_attr_type_ui > full_attr_type_ui:
                        print(
                            "[attr_type] UI: ",
                            lite_attr_type_ui,
                            " > ",
                            full_attr_type_ui,
                        )
                    if lite_security > full_security:
                        print("[security]: ", lite_security, " > ", full_security)

                    print("-------------------------------------------------")

                    full_dir_size = 0
                    full_dir_count = 0
                    full_file_type_arrays = 0
                    full_file_type_colors = 0
                    full_file_type_dimens = 0
                    full_file_type_string = 0
                    full_file_type_styles = 0
                    full_attr_type_action = 0
                    full_attr_type_input = 0
                    full_attr_type_media = 0
                    full_attr_type_network = 0
                    full_attr_type_notification = 0
                    full_attr_type_other = 0
                    full_attr_type_permission = 0
                    full_attr_type_security = 0
                    full_attr_type_storage = 0
                    full_attr_type_ui = 0
                    full_security = 0

                    lite_dir_size = 0
                    lite_dir_count = 0
                    lite_file_type_arrays = 0
                    lite_file_type_colors = 0
                    lite_file_type_dimens = 0
                    lite_file_type_string = 0
                    lite_file_type_styles = 0
                    lite_attr_type_action = 0
                    lite_attr_type_input = 0
                    lite_attr_type_media = 0
                    lite_attr_type_network = 0
                    lite_attr_type_notification = 0
                    lite_attr_type_other = 0
                    lite_attr_type_permission = 0
                    lite_attr_type_security = 0
                    lite_attr_type_storage = 0
                    lite_attr_type_ui = 0
                    lite_security = 0

            if is_full % 2 == 1:
                if line.startswith("-- [dir_size]"):
                    if line.split(":")[1] == " nan\n":
                        full_dir_size += 0
                    else:
                        full_dir_size += int(float(line.split(":")[1].strip()))
                    full_dir_count += 1
                elif line.startswith("-- [file_type] arrays"):
                    full_file_type_arrays += int(line.split(":")[1])
                elif line.startswith("-- [file_type] colors"):
                    full_file_type_colors += int(line.split(":")[1])
                elif line.startswith("-- [file_type] dimens"):
                    full_file_type_dimens += int(line.split(":")[1])
                elif line.startswith("-- [file_type] string"):
                    full_file_type_string += int(line.split(":")[1])
                elif line.startswith("-- [file_type] styles"):
                    full_file_type_styles += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] Action"):
                    full_attr_type_action += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] Input"):
                    full_attr_type_input += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] Media"):
                    full_attr_type_media += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] Network"):
                    full_attr_type_network += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] Notification"):
                    full_attr_type_notification += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] Other"):
                    full_attr_type_other += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] Permission"):
                    full_attr_type_permission += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] Security"):
                    full_attr_type_security += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] Storage"):
                    full_attr_type_storage += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] UI"):
                    full_attr_type_ui += int(line.split(":")[1])
                elif line.startswith("-- [security]"):
                    full_security += int(line.split(":")[1])
            else:
                if line.startswith("-- [dir_size]"):
                    if line.split(":")[1] == " nan\n":
                        lite_dir_size += 0
                    else:
                        lite_dir_size += int(float(line.split(":")[1].strip()))
                    lite_dir_count += 1
                elif line.startswith("-- [file_type] arrays"):
                    lite_file_type_arrays += int(line.split(":")[1])
                elif line.startswith("-- [file_type] colors"):
                    lite_file_type_colors += int(line.split(":")[1])
                elif line.startswith("-- [file_type] dimens"):
                    lite_file_type_dimens += int(line.split(":")[1])
                elif line.startswith("-- [file_type] string"):
                    lite_file_type_string += int(line.split(":")[1])
                elif line.startswith("-- [file_type] styles"):
                    lite_file_type_styles += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] Action"):
                    lite_attr_type_action += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] Input"):
                    lite_attr_type_input += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] Media"):
                    lite_attr_type_media += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] Network"):
                    lite_attr_type_network += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] Notification"):
                    lite_attr_type_notification += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] Other"):
                    lite_attr_type_other += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] Permission"):
                    lite_attr_type_permission += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] Security"):
                    lite_attr_type_security += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] Storage"):
                    lite_attr_type_storage += int(line.split(":")[1])
                elif line.startswith("-- [attr_type] UI"):
                    lite_attr_type_ui += int(line.split(":")[1])
                elif line.startswith("-- [security]"):
                    lite_security += int(line.split(":")[1])


if __name__ == "__main__":
    # compare_layout()
    compare_value()
