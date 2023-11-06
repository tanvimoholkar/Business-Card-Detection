# Visiting Card scanner GUI

# imported tkinter library
from tkinter import *
import tkinter.messagebox as tmsg

# Pillow library for importing images
from PIL import Image, ImageTk

# library for filedialog (For file selection)
from tkinter import filedialog

# Pytesseract module importing
import pytesseract
import os.path
import re

root = Tk()

# fixing geometry of GUI
root.geometry("800x500")
root.maxsize(1000, 500)
root.minsize(600, 500)
root.title("Business card scanner")


# function for uploading file to GUI
def upload_file():
    global filename
    global start, last
    filename = filedialog.askopenfilename(
        initialdir="/Desktop",
        title="Select a card image",
        filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")),
    )

    if filename == "":
        t.delete(1.0, END)
        t.insert(1.0, "You have not provided any image to convert")
        tmsg.showwarning(
            title="Alert!", message="Please provide proper formatted image"
        )
        return

    else:
        p_label_var.set("Image uploaded successfully")
        l.config(fg="#0CDD19")

    if (
        filename.endswith(".JPG")
        or filename.endswith(".JPEG")
        or filename.endswith(".jpg")
        or filename.endswith(".jpeg")
        or filename.endswith(".PNG")
        or filename.endswith(".png")
    ):
        filename_rev = filename[::-1]
        last = filename.index(".")
        start = len(filename) - filename_rev.index("/") - 1


# Function for post-processing and data extraction
def extract_information(text):
    # Regular expressions for name, email, phone, address, and website
    name_pattern = r"(?:Mr\. )?\b[A-Z][a-z]+(?: [A-Z][a-z]+)*\b"
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    phone_pattern = r"\b\d{3}-\d{3}-\d{4}\b"
    url_pattern = r"(https?://\S+|www\.\S+)"
    address_pattern = r"(\d+ [A-Za-z]+ [\w\s]+)"

    # Use regular expressions to find matches in the text
    name_match = re.search(name_pattern, text)
    email_matches = re.findall(email_pattern, text)
    phone_matches = re.findall(phone_pattern, text)
    url_matches = re.findall(url_pattern, text)
    address_matches = re.findall(address_pattern, text)

    # Process and return the extracted information
    name = name_match.group() if name_match else "Name not found"
    emails = email_matches
    phones = phone_matches
    urls = url_matches
    address = address_matches[0] if address_matches else "Address not found"

    return (
        name,
        emails,
        phones,
        urls,
        address,
    )


# Function to display categorized information
def display_categorized_information():
    try:
        c_label_var.set("Categorized Output...")
        pytesseract.pytesseract.tesseract_cmd = (
            r"/opt/homebrew/Cellar/tesseract/5.3.3/bin/tesseract"
        )
        text = pytesseract.image_to_string(filename)
        display_information(text)

    except:
        t.delete(1.0, END)
        t.insert(1.0, "You have not provided any image to convert")
        tmsg.showwarning(
            title="Alert!", message="Please provide a properly formatted image"
        )


def display_information(text):
    # Call the extract_information function for post-processing
    name, emails, phones, urls, address = extract_information(text)

    # Display the categorized information
    t.delete(1.0, END)
    t.insert(1.0, f"Name: {name}\n")
    t.insert(END, "Emails:\n")
    for email in emails:
        t.insert(END, f"- {email}\n")
    t.insert(END, "Phone Numbers:\n")
    for phone in phones:
        t.insert(END, f"- {phone}\n")
    t.insert(END, "Websites:\n")
    for url in urls:
        t.insert(END, f"- {url}\n")
    t.insert(END, f"Address: {address}\n")


# Menu bar and navigation tab creation
mainmenu = Menu(root)
mainmenu.config(font=("Times", 29))

m1 = Menu(mainmenu, tearoff=0)
m1.add_command(
    label="Scan/Upload Visiting or Business cards and get all the text of cards",
    font=("Times", 13),
)
root.config(menu=mainmenu)
mainmenu.add_cascade(label="Aim", menu=m1)

m2 = Menu(mainmenu, tearoff=0)
m2.add_command(label="Computer Science and Engineering Student", font=("Times", 13))
m2.add_command(label="|| Coding Enthusiast ||", font=("Times", 13))
root.config(menu=mainmenu)
mainmenu.add_cascade(label="About us", menu=m2)

m3 = Menu(mainmenu, tearoff=0)
m3.add_command(label="", font=("Times", 13))
m3.add_separator()
m3.add_command(label="", font=("Times", 13))
m3.add_separator()
m3.add_command(
    label="LinkedIn: ",
    font=("Times", 13),
)
root.config(menu=mainmenu)
mainmenu.add_cascade(label="Contact us", menu=m3)

Label(
    text="Visiting card scanner", bg="#FAD2B8", fg="#39322D", font=("Times", 18)
).pack(fill="x")
Label(
    text="Python GUI",
    bg="#FAD2B8",
    fg="#39322D",
    font=("Times New Roman", 12, "italic"),
).pack(fill="x")

f1 = Frame()
f1.config(bg="white")
Label(f1, text="Browse photo to upload", width=20, font=("Times", 15), bg="white").pack(
    side="left"
)
Label(f1, text="format: png/jpeg", bg="white", width=30).pack(side="right", padx=5)
Button(
    f1,
    text="Upload card",
    bg="#F58D4B",
    font=("Times", 15),
    width=70,
    command=upload_file,
).pack(side="right")
f1.pack(pady=10, fill="x")
p_label_var = StringVar()
p_label_var.set("Please upload an image to scan")
l = Label(textvariable=p_label_var, fg="pink", bg="white")
l.pack()


Label(
    text="",
    bg="#433E3B",
    fg="white",
    font=("Times", 10, " italic"),
).pack(side="bottom", fill="x")
t = Text(root, height="9", font=("Times", 13))
t.pack(side="bottom", fill="x")
t.insert(1.0, "Text of converted card will be shown here...", END)
c_label_var = StringVar()
c_label_var.set("Ready for conversion")
c_label = Label(textvariable=c_label_var)
c_label.pack(side="bottom", anchor="w")
Button(
    root,
    text="Scan and Convert",
    bg="#F58D4B",
    font=("Times", 15),
    width=70,
    command=display_categorized_information,
).pack(pady="10", side="bottom")
root.mainloop()
