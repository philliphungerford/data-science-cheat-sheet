import tkinter as tk
from tkinter import filedialog, scrolledtext, simpledialog
import xml.etree.ElementTree as ET
import os
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import textwrap

# --- Model Setup ---
default_model_name = "facebook-bert"
model_dir = os.path.join(os.path.dirname(__file__), f"model/{default_model_name}")
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForSequenceClassification.from_pretrained(model_dir)
model.eval()

# --- XML Parsing ---
def strip_namespace(tag):
    return tag.split("}", 1)[1] if "}" in tag else tag

def parse_element(elem, parent_path=""):
    path = f"{parent_path}/{strip_namespace(elem.tag)}" if parent_path else strip_namespace(elem.tag)
    rows = []
    if elem.text and elem.text.strip():
        rows.append((path, elem.text.strip()))
    for child in elem:
        rows.extend(parse_element(child, path))
    return rows

# --- NLI & chunking ---
def run_nli_chunked(report_text, question, tokenizer, model, chunk_size=100, method="max"):
    words = report_text.split()
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

    entail_probs = []
    for chunk in chunks:
        inputs = tokenizer(chunk, question, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
            probs = F.softmax(outputs.logits, dim=-1)
        labels = [model.config.id2label[i].upper() for i in range(probs.size(-1))]
        prob_dict = dict(zip(labels, probs[0].tolist()))
        entail_prob = prob_dict.get("ENTAILMENT", 0.0)
        entail_probs.append(entail_prob)

    overall_prob = max(entail_probs) if method == "max" else sum(entail_probs)/len(entail_probs)
    return overall_prob, chunks, entail_probs

# --- Bold question words in full text ---
def bold_question_words(question):
    full_text_box.tag_remove("bold", "1.0", tk.END)
    if not question:
        return
    words = question.split()
    for word in words:
        start = "1.0"
        while True:
            pos = full_text_box.search(rf'\b{word}\b', start, stopindex=tk.END, nocase=True, regexp=True)
            if not pos:
                break
            end = f"{pos}+{len(word)}c"
            full_text_box.tag_add("bold", pos, end)
            start = end
    full_text_box.tag_config("bold", font=("TkDefaultFont", 10, "bold"), foreground="red")

# --- Helper functions ---
def get_chunk_size():
    try:
        val = int(chunk_size_entry.get())
        return max(1, val)
    except:
        return 100

def wrap_chunk_text(text, width=80):
    return "\n".join(textwrap.wrap(text, width=width))

# --- GUI Functions ---
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")], title="Select a Pathology Report")
    if not file_path:
        return
    tree = ET.parse(file_path)
    root = tree.getroot()

    full_text_box.delete("1.0", tk.END)
    nli_result_box.delete("1.0", tk.END)
    question_entry.delete(0, tk.END)

    rows = parse_element(root)
    full_text = "\n".join([str(val) for _, val in rows])
    full_text_box.insert(tk.END, full_text)
    update_chunks_display()

def enter_plain_text():
    full_text_box.delete("1.0", tk.END)
    nli_result_box.delete("1.0", tk.END)
    question_entry.delete(0, tk.END)
    text = simpledialog.askstring("Enter Text", "Paste your report text here:")
    if text:
        full_text_box.insert(tk.END, text)
        update_chunks_display()

def select_model():
    model_base_dir = os.path.join(os.path.dirname(__file__), "model")
    subfolders = [f for f in os.listdir(model_base_dir) if os.path.isdir(os.path.join(model_base_dir, f))]
    if not subfolders:
        return
    selection_text = "\n".join([f"{i+1}: {name}" for i, name in enumerate(subfolders)])
    choice = simpledialog.askinteger("Select Model", f"Available models:\n{selection_text}\n\nEnter number:")
    if choice is None or choice < 1 or choice > len(subfolders):
        return
    selected_model_name = subfolders[choice-1]
    selected_model_path = os.path.join(model_base_dir, selected_model_name)
    global tokenizer, model
    tokenizer = AutoTokenizer.from_pretrained(selected_model_path)
    model = AutoModelForSequenceClassification.from_pretrained(selected_model_path)
    model.eval()
    model_label.config(text=f"Current model: {selected_model_name}")

def update_chunks_display():
    text = full_text_box.get("1.0", tk.END).strip()
    if not text:
        return
    chunk_size = get_chunk_size()
    chunks = [" ".join(text.split()[i:i+chunk_size]) for i in range(0, len(text.split()), chunk_size)]

    chunk_text.config(state=tk.NORMAL)
    chunk_text.delete("1.0", tk.END)
    for i, chunk in enumerate(chunks, start=1):
        wrapped_chunk = wrap_chunk_text(chunk, width=80)
        chunk_text.insert(tk.END, f"Chunk {i} (Prob: -)\n{wrapped_chunk}\n")
        chunk_text.insert(tk.END, "-"*80 + "\n", "divider")
    chunk_text.tag_configure("divider", foreground="gray", font=("TkDefaultFont", 8, "italic"))
    chunk_text.config(state=tk.DISABLED)

def ask_question():
    question = question_entry.get().strip()
    if not question:
        return
    nli_result_box.delete("1.0", tk.END)
    status_label.config(text="Analyzing...", foreground="blue")
    root.update_idletasks()

    full_text = full_text_box.get("1.0", tk.END).strip()
    method = entailment_method.get()
    chunk_size = get_chunk_size()
    overall_prob, chunks, probs = run_nli_chunked(full_text, question, tokenizer, model, chunk_size=chunk_size, method=method)

    bold_question_words(question)
    nli_result_box.insert(tk.END, f"Probability of '{question}' being true ({method}): {overall_prob:.2f}\n")

    # Update chunk_text with probabilities and highlights
    chunk_text.config(state=tk.NORMAL)
    chunk_text.delete("1.0", tk.END)
    for i, (chunk, prob) in enumerate(zip(chunks, probs), start=1):
        wrapped_chunk = wrap_chunk_text(chunk, width=80)
        header = f"Chunk {i} (Prob: {prob:.2f})\n"
        chunk_text.insert(tk.END, header, ("high_prob" if prob >= 0.5 else ""))
        chunk_text.insert(tk.END, f"{wrapped_chunk}\n")
        chunk_text.insert(tk.END, "-"*80 + "\n", "divider")

    chunk_text.tag_configure("high_prob", background="yellow")
    chunk_text.tag_configure("divider", foreground="gray", font=("TkDefaultFont", 8, "italic"))
    chunk_text.config(state=tk.DISABLED)

    status_label.config(text="Analysis complete", foreground="green")

def on_chunk_size_change(event=None):
    update_chunks_display()

# --- Tkinter GUI ---
root = tk.Tk()
root.title("Phils Epath NLI Analyser")
root.geometry("1200x800")

left_frame = tk.Frame(root)
right_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5, pady=5)

