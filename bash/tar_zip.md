## 🧱 Basic Command (tar + gzip)

To compress a file or folder into a `.tar.gz` archive:

```bash
tar -czvf archive-name.tar.gz file_or_directory
```

### What the flags mean:

- `-c` → create archive

- `-z` → use gzip compression

- `-v` → verbose (shows progress, optional)

- `-f` → filename of the archive

---

## 📦 Examples

### 1. Compress a folder

```bash
tar -czvf myfolder.tar.gz myfolder/
```

### 2. Compress multiple files

```bash
tar -czvf files.tar.gz file1.txt file2.txt
```

### 3. Compress everything in current directory

```bash
tar -czvf backup.tar.gz *
```

---

## 📂 Extract (untar) later

```bash
tar -xzvf archive-name.tar.gz
```

- `-x` → extract

- `-z` → gzip

- `-v` → verbose

- `-f` → file

---

## ⚡ Quick Tip

If you don’t care about seeing the file list, skip `-v`:

```bash
tar -czf archive.tar.gz folder/
```

---

If you want, I can also show:

- how to exclude files (like `.git` or `node_modules`)

- or how to create smaller/faster archives (e.g., `xz` instead of gzip)

