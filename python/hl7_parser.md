---
title: "python_hl7_helper"
format: html
editor: visual
---

PYTHON BCC SCC

```{python}

# from hl7conv2 import Hl7Json
# 
# hl7_string = """MSH|^~\\&|ADT1|HOSPITAL|LAB|HOSPITAL|20240101120000|SECURITY|ADT^A01^ADT_A01|MSG00001|T|2.5.1
# PID|1||PATID1234||DOE^JOHN||19800101|M"""
# 
# # Basic usage (default settings)
# hl7_obj = Hl7Json(hl7_string)
# json_data = hl7_obj.hl7_json
# 
# # Create with custom settings
# hl7_obj = Hl7Json(
#     hl7_string,
#     validation_enabled=True,
#     strict_validation=False,
#     escaping_enabled=True
# )
# 
# print(json.dumps(json_data, indent=2))
# 
# # Save to file
# with open("hl7_output.json", "w", encoding="utf-8") as f:
#     json.dump(json_data, f, indent=2)

```

```{python}
import re
import pandas as pd 

from hl7apy.parser import parse_message


def hl7messageobj_to_dict(m, p_use_long_name=True):
    """Convert an HL7 message to a dictionary
    :param m: The HL7 message
    :param p_use_long_name: Whether or not to user the long names
                          (e.g. "patient_name" instead of "pid_5")
    :returns: A dictionary representation of the HL7 message
    """
    if m.children:
        d = {}
        for c in m.children:
            name = str(c.name).lower()
            if p_use_long_name:
                name = str(c.long_name).lower() if c.long_name else name
            dictified = hl7messageobj_to_dict(c, p_use_long_name=p_use_long_name)
            if name in d:
                if not isinstance(d[name], list):
                    d[name] = [d[name]]
                d[name].append(dictified)
            else:
                d[name] = dictified
        return d
    else:
        return m.to_er7()


def udf(p_hl7v2_raw_msg):
  
    """Convert HL7 string to json
    """

    # replace new line with carriage return
    s = p_hl7v2_raw_msg.replace("\n", "\r")

    # Parse the message into object
    hl7_obj = parse_message(s)

    hl7_dict = hl7messageobj_to_dict(hl7_obj, True)
    
    return hl7_dict
  
def read_msgs(p_hl7msgfile):
    
    msgs = []

    with open(p_hl7msgfile, "r", encoding="utf-8", errors="replace", newline="") as f:
        raw_data = f.read()

    raw_data = raw_data.replace("\r\n", "\n").replace("\r", "\n")

    parts = re.split(r'(?=MSH\|)', raw_data)

    msgs = [p.strip() for p in parts if p.strip()]

    msgs = [m.replace("\n", "\r") for m in msgs]

    return msgs
  
def main(p_hl7msgfile, p_targetfile):
  
    msgs = read_msgs(p_hl7msgfile)
    
    total_msgs = len(msgs)

    df = pd.DataFrame(msgs, columns=["raw_msg"])
    
    df.to_csv(p_targetfile, index=False)

    ret = {
        "rows": total_msgs
    }
    
    return ret

# helper 

  
bcc_file_path = "H:/Restricted Share/NSWCR Identified Data/NMSC Landing Files/PS NonReportable BCC 2025.txt"
scc_file_path = "H:/Restricted Share/NSWCR Identified Data/NMSC Landing Files/PS NonReportable SCC 2025.txt"

bcc_msgs = read_msgs(bcc_file_path)
scc_msgs = read_msgs(scc_file_path)

bcc_df = pd.DataFrame(bcc_msgs, columns=["raw_msg"])
scc_df = pd.DataFrame(scc_msgs, columns=["raw_msg"])

bcc_df["SOURCE"] = "BCC"
scc_df["SOURCE"] = "SCC"

df = pd.concat([bcc_df, scc_df], ignore_index=True)
df["SOURCE"].value_counts()

```

PARSE

When finding the correct keys better to print the json and find the hierarchy 

Message  └ Segment      └ Field          └ Component              └ Subcomponent

