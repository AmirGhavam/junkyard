import os
import webbrowser

def open_all_htmls():
    # Get the current working directory
    cwd = os.getcwd()
    
    # List all files in the directory
    files = os.listdir(cwd)
    
    # Filter for HTML files
    html_files = [f for f in files if f.lower().endswith('.html')]
    
    if not html_files:
        print("No HTML files found in the current directory.")
        return

    print(f"Found {len(html_files)} HTML files. Opening them now...")
    
    for filename in html_files:
        # Construct the full file path
        file_path = os.path.join(cwd, filename)
        
        # specific to mac/unix file uri
        url = 'file://' + file_path
        
        print(f"Opening: {filename}")
        webbrowser.open_new_tab(url)

if __name__ == "__main__":
    open_all_htmls()
