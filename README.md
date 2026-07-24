# rmFixlayout
Unifies the Fixed Layout of Comics/Mangas (like Diary of a Wimpy Kid) for use on any eReader.
# NOTE
I used Gemini to troubleshoot, so some code is writen by AI. It still works perfect for the book I tried.
## Usage
This script requires the following:\
-Python\
-Playwright\
\
First rename your EPUB to .zip\
Then, find the folder containing all of the xhtml files\
Now, do Win + R and enter `cmd`\
Enter, `copy /b *.xhtml {filename}.html`\
Now, run the script by entering `python rmfixlayout.py`. This will out put a zip file.\
Once that is done, make it a .cbz file using KCC. (Assuming that you're going to use a Kindle)
