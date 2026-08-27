from artifact_tool import Workbook, SpreadsheetFile
from datetime import datetime

# -----------------------------
# Create workbook and worksheets
# -----------------------------
wb = Workbook.create()
guide = wb.worksheets.add("START HERE")
inbox = wb.worksheets.add("INBOX")
processes = wb.worksheets.add("PROCESSES")
threads = wb.worksheets.add("THREADS")
instructions = wb.worksheets.add("INSTRUCTIONS")
scheduler = wb.worksheets.add("SCHEDULER")
config = wb.worksheets.add("CONFIG")

# -----------------------------
# Shared styles
# -----------------------------
title_fmt = {
    "fill": "#172554",
    "font": {"bold": True, "color": "#FFFFFF", "size": 18},
    "vertical_alignment": "center",
}
section_fmt = {
    "fill": "#1E3A8A",
    "font": {"bold": True, "color": "#FFFFFF", "size": 12},
    "vertical_alignment": "center",
}
header_fmt = {
    "fill": "#DBEAFE",
    "font": {"bold": True, "color": "#172554"},
    "horizontal_alignment": "center",
    "vertical_alignment": "center",
    "wrap_text": True,
    "borders": {
        "bottom": {"style": "continuous", "color": "#93C5FD"},
    },
}
input_fmt = {"fill": "#FFF7ED"}
formula_fmt = {"fill": "#F1F5F9"}
note_fmt = {"fill": "#F8FAFC", "font": {"color": "#334155"}, "wrap_text": True}

# -----------------------------
# CONFIG
# -----------------------------
config.get_range("A1:I1").merge()
config.get_range("A1").values = [["SYSTEM CONFIGURATION"]]
config.get_range("A1:I1").format = title_fmt
config.get_range("A1:I1").format.row_height = 30

config.get_range("A3:B7").values = [
    ["Current operating context", "Work computer"],
    ["Available minutes", 60],
    ["Current energy", "High"],
    ["Maximum active instructions", 1],
    ["Scheduler note", "Change the orange cells before choosing work."],
]
config.get_range("A3:A7").format = header_fmt
config.get_range("B3:B7").format = input_fmt
config.get_range("A3:A7").format.column_width = 28
config.get_range("B3:B7").format.column_width = 34
config.get_range("B7").format.wrap_text = True

config.get_range("D1:F1").values = [["Priority", "Weight", "Meaning"]]
config.get_range("D1:F1").format = header_fmt
config.get_range("D2:F6").values = [
    ["P0", 100, "Interrupt: emergency or immediate failure"],
    ["P1", 80, "Time-critical or high consequence"],
    ["P2", 50, "Important planned work"],
    ["P3", 20, "Maintenance and administration"],
    ["P4", 5, "Background or optional"],
]
config.get_range("D2:F6").format.wrap_text = True
config.get_range("D1:D6").format.column_width = 12
config.get_range("E1:E6").format.column_width = 10
config.get_range("F1:F6").format.column_width = 38

config.get_range("H1:I1").values = [["Energy", "Level"]]
config.get_range("H1:I1").format = header_fmt
config.get_range("H2:I4").values = [["Low", 1], ["Medium", 2], ["High", 3]]
config.get_range("H1:I4").format.column_width = 14

# Lists for dropdowns
config.get_range("K1:K11").values = [
    ["States"], ["INBOX"], ["DEFINED"], ["READY"], ["RUNNING"], ["WAITING"],
    ["BLOCKED"], ["SCHEDULED"], ["DONE"], ["CANCELLED"], ["SOMEDAY"]
]
config.get_range("L1:L6").values = [
    ["Contexts"], ["Any"], ["Work computer"], ["Home"], ["Errands"], ["Phone"]
]
config.get_range("M1:M6").values = [
    ["Classes"], ["PROJECT"], ["ROUTINE"], ["CASE"], ["MAINTENANCE"], ["EVENT"]
]
config.get_range("N1:N5").values = [["Energy"], ["Low"], ["Medium"], ["High"], ["Any"]]
config.get_range("O1:O6").values = [["Priority"], ["P0"], ["P1"], ["P2"], ["P3"], ["P4"]]
config.get_range("P1:P6").values = [["Areas"], ["Research"], ["Work"], ["Home"], ["Finances"], ["Health"]]
config.get_range("K1:P1").format = header_fmt

config.get_range("B3").data_validation = {
    "rule": {"type": "list", "formula1": "CONFIG!$L$2:$L$6"}
}
config.get_range("B5").data_validation = {
    "rule": {"type": "list", "formula1": "CONFIG!$N$2:$N$4"}
}
config.freeze_panes.freeze_rows(1)