# --- Left Panel ---
tk.Label(left_frame, text="Full Report Text").pack()
full_text_box = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD)
full_text_box.pack(expand=True, fill=tk.BOTH)

# --- Right Panel ---
button_frame = tk.Frame(right_frame)
button_frame.pack(pady=5, fill=tk.X)

open_button = tk.Button(button_frame, text="Open XML File", command=open_file)
open_button.pack(side=tk.LEFT, padx=5)

plain_text_button = tk.Button(button_frame, text="Enter Plain Text", command=enter_plain_text)
plain_text_button.pack(side=tk.LEFT, padx=5)

select_model_button = tk.Button(button_frame, text="Select Model", command=select_model)
select_model_button.pack(side=tk.LEFT, padx=5)

model_label = tk.Label(button_frame, text=f"Current model: {default_model_name}")
model_label.pack(side=tk.LEFT, padx=10)

# --- Chunk size adjustment ---
chunk_size_frame = tk.Frame(right_frame)
chunk_size_frame.pack(pady=5, fill=tk.X)
tk.Label(chunk_size_frame, text="Chunk size (words):").pack(side=tk.LEFT, padx=5)
chunk_size_entry = tk.Entry(chunk_size_frame, width=6)
chunk_size_entry.insert(0, "100")
chunk_size_entry.pack(side=tk.LEFT, padx=5)
chunk_size_entry.bind("<Return>", on_chunk_size_change)

# --- Entailment method ---
method_frame = tk.Frame(right_frame)
method_frame.pack(pady=5, fill=tk.X)
tk.Label(method_frame, text="Entailment method:").pack(side=tk.LEFT, padx=5)
entailment_method = tk.StringVar(value="max")
tk.Radiobutton(method_frame, text="Max", variable=entailment_method, value="max").pack(side=tk.LEFT)
tk.Radiobutton(method_frame, text="Average", variable=entailment_method, value="average").pack(side=tk.LEFT)

# --- Chunk table ---
tk.Label(right_frame, text="Chunks and Probabilities").pack()
chunk_frame = tk.Frame(right_frame)
chunk_frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
chunk_text = scrolledtext.ScrolledText(chunk_frame, wrap=tk.WORD, height=15)
chunk_text.pack(expand=True, fill=tk.BOTH)

# --- Question & NLI result ---
tk.Label(right_frame, text="Ask a Question").pack()
question_entry = tk.Entry(right_frame, width=60)
question_entry.pack(pady=5)
ask_button = tk.Button(right_frame, text="Run NLI", command=ask_question)
ask_button.pack(pady=5)

tk.Label(right_frame, text="NLI Result").pack()
nli_result_box = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, height=5)
nli_result_box.pack(expand=False, fill=tk.X, padx=5, pady=5)

status_label = tk.Label(right_frame, text="", font=("Arial", 10, "bold"))
status_label.pack(pady=5)

root.mainloop()
