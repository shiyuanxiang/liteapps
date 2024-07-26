import xml.etree.ElementTree as ET
import os


def count_android_components(manifest_path):
    tree = ET.parse(manifest_path)
    root = tree.getroot()

    namespaces = {"android": "http://schemas.android.com/apk/res/android"}

    component_counts = {"activity": 0, "service": 0, "receiver": 0, "provider": 0}

    for elem in root.iter():
        if elem.tag.endswith("activity"):
            component_counts["activity"] += 1
        elif elem.tag.endswith("service"):
            component_counts["service"] += 1
        elif elem.tag.endswith("receiver"):
            component_counts["receiver"] += 1
        elif elem.tag.endswith("provider"):
            component_counts["provider"] += 1

    return component_counts


def get_xml_fp():
    xml_fps = []
    for root, dirs, files in os.walk("./manifest"):
        for file in files:
            if file.endswith(".xml"):
                xml_fps.append(os.path.join(root, file))
    xml_fps.sort(key=lambda x: int(x.split("/")[-1].split(".")[0]))
    return xml_fps


def main():
    xml_fps = get_xml_fp()
    aid2ccnt = {}
    with open("manifest_analyzed", "w") as fw:
        for xml_fp in xml_fps:
            component_counts = count_android_components(xml_fp)
            aid = int(xml_fp.split("/")[-1].split(".")[0])
            aid2ccnt[aid] = component_counts
            fw.write(f"[apk_id] {aid}\n")
            for component, count in component_counts.items():
                fw.write(f"-- [{component}]: {count}\n")
            fw.write("\n")
        fw.write("[abnormal lite full]\n")
        abnormal_cnt = 0
        abnormal_dict = {"activity": 0, "service": 0, "receiver": 0, "provider": 0}
        for aid, ccnt in aid2ccnt.items():
            if aid % 2 == 1 and (aid + 1) in aid2ccnt:
                is_abnormal = False
                for component, count in ccnt.items():
                    if aid2ccnt[aid + 1][component] > count:
                        fw.write(
                            f"{aid}-{aid+1} {component}: {count} {aid2ccnt[aid + 1][component]}\n"
                        )
                        is_abnormal = True
                        abnormal_dict[component] += 1
                if is_abnormal:
                    abnormal_cnt += 1
        fw.write(f"\n\n[abnormal apks] {abnormal_cnt}\n")
        fw.write(f"-- activity: {abnormal_dict['activity']} times\n")
        fw.write(f"-- service: {abnormal_dict['service']} times\n")
        fw.write(f"-- receiver: {abnormal_dict['receiver']} times\n")
        fw.write(f"-- provider: {abnormal_dict['provider']} times\n")


if __name__ == "__main__":
    main()
