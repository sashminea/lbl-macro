# LBL Macro: Letter By Letter Macro

## Overview

**LBL Macro** (Letter By Letter Macro) is a unique application I developed to automate the creation of captivating short videos that showcase HTML, CSS, and JavaScript code snippets in a dynamic time-lapse format. This tool types out code character by character at customizable intervals, providing a visually striking display of the coding process.

Initially, I intended to develop this macro for Visual Studio Code (VS Code). However, due to some limitations and the absence of existing shortcuts for this kind of automation, I decided to pivot to using CodePen and other real-time HTML/CSS/JS previewers. This approach ensures a seamless visual experience while showcasing my coding skills.

## Features

- **Automated Typing:** LBL Macro types out code one character at a time, creating an engaging visual effect perfect for time-lapse videos.
- **Customizable Interval:** Set your preferred typing speed in microseconds to control the automation process.
- **Hotkeys Support:** Utilize convenient hotkeys to manage the macro functions:
  - **F9:** Start/Stop the Macro
  - **F8:** Open VS Code and create a new project folder
  - **F6:** Launch CodePen in your web browser
- **Settings Management:** Easily configure the path for VS Code and project folders.

## Prerequisites

- **Python 3.x** installed on your machine.
- Required packages: 
  - `tkinter`
  - `keyboard`
  - `pyautogui`
  
You can install the necessary packages using pip:

```bash
pip install keyboard pyautogui
```

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/LBL-Macro.git
   ```
   
2. Navigate to the project directory:
   ```bash
   cd LBL-Macro
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Usage Instructions

1. **Open the Application:** Launch LBL Macro by running the `main.py` file.
2. **Enter Your Code:** Type or paste your HTML, CSS, or JavaScript code in the text area.
3. **Configure Settings:** Adjust the typing interval in the settings window to control the speed of the automation.
4. **Start the Macro:** Press **F9** to begin the automated typing of your code.
5. **Open CodePen or VS Code:** Use **F6** to open CodePen or **F8** to launch VS Code and create a project folder for your code.

### Note
Before starting the macro, ensure that you adjust the file paths for VS Code and the folder location in the settings. This is crucial to avoid errors when attempting to open VS Code.

## Screenshots

<!-- Add your screenshots here -->
![Screenshot 1](https://i.postimg.cc/fLBLf7PP/image.png)
![Screenshot 2](https://i.postimg.cc/GtfmZLdJ/image.png)
![Screenshot 3](https://i.postimg.cc/MGwpkr24/image.png)

## Future Updates

- **VS Code Integration:** Although LBL Macro currently operates as a standalone tool, I am exploring better integration with VS Code in future updates if the limitations can be resolved.
- **Enhanced Features:** Future enhancements may include additional customization options and support for more coding environments.

## Contribution

Feel free to fork the repository and submit pull requests if you'd like to contribute to LBL Macro's development. Any enhancements or usability improvements are always welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Let me know if you’d like any further adjustments!