# -----------------------------
# START HERE guide
# -----------------------------
guide.get_range("A1:H1").merge()
guide.get_range("A1").values = [["PERSONAL OPERATING SYSTEM"]]
guide.get_range("A1:H1").format = title_fmt
guide.get_range("A1:H1").format.row_height = 34

guide.get_range("A3:H3").merge()
guide.get_range("A3").values = [[
    "A computer-inspired productivity system: capture inputs, instantiate processes, divide them into threads, "
    "execute instructions, and let the scheduler choose from the READY queue."
]]
guide.get_range("A3:H3").format = note_fmt
guide.get_range("A3:H3").format.row_height = 44

guide.get_range("A5:C5").values = [["Computing term", "Personal analogue", "Naming rule"]]
guide.get_range("A5:C5").format = header_fmt
guide.get_range("A6:C13").values = [
    ["Input", "An unprocessed thought, obligation, idea or request", "Capture it exactly as it appears"],
    ["Process", "A finite outcome currently instantiated in your life", "Name the observable completed state"],
    ["Thread", "An independent workstream inside a process", "Use a component noun"],
    ["Instruction", "One executable physical or cognitive action", "Start with a verb"],
    ["State", "The runtime condition of an item", "READY, RUNNING, WAITING, BLOCKED, DONE"],
    ["Dependency", "An instruction that must finish first", "Reference its Instruction ID"],
    ["Scheduler", "The rule that allocates your attention", "Chooses only executable READY instructions"],
    ["Daemon", "A recurring maintenance routine", "Create recurring process instances when needed"],
]
guide.get_range("A5:C13").format.wrap_text = True
guide.get_range("A:A").format.column_width = 18
guide.get_range("B:B").format.column_width = 44
guide.get_range("C:C").format.column_width = 40

guide.get_range("E5:H5").merge()
guide.get_range("E5").values = [["OPERATING LOOP"]]
guide.get_range("E5:H5").format = section_fmt
guide.get_range("E6:H12").values = [
    ["1", "CAPTURE", "Put raw thoughts in INBOX", "Do not organise while capturing"],
    ["2", "CLARIFY", "Decide whether it is information, an instruction or a multi-step process", "Define the output"],
    ["3", "INSTANTIATE", "Create the process and its threads", "Only for outcomes needing multiple actions"],
    ["4", "COMPILE", "Translate work into executable instructions", "One action per row"],
    ["5", "DISPATCH", "Set executable instructions to READY", "Blocked and waiting work leaves the queue"],
    ["6", "SCHEDULE", "Set current context, time and energy in CONFIG", "Use SCHEDULER"],
    ["7", "EXECUTE", "Run one instruction and save a resume note", "Minimise context switching"],
]
guide.get_range("E6:H12").format.wrap_text = True
guide.get_range("E:E").format.column_width = 6
guide.get_range("F:F").format.column_width = 15
guide.get_range("G:G").format.column_width = 35
guide.get_range("H:H").format.column_width = 33

guide.get_range("A16:H16").merge()
guide.get_range("A16").values = [["SCALING RULES"]]
guide.get_range("A16:H16").format = section_fmt
guide.get_range("A17:H22").values = [
    ["Rule", "Small item", "Large item", "", "", "", "", ""],
    ["Use an instruction when", "It can be completed in one session", "Example: Replace the globe", "", "", "", "", ""],
    ["Use a process when", "Several dependent instructions are required", "Example: Hallway light working again", "", "", "", "", ""],
    ["Use threads when", "Parts can progress independently", "Example: Analysis, Discussion and Figures", "", "", "", "", ""],
    ["Store outcomes as", "Processes", "They define what DONE means", "", "", "", "", ""],
    ["Execute work as", "Instructions", "They define exactly what to do next", "", "", "", "", ""],
]
guide.get_range("A17:H22").format.wrap_text = True
guide.get_range("A17:H17").format = header_fmt
guide.freeze_panes.freeze_rows(3)

