# CSCI2100A_24P1

Project Template for CUHK CSCI2100A Fall 2024

## Supported Languages

- C++
- Java
- Python**3**

**Note that python2 is deprecated and you should never use it in any new projects.**

## Quick Start Guide

This project officially support three platforms: Windows, macOS and Debian-based Linux distributions.

### Step1: Obtain your API key

Signup for a free account at [financialmodelingprep](https://site.financialmodelingprep.com/login)

Visit [https://financialmodelingprep.com/api/v3/market-capitalization/AAPL](https://financialmodelingprep.com/api/v3/market-capitalization/AAPL), the browser should automatically fill in the API key for you, copy the API key and store it in a safe place.

### Step2: setup the project

#### For C++ Users

##### Windows

This part is a little complicated as Windows does not come with a package manager and C++ compiler, we have to install the entire toolkit manually.

To begin with, check your system to make sure there is no existing `g++` command. If you have installed `mingw` or `cygwin`, you should uninstall them or remove then from environment variables first.

First you need to download `csci2100a_project1_toolkit.7z` from the course website, then extract the folder `gcc-14.2.0-no-debug`.

![win_step1](https://raw.githubusercontent.com/cmd2001/CSCI2100A_24P1/refs/heads/master/assets/win_step1.png)

Then you need to copy the folder into `C:\Program Files`.

**Attention: This step requires administrator privilege. Please check Yes for all files to avoid making incomplete copies.**

![win_step2](https://raw.githubusercontent.com/cmd2001/CSCI2100A_24P1/refs/heads/master/assets/win_step2.png)

After that, you need to add the path to the environment variables. Open the start menu and search for `env`, then click on `Edit the system environment variables`.

![win_step3](https://raw.githubusercontent.com/cmd2001/CSCI2100A_24P1/refs/heads/master/assets/win_step3.png)

Click on `Environment Variables...` in the bottom right corner, then click on `Path` in the `System variables` section, then click on `Edit...`.

![win_step4](https://raw.githubusercontent.com/cmd2001/CSCI2100A_24P1/refs/heads/master/assets/win_step4.png)

Click on `New`, then paste the path `C:\Program Files\gcc-14.2.0-no-debug\bin`, then click `OK`.

Next, create a new environment variable named `cpath`, and set the value to `C:\Program Files\gcc-14.2.0-no-debug\include`.

![win_step5](https://raw.githubusercontent.com/cmd2001/CSCI2100A_24P1/refs/heads/master/assets/win_step5.png)

Close all the windows with `OK`.

Finally, open a new command prompt at the root path of the project, and run the following command to check if the installation is successful.

```batch
g++ --version
g++ src/cpp/example.cpp -o code -lcurl -Wl,-Bstatic
set API_KEY=YOUR_API_KEY
code.exe
```

![win_step6](https://raw.githubusercontent.com/cmd2001/CSCI2100A_24P1/refs/heads/master/assets/win_step6.png)

##### macOS

First, make sure you have enabled the command line tools `xcode-select --install` and [Homebrew](https://brew.sh/) installed.

Then, you can install the required libraries using Homebrew.

```bash
brew install nlohmann-json
```

To check if the installation is successful, run the following command.

```bash
export CPLUS_INCLUDE_PATH=/opt/homebrew/Cellar/nlohmann-json/3.11.3/include
g++ src/cpp/example.cpp -o code -lcurl -std=c++17
export API_KEY="YOUR_API_KEY"
./code
```

**Note that the version number 3.11.3 may vary, but you can always check the actual path by `ls /opt/homebrew/Cellar/nlohmann-json`**

##### Linux

`apt` is all you need!

```bash
sudo apt install build-essential
sudo apt install libcurl4-openssl-dev nlohmann-json3-dev
```

To check if the installation is successful, run the following command.

```bash
g++ src/cpp/example.cpp -o code -lcurl
export API_KEY="YOUR_API_KEY"
./code
```

#### For Java Users

##### Windows

Download [OpenJDK17 Installer](https://aka.ms/download-jdk/microsoft-jdk-17.0.12-windows-x64.msi), then install it.

Launch a command prompt at the root path of the project, then run the following command to run the example code.

```batch
set API_KEY=YOUR_API_KEY
java -classpath ./lib/gson.jar src/java/example.java
```

##### macOS

First, make sure you have enabled the command line tools `xcode-select --install` and [Homebrew](https://brew.sh/) installed.

Then, install OpenJDK build by Microsoft using Homebrew.

```bash
brew install microsoft-openjdk@17
```

Run the example code with

```bash
export API_KEY="YOUR_API_KEY"
java -classpath ./lib/gson.jar src/java/example.java
```

##### Linux

```bash
sudo apt install openjdk-17-jdk
```

Then run the example code with

```bash
export API_KEY="YOUR_API_KEY"
java -classpath ./lib/gson.jar src/java/example.java
```

#### For Python Users

##### Windows

Download and install [Python3.12](https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe).

Launch a command prompt at the root path of the project, then run the following command to run the example code.

```batch
set API_KEY=YOUR_API_KEY
python src/python/example.py
```

##### macOS and Linux

macOS and Linux should have Python3 installed by default, if not you can install it using Homebrew or apt.

Run the following command to run the example code.

```bash
export API="YOUR_API_KEY"
python3 src/python/example.py
```

### Step 3: Run the example eval script

The entry point for the project is `entry.sh`, and by default its for C++.

Commend out the C++ part and uncomment the Java or Python part if you want to run the Java or Python version.

Finally, run the following command to execute the script.

```bash
bash entry.sh
```

### Step4: Write your own code

You can start writing your own code in the corresponding language directory, change `entry.sh` to run your code.

## Output Format

The output should be in csv format, as the exact format in the example output.

The filename should be `table1.csv`, 'table2.csv', 'table1_sorted_a.csv' and 'table1_sorted_b.csv', corresponding to the output of the of the first table, the second table, and the two sorted tables, respectively.

## Evaluation

The project will be evaluated based on the following criteria:

- Tests passed (45% total score): this part is related to the correctness of the outputs and the performance of your program (points will be deducted if the running time is long or the program generates incomplete/wrong outcomes);
- Report and analysis of results (25% total score):
  - (12%) The design of your program, including a clear illustration of the data structures used and their algorithms. Use one or more figures to explain your design.
  - (10%) The tradeoffs made in your design.
    - The tradeoffs include the parameter combinations studied in your implementation and a detailed analysis of your design choices.
    - Examples of tradeoffs made.
    - Discuss with justifications the best choice of the parameters to support the application. Analyze the results obtained and propose other approaches to improve them. It would help if you discussed the effects of your tradeoffs on solution times.
      A high score will be given only on a very detailed analysis.
    - Readability of the report (points will be deducted for poor readability).
    - (3%) A VeriGuide report on your written report.
- Program and functions implemented with proper documentation and comments (30% total score)
  - (15%) Implementing the data structures for the selection sort and the quick-sort.
  - (15%) Quality of program code, including proper documentation and instructions for the teaching assistants to compile and run your program. Provide a README file on how to compile and run your program. Also, explain the outputs generated by your program.

The First Part will be done by running the evaluation script, `eval.sh`, which will parse the output csv files and check its correctness.
