<div align='center'>
	<img src=assets/offbook-icon.png width=150>
</div>

<h1 align='center'>OffBook</h1>

A Python project made to help actors learn their lines for a show and go "off book."

<details open>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About the Project
OffBook is an application made using Python that helps actors rehearse their lines. First, the application reads aloud a random line and the user must recite the next line. Then, they are automatically provided feedback based on their accuracy and overall performance.

### Features
<ul>
	<li>Two feedback modes</li>
		<ul>
			<li>Random line</li>
			<li>Entire scene</li>
		</ul>
	<li>Four different voices</li>
	<li>Various options to customize practice</li>
	<li>Gemini 2.5 Flash integration for feedback</li>
</ul>

## Getting Started
### Prerequisites
To use OffBook, you will need the following installed:
- Python
- FFmpeg

### Installation
<ol>
	<li>Download the ZIP from the <a href=https://github.com/bdarwish/offbook/releases/latest>releases tab</a> on the repository.</li>
	<li>Unzip the file you have downloaded into the location you would like to store OffBook</li>
	<li>Run <code>setup.command</code> (Mac/Linux) or <code>setup.bat</code> (Windows) to install dependencies</li>
</ol>

You have now installed the required dependencies and setup the app. You can then begin to use it by running `run.command` (Mac/Linux) or `run.bat` (Windows).

<hr>

### Note
On Mac/Linxu, you may need to run the following commands to run the shell scripts:
```bash
$ chmod +x path/to/run/setup.command
$ chmod +x path/to/run/run.command
```

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
Bilal Darwish - <a href='mailto:darwish.b.bilal@gmail.com'>darwish.b.bilal@gmail.com</a> <br>

Source Code and Issues: https://github.com/bdarwish/offbook/

## Acknowledgments
Dependencies:
- [SpeechCapture](https://pypi.org/project/speechcapture/) (Made by me!)
- [CustomTkinter](https://pypi.org/project/customtkinter/)
- [edge-tts](https://pypi.org/project/edge-tts/)
- [langchain-google-genai](https://pypi.org/project/langchain-google-genai/)
- [Pillow](https://pypi.org/project/pillow/)
- [playsound3](https://pypi.org/project/playsound3/)