# -----------------------------
# INBOX
# -----------------------------
inbox.get_range("A1:H1").merge()
inbox.get_range("A1").values = [["INPUT BUFFER"]]
inbox.get_range("A1:H1").format = title_fmt
inbox.get_range("A2:H2").merge()
inbox.get_range("A2").values = [[
    "Capture first. During review, convert each input into a PROCESS, THREAD, INSTRUCTION, EVENT, RESOURCE or discard it."
]]
inbox.get_range("A2:H2").format = note_fmt
inbox_headers = ["Capture ID", "Captured At", "Raw Input", "Proposed Type", "Clarified?", "Converted To ID", "Review Date", "Notes"]
inbox.get_range("A4:H4").values = [inbox_headers]
inbox.get_range("A4:H4").format = header_fmt
inbox_rows = [
    ["CAP-001", datetime(2026, 7, 23, 8, 30), "Finish the journal article draft", "PROCESS", "Yes", "P-001", datetime(2026, 7, 23), "Outcome clarified as draft sent to coauthors"],
    ["CAP-002", datetime(2026, 7, 23, 8, 35), "The hallway light is out", "PROCESS", "Yes", "P-002", datetime(2026, 7, 23), "Needs inspection and purchase"],
    ["CAP-003", datetime(2026, 7, 23, 8, 40), "Review my taxes", "PROCESS", "Yes", "P-003", datetime(2026, 7, 23), "Clarified as return lodged and records archived"],
]
inbox.get_range("A5:H7").values = inbox_rows
inbox.get_range("B5:B200").format.number_format = "yyyy-mm-dd hh:mm"
inbox.get_range("G5:G200").format.number_format = "yyyy-mm-dd"
inbox.get_range("C5:H200").format.wrap_text = True
inbox.get_range("D5:D200").data_validation = {
    "rule": {"type": "list", "values": ["PROCESS", "THREAD", "INSTRUCTION", "EVENT", "RESOURCE", "REFERENCE", "DISCARD"]}
}
inbox.get_range("E5:E200").data_validation = {"rule": {"type": "list", "values": ["No", "Yes"]}}
inbox.get_range("A4:H200").format.row_height = 20
inbox.get_range("A:A").format.column_width = 14
inbox.get_range("B:B").format.column_width = 19
inbox.get_range("C:C").format.column_width = 42
inbox.get_range("D:E").format.column_width = 16
inbox.get_range("F:F").format.column_width = 18
inbox.get_range("G:G").format.column_width = 14
inbox.get_range("H:H").format.column_width = 36
inbox.tables.add("A4:H200", True, "InboxTable")
inbox.freeze_panes.freeze_rows(4)

# -----------------------------
# PROCESSES
# -----------------------------
processes.get_range("A1:N1").merge()
processes.get_range("A1").values = [["PROCESS TABLE — FINITE OUTCOMES"]]
processes.get_range("A1:N1").format = title_fmt
processes.get_range("A2:N2").merge()
processes.get_range("A2").values = [[
    "A process is an active instance of an outcome. Name it as the observable state that will exist when the process terminates."
]]
processes.get_range("A2:N2").format = note_fmt
process_headers = [
    "Process ID", "Process Name / Output", "Area", "Class", "State", "Priority", "Deadline",
    "Definition of DONE", "Current Thread", "Next Instruction", "Done Instructions",
    "Total Instructions", "Progress", "Notes"
]
processes.get_range("A4:N4").values = [process_headers]
processes.get_range("A4:N4").format = header_fmt
process_rows = [
    ["P-001", "Journal article draft sent to coauthors", "Research", "PROJECT", "ACTIVE", "P1", datetime(2026, 8, 7),
     "All main sections drafted; figures inserted; references checked; draft emailed to coauthors", "", "", "", "", "", "Cancer graph manuscript"],
    ["P-002", "Hallway light working again", "Home", "MAINTENANCE", "ACTIVE", "P3", datetime(2026, 7, 26),
     "Correct globe installed and light tested successfully", "", "", "", "", "", "Escalate to electrician only if replacement fails"],
    ["P-003", "2025–26 tax return lodged and records archived", "Finances", "PROJECT", "ACTIVE", "P1", datetime(2026, 10, 15),
     "Return reviewed and lodged; final return and supporting evidence archived", "", "", "", "", "", "Annual tax process instance"],
]
processes.get_range("A5:N7").values = process_rows
processes.get_range("G5:G100").format.number_format = "yyyy-mm-dd"
processes.get_range("H5:N100").format.wrap_text = True

# Process formulas
processes.get_range("I5").formulas = [[
    '=IFERROR(INDEX(INSTRUCTIONS!$D$5:$D$204,MATCH(MAXIFS(INSTRUCTIONS!$V$5:$V$204,INSTRUCTIONS!$C$5:$C$204,A5),INSTRUCTIONS!$V$5:$V$204,0)),"")'
]]
processes.get_range("I5:I100").fill_down()
processes.get_range("J5").formulas = [[
    '=IFERROR(INDEX(INSTRUCTIONS!$B$5:$B$204,MATCH(MAXIFS(INSTRUCTIONS!$V$5:$V$204,INSTRUCTIONS!$C$5:$C$204,A5),INSTRUCTIONS!$V$5:$V$204,0)),"")'
]]
processes.get_range("J5:J100").fill_down()
processes.get_range("K5").formulas = [['=COUNTIFS(INSTRUCTIONS!$C$5:$C$204,A5,INSTRUCTIONS!$E$5:$E$204,"DONE")']]
processes.get_range("K5:K100").fill_down()
processes.get_range("L5").formulas = [['=COUNTIF(INSTRUCTIONS!$C$5:$C$204,A5)']]
processes.get_range("L5:L100").fill_down()
processes.get_range("M5").formulas = [['=IFERROR(K5/L5,0)']]
processes.get_range("M5:M100").fill_down()
processes.get_range("M5:M100").format.number_format = "0%"
processes.get_range("I5:M100").format = formula_fmt

