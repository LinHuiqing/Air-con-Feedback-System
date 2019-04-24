<h1>INSTRUCTIONS ON OPERATING PROCEDURE:</h1>

<p>Our product operates on two seperate RPis and a Kivy application.
<br/>This instructable gives a quick description on how to run all of them.</p>

<h2>KIVY APPLICATION:</h2>
<p>Kivy Application is meant to run on mobile phones to:
<ul>
	<li>collect feedback from users in an air-conditioned room</li>
</ul>
</p>
<br/>
<p>The Kivy application consists of the main.py, 1 folder and 1 package:
<ul>
	<li>main.py (Entry point of code, front-end of the application)</li>
	<li>android.txt (Initialise android application)</li>
	<li>images (Folder containing all the images used in the application)</li>
	<li>backend (Package containing backend code)
		<ul>
			<li>__init__.py (Initialises package)</li>
			<li>firebase.py (Module to push and pull from Firebase)</li>
			<li>key.json (Key to access firebase)</li>
		</ul>
	</li>
</ul>
</p>
<h3>How to run: </h3>
<ol>
	<li>Build the code onto an Android phone</li>
	<li>Open and use the application</li>
</ol>
</p>

<h2>EXTERNAL RPI:</h2>
<p>
This RPi is located outside the cohort classroom to:
<ul>
	<li>Measure surrounding temperatures and push to Firebase</li>
</ul>
</p>
<br/>
<p>The external RPi consists of the MAIN.py code and 1 seperate module:
<ul>
	<li>MAIN.py (Entry point of code)</li>
	<li>FIREBASE.py (Module to push and pull from Firebase)</li>
</ul>
<h3>How to run: </h3>
<ol>
	<li>Connect the external RPi to the sensor</li>
	<li>Run the code on the RPi</li>
</ol>

<h2>INTERNAL RPI:</h2>
<p>This RPi is located inside the cohort classroom to:
<ul>
	<li>Measure the internal temperature and push to Firebase</li>
	<li>Pull Feedback and Temperature datas from Firebase</li>
	<li>Do active Machine Learning and calculate target aircon temperature</li>
	<li>Display OTP and temperature on LCD screen</li>
	<li>Resets feedback after collecting data</li>
	<li>Updates OTP every hour</li>
</ul>
</p>
<br/>
<p>The internal RPi consists of the MAIN.py code and 3 seperate modules:
<ul>
	<li>MAIN.py (Entry point of code)</li>
	<li>FIREBASE.py (Module to push and pull from Firebase)</li>
	<li>ML_ALGO.py (Module to predict optimal temperature using machine learning)</li>
	<li>I2C_LCD_driver.py (Module for LCD driver - DONUT TOUCH)</li>
</ul>
<h3>How to run: </h3>
<ol>
	<li>Connect the internal RPi to the sensor</li>
	<li>Run the MAIN.py code</li>
</ol>
"# Air-con-Feedback-System" 
