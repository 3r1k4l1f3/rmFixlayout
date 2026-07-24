# rmFixlayout
Unifies the Fixed Layout of Comics/Mangas (like Diary of a Wimpy Kid) for use on any eReader.
# NOTE
I used Gemini to troubleshoot, so some code is writen by AI. It still works perfect for the book I tried.
# Usage
This script requires the following:\
-Python\
-Playwright\
\
First rename your EPUB to .zip\
Then, find the folder containing all of the xhtml files\
### Windows
Now, do Win + R and enter `cmd`\
Enter, `copy /b *.xhtml {filename}.html`
### Linux
Press Ctrl + Alt + T to open your default terminal.\
Run `python rmfixlayout.py`\
\
Once the script exits, run the 'kcc_input.zip' through KCC (Assuming that you're going to use a Kindle)