processes.get_range("C5:C100").data_validation = {"rule": {"type": "list", "formula1": "CONFIG!$P$2:$P$6"}}
processes.get_range("D5:D100").data_validation = {"rule": {"type": "list", "formula1": "CONFIG!$M$2:$M$6"}}
processes.get_range("E5:E100").data_validation = {
    "rule": {"type": "list", "values": ["PLANNED", "ACTIVE", "WAITING", "BLOCKED", "DONE", "CANCELLED", "SOMEDAY"]}
}
processes.get_range("F5:F100").data_validation = {"rule": {"type": "list", "formula1": "CONFIG!$O$2:$O$6"}}

processes.get_range("A:A").format.column_width = 12
processes.get_range("B:B").format.column_width = 38
processes.get_range("C:F").format.column_width = 14
processes.get_range("G:G").format.column_width = 13
processes.get_range("H:H").format.column_width = 48
processes.get_range("I:J").format.column_width = 30
processes.get_range("K:M").format.column_width = 14
processes.get_range("N:N").format.column_width = 34
processes.tables.add("A4:N100", True, "ProcessesTable")
processes.freeze_panes.freeze_rows(4)

# -----------------------------
# THREADS
# -----------------------------
threads.get_range("A1:J1").merge()
threads.get_range("A1").values = [["THREAD TABLE — INDEPENDENT WORKSTREAMS"]]
threads.get_range("A1:J1").format = title_fmt
threads.get_range("A2:J2").merge()
threads.get_range("A2").values = [[
    "Threads share the resources and outcome of a process but can progress or wait independently."
]]
threads.get_range("A2:J2").format = note_fmt
thread_headers = ["Thread ID", "Process ID", "Thread Name", "State", "Depends On Thread", "Done Instructions", "Total Instructions", "Progress", "Thread Output", "Notes"]
threads.get_range("A4:J4").values = [thread_headers]
threads.get_range("A4:J4").format = header_fmt
thread_rows = [
    ["T-001", "P-001", "Analysis", "ACTIVE", "", "", "", "", "Validated analysis outputs", ""],
    ["T-002", "P-001", "Discussion", "ACTIVE", "T-001", "", "", "", "Complete discussion section", ""],
    ["T-003", "P-001", "Figures and tables", "ACTIVE", "T-001", "", "", "", "Publication-ready figures and tables", ""],
    ["T-004", "P-001", "Coauthor coordination", "WAITING", "", "", "", "", "Resolved feedback and approved draft", ""],
    ["T-005", "P-002", "Diagnosis and purchasing", "ACTIVE", "", "", "", "", "Correct replacement globe available", ""],
    ["T-006", "P-002", "Installation and test", "BLOCKED", "T-005", "", "", "", "Light operating safely", ""],
    ["T-007", "P-003", "Income records", "ACTIVE", "", "", "", "", "All income evidence collected", ""],
    ["T-008", "P-003", "Deductions", "ACTIVE", "", "", "", "", "All deductions evidenced and summarised", ""],
    ["T-009", "P-003", "Review and lodgement", "BLOCKED", "T-007", "", "", "", "Return lodged and archived", ""],
]
threads.get_range("A5:J13").values = thread_rows
threads.get_range("F5").formulas = [['=COUNTIFS(INSTRUCTIONS!$D$5:$D$204,A5,INSTRUCTIONS!$E$5:$E$204,"DONE")']]
threads.get_range("F5:F100").fill_down()
threads.get_range("G5").formulas = [['=COUNTIF(INSTRUCTIONS!$D$5:$D$204,A5)']]
threads.get_range("G5:G100").fill_down()
threads.get_range("H5").formulas = [['=IFERROR(F5/G5,0)']]
threads.get_range("H5:H100").fill_down()
threads.get_range("H5:H100").format.number_format = "0%"
threads.get_range("F5:H100").format = formula_fmt
threads.get_range("D5:D100").data_validation = {
    "rule": {"type": "list", "values": ["PLANNED", "ACTIVE", "WAITING", "BLOCKED", "DONE", "CANCELLED", "SOMEDAY"]}
}
threads.get_range("A:A").format.column_width = 12
threads.get_range("B:B").format.column_width = 12
threads.get_range("C:C").format.column_width = 28
threads.get_range("D:E").format.column_width = 18
threads.get_range("F:H").format.column_width = 14
threads.get_range("I:I").format.column_width = 38
threads.get_range("J:J").format.column_width = 30
threads.get_range("C5:J100").format.wrap_text = True
threads.tables.add("A4:J100", True, "ThreadsTable")
threads.freeze_panes.freeze_rows(4)

