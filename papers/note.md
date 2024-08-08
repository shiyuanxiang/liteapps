# PEDroid
### Differential Analysis:
1. **Purpose:**
   - Identify and match methods modified between two versions of an Android app to pinpoint changes indicating patches.

2. **Methods:**
   - **Structure Construction & Feature Extraction:** Disassemble code into a hierarchy and extract features, normalizing code orders.
   - **Package-level Matching:** Identify identical and similar packages based on positional relationships within the package hierarchy.
   - **Matching Relation Extraction:** Establish method-level matching and classify methods into Identical, Similar, New, or Deleted categories.

3. **Tools:**
   - **Baksmali:** Disassembles Dex bytecode.
   - **Python:** Implements differential analysis algorithms.

4. **Performance:**
   - Found 429 modified methods classified as Similar out of 36,811 methods analyzed.
   - Achieved a recall of 92.86% on the dBench dataset.
   - Most updates analyzed within 5 to 10 minutes, with time varying based on APK size.

### Patch Identification:
1. **Purpose:**
   - Distinguish modified methods that contain patches addressing bugs or vulnerabilities.

2. **Methods:**
   - **Call Site Analysis:** Uses static taint analysis to identify methods utilizing external values.
   - **Internal Semantic Comparison:** Compares internal semantics of matched methods to identify changes fixing processing logic or handling errors.

3. **Tools:**
   - **Find Security Bugs:** Basis for taint analysis.
   - **Soot:** Framework for analyzing and transforming Java and Android apps.

4. **Performance:**
   - Identified 60 patches, with 41 correctly identified and nine false positives.
   - Majority of updates analyzed within 20 minutes.
   - High accuracy, with detailed analysis of false negatives and false positives for improvement.

### Dataset
1. **dBench:**
    - 6 projects with a total of 13 updates.
    - Includes 83 commits, with 36 identified as patches.
    - https://github.com/gsantner/markor
    - https://github.com/barbeau/gpstest
    - https://github.com/zhanghai/MaterialFiles
    - https://github.com/andOTP/andOTP
    - https://github.com/codinguser/gnucash-android
    - https://github.com/ankidroid/Anki-Android
2. **Pre-installed Apps:**
    - APK files of pre-installed apps extracted from Android phones of six mainstream manufacturers (Huawei, Motorola, OnePlus, Samsung, Vivo, Xiaomi).
    - 187 unique apps collected from regular monitoring and filtering based on vendor signatures.
    - 568 app updates categorized by version gaps (major upgrades, minor upgrades, small updates).

    