import xml.etree.ElementTree as ET
import os
from tools import *


def count_android_components(manifest_path):
    tree = ET.parse(manifest_path)
    root = tree.getroot()

    namespaces = {"android": "http://schemas.android.com/apk/res/android"}

    component_counts = {"activity": 0, "service": 0, "receiver": 0, "provider": 0}
    activity = set()
    for elem in root.iter():
        if elem.tag.endswith("activity"):
            component_counts["activity"] += 1
            activity.add(
                elem.attrib.get(
                    "{http://schemas.android.com/apk/res/android}name"
                ).split(".")[-1]
            )
        elif elem.tag.endswith("service"):
            component_counts["service"] += 1
        elif elem.tag.endswith("receiver"):
            component_counts["receiver"] += 1
        elif elem.tag.endswith("provider"):
            component_counts["provider"] += 1

    return component_counts, activity


def count_activity_introduce_by_lite():
    xml_fps = get_xml_fp()
    aid2activity = {}
    aid2component_counts = {}
    for xml_fp in xml_fps:
        component_counts, activity = count_android_components(xml_fp)
        aid = int(xml_fp.split("/")[-1].split(".")[0])
        aid2activity[aid] = activity
        aid2component_counts[aid] = component_counts
    with open("manifest_analyzed", "a") as fw:
        fw.write("\n\n[activity introduced by lite (count)]\n")
        report_dict = {}
        for aid, activity in aid2activity.items():
            if aid % 2 == 0 and (aid - 1) in aid2activity:
                # fw.write(f"{aid}-{aid-1} {len(activity - aid2activity[aid - 1])}\n")
                report_dict[aid] = len(activity - aid2activity[aid - 1])
        report_dict = dict(
            sorted(report_dict.items(), key=lambda x: x[1], reverse=True)
        )
        for k, v in report_dict.items():
            fw.write(
                f"{k:<8} {v}/{aid2component_counts[k]['activity']:<5}  {v/aid2component_counts[k]['activity']:.2f}\n"
            )


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
            component_counts, _ = count_android_components(xml_fp)
            aid = int(xml_fp.split("/")[-1].split(".")[0])
            aid2ccnt[aid] = component_counts
            fw.write(f"[apk_id] {aid}\n")
            for component, count in component_counts.items():
                fw.write(f"-- [{component}]: {count}\n")
            fw.write("\n")
        fw.write("[abnormal lite full]\n")
        abnormal_cnt = 0
        abnormal_apk_ids = []
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
                    abnormal_apk_ids.append(aid + 1)
        fw.write(f"\n\n[abnormal apks] {abnormal_cnt} apk_id:\n")
        apk_names = id2app_name(abnormal_apk_ids)
        for an in apk_names:
            fw.write(f"{an}\n")
        fw.write(f"-- activity: {abnormal_dict['activity']} times\n")
        fw.write(f"-- service: {abnormal_dict['service']} times\n")
        fw.write(f"-- receiver: {abnormal_dict['receiver']} times\n")
        fw.write(f"-- provider: {abnormal_dict['provider']} times\n")
    count_activity_introduce_by_lite()


if __name__ == "__main__":
    main()