# -----------------------------
# INSTRUCTIONS
# -----------------------------
instructions.get_range("A1:X1").merge()
instructions.get_range("A1").values = [["INSTRUCTION QUEUE — EXECUTABLE WORK"]]
instructions.get_range("A1:X1").format = title_fmt
instructions.get_range("A2:X2").merge()
instructions.get_range("A2").values = [[
    "Orange columns are human inputs. Grey columns are calculated by the scheduler. Only READY instructions that pass every gate can be dispatched."
]]
instructions.get_range("A2:X2").format = note_fmt
instruction_headers = [
    "Instruction ID", "Instruction", "Process ID", "Thread ID", "State", "Priority", "Deadline",
    "Duration Min", "Energy", "Context", "Blocked By", "Waiting For", "Scheduled At",
    "Importance", "Cost of Delay", "Created", "Resume Note", "Ready Gate", "Priority Score",
    "Urgency Score", "Fit Score", "Total Score", "Queue Rank", "Why Now"
]
instructions.get_range("A4:X4").values = [instruction_headers]
instructions.get_range("A4:X4").format = header_fmt

instruction_rows = [
    ["I-001", "Validate the final event-count outputs", "P-001", "T-001", "DONE", "P1", datetime(2026, 7, 24), 60, "High", "Work computer", "", "", "", 5, 5, datetime(2026, 7, 20), "Outputs saved in analysis/results", "", "", "", "", "", "", ""],
    ["I-002", "Draft the limitations paragraph", "P-001", "T-002", "READY", "P1", datetime(2026, 7, 30), 45, "High", "Work computer", "I-001", "", "", 5, 5, datetime(2026, 7, 21), "Begin with generalisability and source-data limitations", "", "", "", "", "", "", ""],
    ["I-003", "Generate the event-count table", "P-001", "T-003", "READY", "P2", datetime(2026, 7, 29), 40, "Medium", "Work computer", "I-001", "", "", 4, 4, datetime(2026, 7, 21), "Use validated output object", "", "", "", "", "", "", ""],
    ["I-004", "Incorporate coauthor comments into Methods", "P-001", "T-004", "WAITING", "P2", datetime(2026, 8, 2), 60, "High", "Work computer", "", "Coauthor comments", "", 4, 3, datetime(2026, 7, 22), "Resume at ontology paragraph", "", "", "", "", "", "", ""],
    ["I-005", "Email the complete draft to coauthors", "P-001", "T-004", "BLOCKED", "P1", datetime(2026, 8, 7), 15, "Low", "Work computer", "I-004", "", "", 5, 5, datetime(2026, 7, 22), "Attach manuscript and figures", "", "", "", "", "", "", ""],
    ["I-006", "Inspect and photograph the hallway fitting", "P-002", "T-005", "DONE", "P3", datetime(2026, 7, 23), 10, "Low", "Home", "", "", "", 3, 3, datetime(2026, 7, 23), "Fitting appears to be B22", "", "", "", "", "", "", ""],
    ["I-007", "Buy one suitable B22 LED globe", "P-002", "T-005", "READY", "P3", datetime(2026, 7, 25), 25, "Low", "Errands", "I-006", "", "", 3, 4, datetime(2026, 7, 23), "Take fitting photo", "", "", "", "", "", "", ""],
    ["I-008", "Replace the hallway globe and test the light", "P-002", "T-006", "BLOCKED", "P3", datetime(2026, 7, 26), 15, "Low", "Home", "I-007", "", "", 4, 4, datetime(2026, 7, 23), "Turn power off before replacement", "", "", "", "", "", "", ""],
    ["I-009", "Download the PAYG income statement", "P-003", "T-007", "READY", "P1", datetime(2026, 8, 15), 15, "Low", "Work computer", "", "", "", 4, 4, datetime(2026, 7, 23), "Save to tax/2025-26/income", "", "", "", "", "", "", ""],
    ["I-010", "Review home-office expenses", "P-003", "T-008", "READY", "P2", datetime(2026, 8, 30), 60, "Medium", "Home", "", "", "", 4, 3, datetime(2026, 7, 23), "Start with electricity and internet records", "", "", "", "", "", "", ""],
    ["I-011", "Upload evidence to the accountant portal", "P-003", "T-009", "BLOCKED", "P1", datetime(2026, 9, 15), 30, "Low", "Work computer", "I-009", "", "", 5, 4, datetime(2026, 7, 23), "Upload income documents first", "", "", "", "", "", "", ""],
]
instructions.get_range("A5:X15").values = instruction_rows

