from altair import Type
import pandas as pd
import numpy as np
import time
# Load data from CSV
df=pd.read_csv("netflix_titles.csv")
print("\n===== Loaded Dataset =====")
print(df)
#hnadle missing values
print("\nMisssing Valus Summary::")
print(df.isnull().sum())
df['director'].fillna('Unknown',inplace=True)
df['cast'].fillna('Unknown',inplace=True)
#filling missing values with mode for categorical columns
categorical_cols=['director','cast','country','date_added','rating','duration','listed_in','description']
for col in categorical_cols:
  df[col].fillna(df[col].mode()[0],inplace=True)
print("\n===== Dataset after handling missing values =====")
print(df)   
#convert dataframe columns to numpy arrays
title=df["title"].to_numpy()
release_year=df["release_year"].to_numpy()
print("\n=====Numpy-Based-Analysis=====")
#descriptive statistics using numpy
print(f"Total title:{np.size(title)}")
print(f"release_year min and max:{np.min(release_year)}-{np.max(release_year)}")
print(f"Average release_year:{np.mean(release_year):.2f}")
print(f"release_year Std Dev:{np.std(release_year):.2f}")
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector
# ── MySQL setup (runs once, loads CSV into DB) ──
def setup_mysql():
    cfg={"host":"localhost","user":"root","password":"Kan@2418"}   # <-- add your password
    conn=mysql.connector.connect(**cfg)
    cur=conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS netflix_db")
    conn.commit();cur.close();conn.close()
    conn=mysql.connector.connect(host="localhost",user="root",password="Kan@2418",database="netflix_db")
    cur=conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS titles(
        show_id VARCHAR(10) PRIMARY KEY,type VARCHAR(20),title VARCHAR(300),
        director VARCHAR(300),country VARCHAR(200),release_year INT,
        rating VARCHAR(20),listed_in VARCHAR(300),duration VARCHAR(50))""")
    cur.execute("SELECT COUNT(*) FROM titles")
    if cur.fetchone()[0]==0:
        needed=["show_id","type","title","director","country","release_year","rating","listed_in","duration"]
        data=df[needed].fillna("Unknown")
        cur.executemany("INSERT IGNORE INTO titles VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        [tuple(r) for r in data.values])
        conn.commit();print("CSV loaded into MySQL.")
    cur.close();conn.close()
setup_mysql()


# ── Tkinter window ───────────────────────────────────

root=tk.Tk()

root.title("Netflix Data Explorer")

root.geometry("1000x680")

root.configure(bg="#141414")



tk.Label(root,text="NETFLIX",font=("Helvetica",22,"bold"),bg="#141414",fg="#e50914").pack(side=tk.TOP,anchor="w",padx=20,pady=(12,0))
tk.Label(root,text=" Data Explorer",font=("Helvetica",11),bg="#141414",fg="white").place(x=150,y=11)



sidebar=tk.Frame(root,bg="#1f1f1f",width=180)

sidebar.pack(side=tk.LEFT,fill=tk.Y,padx=(10,0),pady=10)

sidebar.pack_propagate(False)



chart_area=tk.Frame(root,bg="#141414")

chart_area.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=10,pady=10)



fig=plt.figure(figsize=(7,3.5))

fig.patch.set_facecolor("#222121")

canvas=FigureCanvasTkAgg(fig,master=chart_area)

canvas.get_tk_widget().pack(fill=tk.X)



# ── Filter bar ───────────────────────────────────────

filter_frame=tk.Frame(chart_area,bg="#1f1f1f",pady=6)

filter_frame.pack(fill=tk.X,pady=(6,0))

genre_var=tk.StringVar(value="All");year_var=tk.StringVar(value="All");type_var=tk.StringVar(value="All")
tk.Label(filter_frame,text="Genre",bg="#1f1f1f",fg="#aaaaaa",font=("Helvetica",9)).pack(side=tk.LEFT,padx=(10,3))

ttk.Combobox(filter_frame,textvariable=genre_var,state="readonly",width=16,
    values=["All","Dramas","Comedies","Documentaries","Action & Adventure",
            "Thrillers","Children & Family","Horror Movies"]).pack(side=tk.LEFT,padx=3)
tk.Label(filter_frame,text="Year",bg="#1f1f1f",fg="#aaaaaa",font=("Helvetica",9)).pack(side=tk.LEFT,padx=(10,3))
years=["All"]+[str(y) for y in sorted(df["release_year"].dropna().astype(int).unique(),reverse=True)]

ttk.Combobox(filter_frame,textvariable=year_var,state="readonly",width=7,values=years).pack(side=tk.LEFT,padx=3)

tk.Label(filter_frame,text="Type",bg="#1f1f1f",fg="#aaaaaa",font=("Helvetica",9)).pack(side=tk.LEFT,padx=(10,3))

ttk.Combobox(filter_frame,textvariable=type_var,state="readonly",width=9,values=["All","Movie","TV Show"]).pack(side=tk.LEFT,padx=3)

result_lbl=tk.Label(filter_frame,text="",bg="#1f1f1f",fg="#aaaaaa",font=("Helvetica",8))

result_lbl.pack(side=tk.RIGHT,padx=10)
# ── Results table ────────────────────────────────────
style=ttk.Style();style.theme_use("clam")
style.configure("N.Treeview",background="#1f1f1f",foreground="white",fieldbackground="#1f1f1f",rowheight=22,font=("Helvetica",8))
style.configure("N.Treeview.Heading",background="#e50914",foreground="white",font=("Helvetica",8,"bold"))
style.map("N.Treeview",background=[("selected","#e50914")])
table_frame=tk.Frame(chart_area,bg="#141414")
table_frame.pack(fill=tk.BOTH,expand=True,pady=(4,0))
cols=("Title","Type","Year","Genre","Country")
tree=ttk.Treeview(table_frame,columns=cols,show="headings",height=9,style="N.Treeview")
for c,w in zip(cols,[240,70,55,220,150]):
    tree.heading(c,text=c);tree.column(c,width=w,anchor=tk.W)
vsb=ttk.Scrollbar(table_frame,orient="vertical",command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
tree.pack(side=tk.LEFT,fill=tk.BOTH,expand=True);vsb.pack(side=tk.RIGHT,fill=tk.Y)
def filter_table():
    for r in tree.get_children():tree.delete(r)
    filtered=df.copy()
    if genre_var.get()!="All":filtered=filtered[filtered["listed_in"].str.contains(genre_var.get(),na=False)]
    if year_var.get()!="All":filtered=filtered[filtered["release_year"]==int(year_var.get())]
    if type_var.get()!="All":filtered=filtered[filtered["type"]==type_var.get()]
    for _,row in filtered.head(300).iterrows():
        tree.insert("",tk.END,values=(row["title"],row["type"],row["release_year"],row["listed_in"],row["country"]))
    result_lbl.config(text=f"{len(filtered)} results")
tk.Button(filter_frame,text="Search",command=filter_table,bg="#e50914",fg="white",
    font=("Helvetica",9,"bold"),relief=tk.FLAT,cursor="hand2",padx=8,pady=3).pack(side=tk.LEFT,padx=8)
tk.Button(filter_frame,text="Reset",
    command=lambda:[genre_var.set("All"),year_var.set("All"),type_var.set("All"),filter_table()],
    bg="#1f1f1f",fg="#aaaaaa",font=("Helvetica",9),relief=tk.FLAT,cursor="hand2").pack(side=tk.LEFT)

filter_table()
# ── Helper: clear axes before each chart ─────────────
def reset_ax():
   global ax
   fig.clf()
   ax=fig.add_subplot(111)
   ax.set_facecolor("#1f1f1f");fig.patch.set_facecolor("#141414")
   for s in ax.spines.values():s.set_edgecolor("#333333")
   ax.tick_params(colors="white",labelsize=8)
#visulation using matplotlib
def plot_release_year_histogram(release_year):
    reset_ax()                                              # added
    ax.hist(release_year,bins=30,color='skyblue',edgecolor='red')

    ax.set_title('Distribution of Release Year',color='white',fontsize=10)
    ax.set_xlabel('Release Year',color='#aaaaaa',fontsize=8)
    ax.set_ylabel('Number of Titles',color='#aaaaaa',fontsize=8)
    fig.tight_layout();canvas.draw()                        # replaced plt.show()

def show_Bar_chart(Type,df):
    reset_ax()                                              # added
    Type_counts=df[Type].value_counts()
    ax.bar(Type_counts.index,Type_counts.values,color='Lightgreen',edgecolor='lightyellow')
    ax.set_title("Movies vs TV Shows",color='white',fontsize=10)
    ax.set_xlabel("Type",color='#aaaaaa',fontsize=8)
    ax.set_ylabel("Count",color='#aaaaaa',fontsize=8)

    fig.tight_layout();canvas.draw()                        # replaced plt.show()
def show_county_bar():
   reset_ax()                                               # added
   top_countries=df["country"].value_counts().head(10)
   ax.bar(top_countries.index,top_countries.values,color='orange',edgecolor='red')
   ax.set_title("Top 10 Countries by Number of Titles",color='white',fontsize=10)
   ax.set_xlabel("Country",color='#aaaaaa',fontsize=8)
   ax.set_ylabel("Count",color='#aaaaaa',fontsize=8)
   ax.invert_xaxis()
   fig.tight_layout();canvas.draw()                         # replaced plt.show()
def show_pie_chart():
    reset_ax()                                              # added
    rating_counts=df["rating"].value_counts()
    ax.pie(rating_counts.values,labels=rating_counts.index,autopct='%1.1f%%',startangle=140,labeldistance=1.1,pctdistance=0.8)
    ax.set_title("Distribution of Ratings",fontsize=14,fontweight='bold',color='white')
    fig.tight_layout();canvas.draw()                        # replaced plt.show()


def animated_exit():
    print("\nThanks for using Netflix Data Visualizer ❤️")
    print("Generating an animated goodbye...")
    top=tk.Toplevel(root);top.title("Goodbye!");top.configure(bg="#141414");top.geometry("500x350")
    fig2,ax2=plt.subplots(figsize=(5,3));fig2.patch.set_facecolor("#141414");ax2.set_facecolor("#1f1f1f")
    c2=FigureCanvasTkAgg(fig2,master=top);c2.get_tk_widget().pack(fill=tk.BOTH,expand=True)
    x=np.linspace(0,4*np.pi,100)
    for i in range(1,8):
        y=np.sin(x+i)
        ax2.clear();ax2.set_facecolor("#1f1f1f")
        ax2.plot(x,y,color='orange')                        # your original logic kept
        ax2.set_title("Goodbye! •See you again • :)",color='white')
        c2.draw();top.update();time.sleep(0.6)              # replaced plt.pause()
    print("keep Coding , keep Learning!")
    top.after(1000,top.destroy)
# ── Sidebar buttons (replaces while True menu) ───────
tk.Label(sidebar,text="CHARTS",font=("Helvetica",10,"bold"),bg="#1f1f1f",fg="#aaaaaa").pack(pady=(10,5))

for label,cmd in [

    ("📊 Release Year",    lambda:plot_release_year_histogram(release_year)),  # option 1

    ("🎬 Movies vs Shows", lambda:show_Bar_chart('type',df)),                  # option 2

    ("🌍 Top 10 Countries",show_county_bar),                                   # option 3

    ("🥧 Rating Pie Chart",show_pie_chart),                                    # option 4

    ("👋 Animated Exit",   animated_exit),                                     # option 5

]:
    tk.Button(sidebar,text=label,command=cmd,bg="#1f1f1f",fg="white",
        font=("Helvetica",9),relief=tk.FLAT,cursor="hand2",anchor=tk.W,
        padx=10,pady=6,activebackground="#e50914",activeforeground="white"

        ).pack(fill=tk.X,padx=5,pady=2)



plot_release_year_histogram(release_year)   # show chart on launch

root.mainloop()