```{python}

# SAMPLE 
# tmp = df.sample(10)
# 
# tmp["json_hl7"]   = tmp["raw_msg"].apply(udf)
# 
# import json
# print(json.dumps(tmp["json_hl7"].iloc[0], indent=2))

df["json_hl7"] = df["raw_msg"].apply(udf)

def nested_get(d, *keys):
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k)
        else:
            return None
    return d

df["message_control_id"] = df["json_hl7"].apply(
    lambda x: nested_get(x, "msh", "message_control_id", "st", "st")
)

df["date_time_of_message"] = df["json_hl7"].apply(
    lambda x: nested_get(x, "msh", "date_time_of_message", "time_of_an_event", "st")
)

df["sending_facility"] = df["json_hl7"].apply(
    lambda x: nested_get(x, "msh", "sending_facility", "namespace_id", "is")
)

df["patient_id"] = df["json_hl7"].apply(
    lambda x: nested_get(x, "oru_r01_patient_result", "oru_r01_patient", "pid", "patient_id", "id", "st")
)

df["date_time_of_birth"] = df["json_hl7"].apply(
    lambda x: nested_get(x, "oru_r01_patient_result", "oru_r01_patient", "pid", "date_time_of_birth", "time_of_an_event", "st")
)

df["sex"] = df["json_hl7"].apply(
    lambda x: nested_get(x, "oru_r01_patient_result", "oru_r01_patient", "pid", "sex", "is", "is")
)

df["assigned_patient_location"] = df["json_hl7"].apply(
    lambda x: nested_get(x, "oru_r01_patient_result", "oru_r01_patient", "oru_r01_visit", "pv1", "assigned_patient_location", "point_of_care", "is")
)

# SAVE
df.to_csv("SCC_BCC_HALF_PARSED.csv")
```

**RESULTS **

```{python}

import pandas as pd

# --- clean dates ---
df["date_time_of_birth"] = pd.to_datetime(
    df["date_time_of_birth"],
    format="%Y%m%d",
    errors="coerce"
)

df["date_time_of_message"] = pd.to_datetime(
    df["date_time_of_message"],
    format="%Y%m%d%H%M%S",
    errors="coerce"
)

# --- age ---
today = pd.Timestamp.today().normalize()
df["age"] = ((today - df["date_time_of_birth"]).dt.days / 365.25).round(1)

# --- 1. total reports ---
total_reports = len(df)

# --- 2. unique reports ---
unique_reports = df["message_control_id"].nunique(dropna=True)

# --- 3. duplicate reports ---
duplicate_reports = df.duplicated(subset=["message_control_id"]).sum()

# --- 4. unique people ---
unique_people = df["patient_id"].nunique(dropna=True)

# --- 5. people split by gender ---
people_by_gender = (
    df.drop_duplicates(subset=["patient_id"])
      .groupby("sex")["patient_id"]
      .nunique()
      .sort_values(ascending=False)
)

# --- 6. report counts by gender ---
reports_by_gender = df["sex"].value_counts(dropna=False)

# --- 7. age summary ---
age_summary = df.drop_duplicates(subset=["patient_id"])["age"].describe()

# --- 8. age groups ---
age_bins = [0, 18, 30, 40, 50, 60, 70, 80, 120]
age_labels = ["0-17", "18-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"]
df_unique_people = df.drop_duplicates(subset=["patient_id"]).copy()
df_unique_people["age_group"] = pd.cut(df_unique_people["age"], bins=age_bins, labels=age_labels, right=False)
age_distribution = df_unique_people["age_group"].value_counts().sort_index()

# --- 9. facilities ---
facility_counts = df["sending_facility"].value_counts(dropna=False)

# --- 10. patient locations / clinics if useful ---
location_counts = df["assigned_patient_location"].value_counts(dropna=False)

# --- print results ---
print("Total reports:", total_reports)
print("Unique reports:", unique_reports)
print("Duplicate reports:", duplicate_reports)
print("Unique people:", unique_people)

print("\nPeople by gender:")
print(people_by_gender)

print("\nReports by gender:")
print(reports_by_gender)

print("\nAge summary:")
print(age_summary)

print("\nAge distribution:")
print(age_distribution)

print("\nSending facilities:")
print(facility_counts)

print("\nAssigned patient locations:")
print(location_counts)
  

possible_updated_reports = df.duplicated(
    subset=["patient_id", "date_time_of_message", "sending_facility"],
    keep=False
).sum()

print("\nPossible updated/repeated reports:", possible_updated_reports)

summary = {
    "total_reports": total_reports,
    "unique_reports": unique_reports,
    "duplicate_reports": duplicate_reports,
    "unique_people": unique_people,
    "n_facilities": df["sending_facility"].nunique(dropna=True),
    "n_locations": df["assigned_patient_location"].nunique(dropna=True),
}

print(pd.Series(summary))

print(df["sending_facility"].dropna().unique())
```