# Human input / calculated area colouring
instructions.get_range("A5:Q204").format = input_fmt
instructions.get_range("R5:X204").format = formula_fmt

# Formula columns
instructions.get_range("R5").formulas = [[
    '=IF(E5<>"READY","No",IF(AND(L5="",OR(M5="",M5<=NOW()),OR(K5="",COUNTIFS($A$5:$A$204,K5,$E$5:$E$204,"DONE")>0)),"Yes","No"))'
]]
instructions.get_range("R5:R204").fill_down()

instructions.get_range("S5").formulas = [[
    '=IFERROR(VLOOKUP(F5,CONFIG!$D$2:$E$6,2,FALSE),0)'
]]
instructions.get_range("S5:S204").fill_down()

instructions.get_range("T5").formulas = [[
    '=IF(G5="",0,IF(G5<TODAY(),60,MAX(0,40-(G5-TODAY())*2)))'
]]
instructions.get_range("T5:T204").fill_down()

instructions.get_range("U5").formulas = [[
    '=IF(OR(CONFIG!$B$3="Any",J5=CONFIG!$B$3),10,-20)+IF(H5<=CONFIG!$B$4,10,-15)+IFERROR(IF(OR(I5="Any",VLOOKUP(I5,CONFIG!$H$2:$I$4,2,FALSE)<=VLOOKUP(CONFIG!$B$5,CONFIG!$H$2:$I$4,2,FALSE)),10,-10),0)'
]]
instructions.get_range("U5:U204").fill_down()

instructions.get_range("V5").formulas = [[
    '=IF(R5="Yes",S5+T5+(N5*10)+(O5*8)+U5-MAX(0,H5-CONFIG!$B$4)/5,-999)'
]]
instructions.get_range("V5:V204").fill_down()

instructions.get_range("W5").formulas = [[
    '=IF(R5="Yes",RANK.EQ(V5,$V$5:$V$204,0)+COUNTIF($V$5:V5,V5)-1,"")'
]]
instructions.get_range("W5:W204").fill_down()

instructions.get_range("X5").formulas = [[
    '=IF(R5<>"Yes","Not executable",TEXTJOIN(", ",TRUE,IF(S5>=80,"high priority",""),IF(T5>=20,"deadline pressure",""),IF(U5>=20,"fits current context",""),IF(O5>=4,"high delay cost","")))'
]]
instructions.get_range("X5:X204").fill_down()

instructions.get_range("G5:G204").format.number_format = "yyyy-mm-dd"
instructions.get_range("M5:M204").format.number_format = "yyyy-mm-dd hh:mm"
instructions.get_range("P5:P204").format.number_format = "yyyy-mm-dd"
instructions.get_range("E5:E204").data_validation = {"rule": {"type": "list", "formula1": "CONFIG!$K$2:$K$11"}}
instructions.get_range("F5:F204").data_validation = {"rule": {"type": "list", "formula1": "CONFIG!$O$2:$O$6"}}
instructions.get_range("I5:I204").data_validation = {"rule": {"type": "list", "formula1": "CONFIG!$N$2:$N$5"}}
instructions.get_range("J5:J204").data_validation = {"rule": {"type": "list", "formula1": "CONFIG!$L$2:$L$6"}}

# Conditional formats
instructions.get_range("R5:R204").conditional_formats.add_custom('=R5="Yes"', {"fill": "#DCFCE7", "font": {"color": "#166534", "bold": True}})
instructions.get_range("R5:R204").conditional_formats.add_custom('=R5="No"', {"fill": "#FEE2E2", "font": {"color": "#991B1B"}})
instructions.get_range("V5:V204").conditional_formats.add_data_bar({"color": "#2563EB", "gradient": True})
instructions.get_range("E5:E204").conditional_formats.add_custom('=E5="DONE"', {"fill": "#DCFCE7"})
instructions.get_range("E5:E204").conditional_formats.add_custom('=E5="WAITING"', {"fill": "#FEF3C7"})
instructions.get_range("E5:E204").conditional_formats.add_custom('=E5="BLOCKED"', {"fill": "#FEE2E2"})
instructions.get_range("E5:E204").conditional_formats.add_custom('=E5="RUNNING"', {"fill": "#DBEAFE", "font": {"bold": True}})

# Widths
widths = {
    "A:A": 13, "B:B": 40, "C:D": 12, "E:F": 12, "G:G": 13, "H:H": 12,
    "I:J": 15, "K:K": 14, "L:L": 22, "M:M": 19, "N:O": 13, "P:P": 13,
    "Q:Q": 42, "R:R": 12, "S:W": 13, "X:X": 35
}
for rng, width in widths.items():
    instructions.get_range(rng).format.column_width = width
