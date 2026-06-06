# 🎬 Netflix Data Explorer — Desktop App

A desktop data analysis application built with **Python, Tkinter, MySQL, Matplotlib, Pandas and NumPy**.
Loads the Netflix titles dataset into a MySQL database and provides an interactive GUI to explore, filter, and visualize the data.

---

<img width="1917" height="1005" alt="image" src="https://github.com/user-attachments/assets/6f08cf29-4f23-43cb-a4a6-89c800e77eea" />


---

## ✨ Features

- 🖥️ Full desktop GUI built with Tkinter
- 🗄️ MySQL database integration — CSV loaded once, queried every run
- 📊 5 interactive charts:
  - Release Year Histogram
  - Movies vs TV Shows Bar Chart
  - Top 10 Countries Bar Chart
  - Rating Distribution Pie Chart
  - Animated Goodbye (sine wave animation)
- 🔍 Filter titles by Genre, Year, and Content Type
- 📋 Scrollable results table (ttk.Treeview)
- 🎨 Netflix-themed dark UI (red + black)

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Tkinter | GUI framework |
| MySQL | Database storage and querying |
| mysql-connector-python | Python ↔ MySQL connection |
| Pandas | Data loading and cleaning |
| NumPy | Statistical analysis |
| Matplotlib | Data visualization |

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Kandarphada18/netflix-tkinter-mysql.git
cd netflix-tkinter-mysql
```

### 2. Install required libraries
```bash
pip install -r requirements.txt
```

### 3. Install and start MySQL
- Download MySQL Community Server from https://dev.mysql.com/downloads/
- Start MySQL and note your root password

### 4. Add your MySQL password
Open `netflix_explorer.py` and update line with your password:
```python
"password": "your_password_here",
```

### 5. Place the dataset
Make sure `netflix_titles.csv` is in the same folder as `netflix_explorer.py`.
Download the dataset from: https://www.kaggle.com/datasets/shivamb/netflix-shows

### 6. Run the app
```bash
python netflix_explorer.py
```

> On first run, the app automatically creates the database, table, and loads the CSV into MySQL.
> Every run after that opens the GUI directly.

---

```

---


---

## 🧠 Key Concepts Demonstrated

- CRUD operations with MySQL using `mysql-connector-python`
- GUI development with Tkinter widgets (Treeview, Combobox, Button, Frame)
- Embedding Matplotlib charts inside a Tkinter window using `FigureCanvasTkAgg`
- Data cleaning with Pandas (fillna, mode imputation)
- NumPy-based descriptive statistics
- Dark-themed UI design in 