instructions.get_range("B5:X204").format.wrap_text = True
instructions.tables.add("A4:X204", True, "InstructionsTable")
instructions.freeze_panes.freeze_rows(4)
instructions.freeze_panes.freeze_columns(4)

# -----------------------------
# SCHEDULER
# -----------------------------
scheduler.get_range("A1:I1").merge()
scheduler.get_range("A1").values = [["CPU SCHEDULER — WHAT SHOULD RECEIVE ATTENTION NOW?"]]
scheduler.get_range("A1:I1").format = title_fmt
scheduler.get_range("A2:I2").merge()
scheduler.get_range("A2").values = [[
    "The scheduler only ranks instructions that are READY, unblocked, not waiting, due to run, and compatible with current time, energy and context."
]]
scheduler.get_range("A2:I2").format = note_fmt

# KPI cells
scheduler.get_range("A4:B8").values = [
    ["Runtime metric", "Value"],
    ["Executable READY", ""],
    ["RUNNING", ""],
    ["WAITING", ""],
    ["BLOCKED", ""],
]
scheduler.get_range("A4:B4").format = header_fmt
scheduler.get_range("B5").formulas = [['=COUNTIF(INSTRUCTIONS!$R$5:$R$204,"Yes")']]
scheduler.get_range("B6").formulas = [['=COUNTIF(INSTRUCTIONS!$E$5:$E$204,"RUNNING")']]
scheduler.get_range("B7").formulas = [['=COUNTIF(INSTRUCTIONS!$E$5:$E$204,"WAITING")']]
scheduler.get_range("B8").formulas = [['=COUNTIF(INSTRUCTIONS!$E$5:$E$204,"BLOCKED")']]
scheduler.get_range("B5:B8").format = formula_fmt
scheduler.get_range("A:A").format.column_width = 20
scheduler.get_range("B:B").format.column_width = 12

scheduler.get_range("D4:I4").values = [["Current Context", "Minutes", "Energy", "WIP Limit", "Today", "System Rule"]]
scheduler.get_range("D4:I4").format = header_fmt
scheduler.get_range("D5").formulas = [["=CONFIG!B3"]]
scheduler.get_range("E5").formulas = [["=CONFIG!B4"]]
scheduler.get_range("F5").formulas = [["=CONFIG!B5"]]
scheduler.get_range("G5").formulas = [["=CONFIG!B6"]]
scheduler.get_range("H5").formulas = [["=TODAY()"]]
scheduler.get_range("I5").values = [["Run the highest-ranked eligible instruction; save state before switching."]]
scheduler.get_range("D5:I5").format = formula_fmt
scheduler.get_range("H5").format.number_format = "yyyy-mm-dd"
scheduler.get_range("D:D").format.column_width = 18
scheduler.get_range("E:G").format.column_width = 12
scheduler.get_range("H:H").format.column_width = 14
scheduler.get_range("I:I").format.column_width = 44
scheduler.get_range("I5").format.wrap_text = True

scheduler.get_range("A11:I11").values = [[
    "Rank", "Instruction ID", "Process", "Thread", "Instruction", "Score", "Minutes", "Context", "Why now"
]]
scheduler.get_range("A11:I11").format = header_fmt
for row in range(12, 22):
    rank = row - 11
    scheduler.get_range(f"A{row}").values = [[rank]]
    scheduler.get_range(f"B{row}").formulas = [[f'=IFERROR(INDEX(INSTRUCTIONS!$A$5:$A$204,MATCH($A{row},INSTRUCTIONS!$W$5:$W$204,0)),"")']]
    scheduler.get_range(f"C{row}").formulas = [[f'=IFERROR(INDEX(PROCESSES!$B$5:$B$100,MATCH(INDEX(INSTRUCTIONS!$C$5:$C$204,MATCH($A{row},INSTRUCTIONS!$W$5:$W$204,0)),PROCESSES!$A$5:$A$100,0)),"")']]
    scheduler.get_range(f"D{row}").formulas = [[f'=IFERROR(INDEX(THREADS!$C$5:$C$100,MATCH(INDEX(INSTRUCTIONS!$D$5:$D$204,MATCH($A{row},INSTRUCTIONS!$W$5:$W$204,0)),THREADS!$A$5:$A$100,0)),"")']]
    scheduler.get_range(f"E{row}").formulas = [[f'=IFERROR(INDEX(INSTRUCTIONS!$B$5:$B$204,MATCH($A{row},INSTRUCTIONS!$W$5:$W$204,0)),"")']]
    scheduler.get_range(f"F{row}").formulas = [[f'=IFERROR(INDEX(INSTRUCTIONS!$V$5:$V$204,MATCH($A{row},INSTRUCTIONS!$W$5:$W$204,0)),"")']]
    scheduler.get_range(f"G{row}").formulas = [[f'=IFERROR(INDEX(INSTRUCTIONS!$H$5:$H$204,MATCH($A{row},INSTRUCTIONS!$W$5:$W$204,0)),"")']]
    scheduler.get_range(f"H{row}").formulas = [[f'=IFERROR(INDEX(INSTRUCTIONS!$J$5:$J$204,MATCH($A{row},INSTRUCTIONS!$W$5:$W$204,0)),"")']]
    scheduler.get_range(f"I{row}").formulas = [[f'=IFERROR(INDEX(INSTRUCTIONS!$X$5:$X$204,MATCH($A{row},INSTRUCTIONS!$W$5:$W$204,0)),"")']]
scheduler.get_range("B12:I21").format = formula_fmt
scheduler.get_range("C12:I21").format.wrap_text = True
scheduler.get_range("A:A").format.column_width = 8
scheduler.get_range("C:C").format.column_width = 33
scheduler.get_range("D:D").format.column_width = 24
scheduler.get_range("E:E").format.column_width = 42
scheduler.get_range("F:G").format.column_width = 12
scheduler.get_range("H:H").format.column_width = 16
scheduler.get_range("I:I").format.column_width = 34
scheduler.get_range("A11:I21").format.row_height = 24
scheduler.get_range("F12:F21").conditional_formats.add_data_bar({"color": "#2563EB", "gradient": True})

# State summary for chart
scheduler.get_range("K3:L9").values = [
    ["Instruction State", "Count"],
    ["READY", ""],
    ["RUNNING", ""],
    ["WAITING", ""],
    ["BLOCKED", ""],
    ["DONE", ""],
    ["SCHEDULED", ""],
]
scheduler.get_range("K3:L3").format = header_fmt
for r in range(4, 10):
    scheduler.get_range(f"L{r}").formulas = [[f'=COUNTIF(INSTRUCTIONS!$E$5:$E$204,K{r})']]
scheduler.get_range("L4:L9").format = formula_fmt
scheduler.get_range("K:K").format.column_width = 18
scheduler.get_range("L:L").format.column_width = 10

chart = scheduler.charts.add("bar", scheduler.get_range("K3:L9"))
chart.title_text = "Instruction Queue by State"
chart.has_legend = False
chart.set_position("K11", "Q27")

scheduler.get_range("A25:I25").merge()
scheduler.get_range("A25").values = [["DISPATCH PROTOCOL"]]
scheduler.get_range("A25:I25").format = section_fmt
scheduler.get_range("A26:I31").values = [
    ["1", "Select rank 1 unless a genuine interrupt exists.", "", "", "", "", "", "", ""],
    ["2", "Change its state from READY to RUNNING.", "", "", "", "", "", "", ""],
    ["3", "Work until DONE, blocked, waiting, or the focus block ends.", "", "", "", "", "", "", ""],
    ["4", "Before switching, write the exact resume point in Resume Note.", "", "", "", "", "", "", ""],
    ["5", "Set DONE only when the instruction's observable action is complete.", "", "", "", "", "", "", ""],
    ["6", "Review the parent process: compile the next instruction or terminate the process.", "", "", "", "", "", "", ""],
]
scheduler.get_range("A26:I31").format.wrap_text = True
scheduler.freeze_panes.freeze_rows(11)

# Add tables after formulas/data are present
scheduler.tables.add("A11:I21", True, "SchedulerQueueTable")

# Final touch: hide helper list columns in CONFIG visually by narrowing them
config.get_range("K:P").format.column_width = 12

# -----------------------------
# Compact verification
# -----------------------------
check1 = wb.inspect({
    "kind": "table",
    "range": "SCHEDULER!A1:I21",
    "include": "values,formulas",
    "table_max_rows": 21,
    "table_max_cols": 9,
})
print(check1.ndjson[:6000])

check2 = wb.inspect({
    "kind": "table",
    "range": "INSTRUCTIONS!A4:X15",
    "include": "values,formulas",
    "table_max_rows": 15,
    "table_max_cols": 24,
})
print(check2.ndjson[:6000])

errors = wb.inspect({
    "kind": "match",
    "search_term": "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
    "options": {"use_regex": True, "max_results": 100},
    "summary": "final formula error scan",
})
print(errors.ndjson)

# Render a compact preview for visual verification
preview = wb.render({"sheet_name": "SCHEDULER", "range": "A1:Q31", "scale": 1})
preview.save("/mnt/data/personal_operating_system_preview.png")

# Export
output_path = "/mnt/data/Personal_Operating_System.xlsx"
SpreadsheetFile.export_xlsx(wb).save(output_path)
print(output_path)
